# -*- coding: utf-8 -*-
# PHIÊN BẢN 6.0 - VieNeu-TTS (OFFLINE, GPU)
# Thay thế edge-tts bằng VieNeu-TTS: offline 100%, không bị throttle,
# chạy trên GPU CUDA (RTX 3060) hoặc CPU.

import os
import sys
import time
import numpy as np

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
VOICE_PRESET_INDEX = 0  # Đặt số (0, 1, 2...) để chọn giọng khác

# Số chunk chia văn bản (VieNeu xử lý local nên không cần quá nhiều)
NUM_CHUNKS = 10

# VieNeu mode: "standard" (PyTorch GPU), "fast" (LMDeploy GPU), None = Turbo (GGUF CPU)
VIENEU_MODE = "standard"  # GPU mode - chất lượng cao nhất

SAMPLE_RATE = 24000  # VieNeu output 24kHz

# --- CHỈNH GIỌNG (HẬU KỲ) ---
# Tốc độ nói: 1.0 = bình thường, 1.2 = nhanh hơn 20%, 0.8 = chậm hơn 20%
SPEED = 1.0

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
    """Loại bỏ markdown, ký tự đặc biệt, chuẩn hóa text cho TTS tiếng Việt."""
    t = raw_text

    # --- Xóa markdown ---
    t = re.sub(r'^---+\s*$', '', t, flags=re.MULTILINE)
    t = re.sub(r'^===+\s*$', '', t, flags=re.MULTILINE)
    t = re.sub(r'^#{1,6}\s+', '', t, flags=re.MULTILINE)
    t = re.sub(r'\*\*(.+?)\*\*', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'\*(.+?)\*', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'__(.+?)__', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'~~(.+?)~~', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'`{1,3}(.+?)`{1,3}', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', t)
    t = re.sub(r'!\[.*?\]\(.*?\)', '', t)

    # --- Xóa URL / HTML ---
    t = re.sub(r'https?://\S+', '', t)
    t = re.sub(r'<[^>]+>', '', t)

    # --- Xóa sạch ký tự nhiễu ---
    t = re.sub(r'[—–•→←✅❌⭐🔊🚀💾📋👤🎧🦜…""\u201c\u201d\u2018\u2019`~|>]', '', t)
    t = re.sub(r'^>\s*', '', t, flags=re.MULTILINE)
    t = re.sub(r'^[\-\*\+]\s+', '', t, flags=re.MULTILINE)
    t = re.sub(r'[{}\[\]()@#&]', '', t)

    # --- Khoảng trắng ---
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n{2,}', '\n', t)

    lines = [line.strip() for line in t.split('\n') if line.strip()]
    return ' '.join(lines)


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

    text_chunks = split_text_by_sentence(cleaned, NUM_CHUNKS)
    num_actual = len(text_chunks)
    print(f"\nĐã chia thành {num_actual} chunk:")
    for idx, ch in enumerate(text_chunks):
        preview = ch[:80].replace('\n', ' ')
        print(f"  [{idx+1}] ({len(ch.split())} từ) {preview}...")
    print()

    # --- GIAI ĐOẠN 2: SYNTHESIS TỪNG CHUNK ---
    print("--- Bắt đầu tổng hợp giọng nói ---")
    all_audio_segments = []
    total_synth_time = 0

    for i in tqdm(range(num_actual), desc="Tổng hợp", unit="chunk"):
        chunk = text_chunks[i]
        if not chunk.strip():
            continue

        try:
            start_chunk = time.time()

            kwargs = {"text": chunk}
            if voice_data is not None:
                kwargs["voice"] = voice_data

            audio_array = tts.infer(**kwargs)
            chunk_time = time.time() - start_chunk
            total_synth_time += chunk_time

            if audio_array is not None and len(audio_array) > 0:
                all_audio_segments.append(audio_array)
            else:
                tqdm.write(f"  Chunk {i+1}: Không nhận được audio (kết quả rỗng)")
        except Exception as e:
            tqdm.write(f"  Lỗi chunk {i+1}: {e}")

    print(f"\n--- Tổng hợp xong {len(all_audio_segments)}/{num_actual} chunk trong {total_synth_time:.1f}s ---\n")

    if not all_audio_segments:
        print("Không có audio nào được tạo ra. Dừng.")
        tts.close()
        return

    # --- GIAI ĐOẠN 3: GHÉP + HẬU KỲ + XUẤT FILE ---
    print("Đang ghép audio...")
    combined = np.concatenate(all_audio_segments)

    # Chỉnh cao độ (pitch) bằng librosa
    if PITCH_SHIFT != 0:
        import librosa
        print(f"Chỉnh cao độ: {PITCH_SHIFT:+} semitones...")
        combined = librosa.effects.pitch_shift(
            combined, sr=SAMPLE_RATE, n_steps=PITCH_SHIFT
        )

    # Chỉnh tốc độ bằng librosa (time_stretch giữ nguyên pitch)
    if SPEED != 1.0:
        import librosa
        print(f"Chỉnh tốc độ: {SPEED}x...")
        combined = librosa.effects.time_stretch(combined, rate=SPEED)

    if hasattr(combined, 'cpu'):
        combined = combined.cpu().numpy()
    combined = np.asarray(combined, dtype=np.float32)
    if combined.ndim > 1:
        combined = combined.flatten()

    temp_wav = os.path.join(temp_dir, "combined.wav")
    sf.write(temp_wav, combined, SAMPLE_RATE)

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
    if sys.platform == "win32" and os.path.exists(final_audio_path):
        print(f"\nĐang mở file audio...")
        os.startfile(final_audio_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
    except Exception as e:
        print(f"\nLỗi không xác định: {e}")
        import traceback
        traceback.print_exc()
