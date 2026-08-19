# 
# /home/t9/miniconda3/envs/tts_env/bin/python /home/t9/code/phanMemDoc/TTS_6_0_vieneu.py
# 
# 
# -*- coding: utf-8 -*-
# PHIÊN BẢN 6.0 - VieNeu-TTS (OFFLINE, GPU)
# Thay thế edge-tts bằng VieNeu-TTS: offline 100%, không bị throttle,
# chạy trên GPU CUDA (RTX 3060) hoặc CPU.

import os
import sys
import time
import numpy as np
import concurrent.futures

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from vieneu import Vieneu
except ModuleNotFoundError as exc:
    print("Lỗi: Chưa cài vieneu. Chạy: pip install vieneu[gpu]")
    raise SystemExit(1) from exc

from pydub import AudioSegment
from tqdm import tqdm
import re
import soundfile as sf

# --- CẤU HÌNH ---
INPUT_TEXT_FILE = "run_text.txt"
OUTPUT_AUDIO_FILE = "doc_len_vieneu.mp3"

# Chọn giọng preset (None = dùng giọng mặc định 'Xuân Vĩnh' - Nam miền Nam)
# Chạy script sẽ in danh sách giọng có sẵn để bạn chọn.
VOICE_PRESET_INDEX = 2  # Đặt số (0, 1, 2...) để chọn giọng khác

# Số chunk chia văn bản (VieNeu xử lý local nên không cần quá nhiều)
NUM_CHUNKS = 24

MAX_WORKER = 1
# VieNeu mode: "standard" (PyTorch GPU), "fast" (LMDeploy GPU), None = Turbo (GGUF CPU)
VIENEU_MODE = "standard"  # Sử dụng LMDeploy GPU - Tốc độ rất cao

SAMPLE_RATE = 24000  # VieNeu output 24kHz

# --- CHỈNH GIỌNG (HẬU KỲ BẰNG TOOL BÊN NGOÀI FFmpeg) ---
# Tốc độ nói: 1.0 = bình thường, 1.25 = nhanh hơn 25%, 1.5 = nhanh hơn 50%
# Hoàn toàn dùng phần mềm bên ngoài xử lý sau khi AI đã tạo xong audio!
SPEED = 1.5

# Cao độ (semitones): 0 = bình thường, -2 = trầm hơn, +2 = cao hơn
# Khoảng hợp lý: -5 đến +5
PITCH_SHIFT = 0

# -----------------

try:
    with open(INPUT_TEXT_FILE, "r", encoding="utf8") as file:
        text = file.read().lower()
        if not text.strip():
            print(f"Lỗi: File '{INPUT_TEXT_FILE}' không có nội dung.")
            sys.exit()
        print(f"\nSẽ đọc văn bản: {text[0:100]}...\n")
except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file '{INPUT_TEXT_FILE}'.")
    sys.exit()
except Exception as e:
    print(f"Gặp lỗi khi đọc file: {e}")
    sys.exit()


def clean_text_for_tts(raw_text: str) -> str:
    t = raw_text.lower()
    t = re.sub(r'^=+\s*$', '', t, flags=re.MULTILINE)
    t = re.sub(r'^-+\s*$', '', t, flags=re.MULTILINE)
    t = re.sub(r'^#{1,6}\s+', '', t, flags=re.MULTILINE)
    t = re.sub(r'\*\*(.+?)\*\*', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'\*(.+?)\*', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'__(.+?)__', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'~~(.+?)~~', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'`{1,3}(.+?)`{1,3}', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'!\[.*?\]\(.*?\)', '', t)
    t = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', t)
    t = re.sub(r'https?://\S+', '', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'[\u2500-\u257F\u2580-\u259F]', '', t)
    t = re.sub(r'[—–•→←↓✅❌✓✗⭐🔊🚀💾📋👤🎧🦜…""\u201c\u201d\u2018\u2019`~|><=+#]', '', t)    
    t = re.sub(r'-', ' ', t)
    t = re.sub(r'^>\s*', '', t, flags=re.MULTILINE)
    t = re.sub(r'^[\-\*\+]\s+', '', t, flags=re.MULTILINE)
    t = re.sub(r'[{}\[\]()@&]', '', t)
    t = re.sub(r'[ \t]+', ' ', t)
    lines = [line.strip() for line in t.split('\n') if line.strip()]
    return '\n'.join(lines)


def split_text_by_sentence(text_to_split: str, num_chunks: int, min_word_threshold: int = 30):
    """Chia văn bản thành chunks, cố gắng tách theo câu để giọng đọc tự nhiên hơn."""
    sentences = re.split(r'(?<=[.!?。\n])\s+', text_to_split.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    total_words = sum(len(s.split()) for s in sentences)
    if total_words <= min_word_threshold:
        return [text_to_split.strip()]

    target_words = total_words / num_chunks
    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        current_chunk.append(sentence)
        current_word_count += word_count

        if current_word_count >= target_words and len(chunks) < num_chunks - 1:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_word_count = 0

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return [c for c in chunks if c.strip()]


def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    final_audio_path = os.path.join(project_dir, OUTPUT_AUDIO_FILE)
    temp_dir = os.path.join(project_dir, "temp_vieneu_chunks")
    os.makedirs(temp_dir, exist_ok=True)

    # --- GIAI ĐOẠN 0: KHỞI TẠO VIENEU ---
    print("=" * 60)
    print("VieNeu-TTS v6.0 - Offline Vietnamese TTS")
    print("=" * 60)
    mode_label = VIENEU_MODE or "turbo"
    print(f"\nĐang khởi tạo VieNeu (mode={mode_label})...")
    print("(Lần đầu sẽ tải model từ HuggingFace, sau đó dùng cache)\n")

    start_init = time.time()
    init_kwargs = {}
    if VIENEU_MODE is not None:
        init_kwargs["mode"] = VIENEU_MODE
    if VIENEU_MODE == "standard":
        import torch
        if torch.cuda.is_available():
            init_kwargs["backbone_repo"] = "pnnbao-ump/VieNeu-TTS-0.3B"
            init_kwargs["backbone_device"] = "cuda"
            init_kwargs["codec_device"] = "cuda"
            init_kwargs["gguf_filename"] = "VieNeu-TTS-0.3B-Q4_K_M.gguf"
            print(f"GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("CUDA không khả dụng, chạy trên CPU")
    tts = Vieneu(**init_kwargs)
    init_time = time.time() - start_init
    print(f"Khởi tạo xong trong {init_time:.1f}s\n")

    # Liệt kê giọng có sẵn
    voices = tts.list_preset_voices()
    print("Các giọng preset có sẵn:")
    for i, (desc, voice_id) in enumerate(voices):
        marker = " <-- đang dùng" if (VOICE_PRESET_INDEX is not None and i == VOICE_PRESET_INDEX) else ""
        print(f"  [{i}] {desc} (ID: {voice_id}){marker}")

    voice_data = None
    if VOICE_PRESET_INDEX is not None and VOICE_PRESET_INDEX < len(voices):
        _, voice_id = voices[VOICE_PRESET_INDEX]
        voice_data = tts.get_preset_voice(voice_id)
        print(f"\nĐang dùng giọng: {voices[VOICE_PRESET_INDEX][0]}")
    else:
        print("\nĐang dùng giọng mặc định (Xuân Vĩnh)")

    # --- GIAI ĐOẠN 1: LỌC MARKDOWN + CHIA VĂN BẢN ---
    cleaned = clean_text_for_tts(text)
    print("Văn bản sau khi lọc:")
    print("-" * 40)
    print(cleaned[:500])
    print("-" * 40)



    # Chia văn bản thành các câu/đoạn ngắn (khoảng 30-50 từ/chunk)
    sentences = re.split(r'(?<=[.!?。\n])\s+', cleaned.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    current_chunk = []
    current_len = 0
    for s in sentences:
        words = len(s.split())
        if current_len + words > 40 and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [s]
            current_len = words
        else:
            current_chunk.append(s)
            current_len += words
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    if not chunks:
        chunks = [cleaned]

    print(f"\n--- Đã chia thành {len(chunks)} chunks để xử lý tối ưu ---")
    
    all_audio_segments = []
    start_time = time.time()
    try:
        from tqdm import tqdm
        for i, chunk in enumerate(tqdm(chunks, desc="Tổng hợp chunks")):
            # Gọi tts.infer cho từng chunk
            audio = tts.infer(chunk, voice=voice_data)
            if hasattr(audio, 'cpu'):
                audio = audio.cpu().numpy()
            all_audio_segments.append(audio)
            
        combined = np.concatenate(all_audio_segments)
        
    except Exception as e:
        print(f"Lỗi: {e}")
        return
        
    total_synth_time = time.time() - start_time
    print(f"\n--- Tổng hợp xong trong {total_synth_time:.1f}s ---\n")

    if combined is None or len(combined) == 0:
        print("Không có audio nào được tạo ra. Dừng.")
        tts.close()
        return

    # --- GIAI ĐOẠN 3: HẬU KỲ + XUẤT FILE ---

    # --- GIAI ĐOẠN 3: HẬU KỲ + XUẤT FILE ---

    if hasattr(combined, 'cpu'):
        combined = combined.cpu().numpy()
    combined = np.asarray(combined, dtype=np.float32)
    if combined.ndim > 1:
        combined = combined.flatten()

    temp_wav = os.path.join(temp_dir, "combined.wav")
    sf.write(temp_wav, combined, SAMPLE_RATE)

    # Chỉnh cao độ (pitch) bằng librosa (nếu có)
    if PITCH_SHIFT != 0:
        import librosa
        print(f"Chỉnh cao độ: {PITCH_SHIFT:+} semitones...")
        y, sr = librosa.load(temp_wav, sr=SAMPLE_RATE)
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=PITCH_SHIFT)
        sf.write(temp_wav, y_shifted, SAMPLE_RATE)

    # Chỉnh tốc độ bằng FFmpeg (Công cụ bên ngoài, không đổi tham số mô hình AI)
    if SPEED != 1.0:
        import subprocess
        print(f"Sử dụng công cụ bên ngoài (FFmpeg) để chỉnh tốc độ: {SPEED}x...")
        print("=> Audio đang được xử lý hậu kỳ bằng FFmpeg độc lập với mô hình AI.")
        temp_speed_wav = os.path.join(temp_dir, "combined_speed.wav")
        # Lệnh FFmpeg: atempo cho phép tăng giảm tốc độ mà không bị méo tiếng
        cmd = [
            "ffmpeg", "-y", "-i", temp_wav, 
            "-filter:a", f"atempo={SPEED}", 
            temp_speed_wav
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        temp_wav = temp_speed_wav

    audio_seg = AudioSegment.from_wav(temp_wav)
    audio_seg.export(final_audio_path, format="mp3", bitrate="192k")
    duration_sec = len(audio_seg) / 1000
    print(f"\nĐã lưu: {final_audio_path}")
    print(f"Thời lượng audio: {duration_sec/60:.1f} phút ({duration_sec:.0f}s)")
    print(f"Tốc độ tổng hợp: {duration_sec/total_synth_time:.1f}x realtime")
    if SPEED != 1.0 or PITCH_SHIFT != 0:
        print(f"Hậu kỳ: tốc độ={SPEED}x, cao độ={PITCH_SHIFT:+} semitones")

    # Dọn dẹp
    tts.close()
    try:
        os.remove(temp_wav)
        os.rmdir(temp_dir)
    except OSError:
        pass

    # Mở file
    if os.path.exists(final_audio_path):
        print(f"\nĐang mở file audio...")
        if sys.platform == "win32":
            os.startfile(final_audio_path)
        elif sys.platform.startswith('linux'):
            import subprocess
            subprocess.call(['xdg-open', final_audio_path])
        elif sys.platform == "darwin":
            import subprocess   
            subprocess.call(['open', final_audio_path])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
