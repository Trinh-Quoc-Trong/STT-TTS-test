#
# /home/t9/miniconda3/envs/tts_env/bin/python /home/t9/code/phanMemDoc/TTS_7_0_bilingual.py
#
#
# -*- coding: utf-8 -*-
# PHIÊN BẢN 7.0 - BILINGUAL TTS (OFFLINE, GPU)
# Kết hợp VieNeu v3 (tiếng Việt) + Kokoro-82M (tiếng Anh)
# Tự nhận diện ngôn ngữ theo từng câu bằng lingua-py
# Chạy 100% offline trên GPU CUDA hoặc CPU.

import os
import sys
import time
import numpy as np
import re

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# --- KIỂM TRA DEPENDENCIES ---
try:
    from vieneu import Vieneu
except ModuleNotFoundError as exc:
    print("Lỗi: Chưa cài vieneu. Chạy: pip install vieneu")
    raise SystemExit(1) from exc

try:
    from kokoro import KPipeline
except ModuleNotFoundError as exc:
    print("Lỗi: Chưa cài kokoro. Chạy: pip install kokoro soundfile")
    print("Cần cài espeak-ng: sudo apt install espeak-ng")
    raise SystemExit(1) from exc

try:
    from lingua import Language, LanguageDetectorBuilder
except ModuleNotFoundError as exc:
    print("Lỗi: Chưa cài lingua. Chạy: pip install lingua-language-detector")
    raise SystemExit(1) from exc

from pydub import AudioSegment
from tqdm import tqdm
import soundfile as sf

# ═══════════════════════════════════════════════════════════════
# CẤU HÌNH
# ═══════════════════════════════════════════════════════════════

INPUT_TEXT_FILE = "run_text.txt"
OUTPUT_AUDIO_FILE = "doc_len_bilingual.mp3"

# --- VieNeu config ---
# Chọn giọng preset (None = dùng giọng mặc định 'Xuân Vĩnh' - Nam miền Nam)
VOICE_PRESET_INDEX = 2  # Đặt số (0, 1, 2...) để chọn giọng khác
# VieNeu mode: "standard" (PyTorch GPU), "fast" (LMDeploy GPU), None = Turbo (GGUF CPU)
VIENEU_MODE = "standard"

# --- Kokoro config ---
KOKORO_LANG = "a"          # "a" = American English, "b" = British English
KOKORO_VOICE = "af_heart"  # Giọng nữ Mỹ (tự nhiên nhất). Xem thêm: af_bella, am_adam, ...

# --- Audio config ---
VIENEU_SAMPLE_RATE = 24000   # VieNeu output sample rate
KOKORO_SAMPLE_RATE = 24000   # Kokoro output sample rate
OUTPUT_SAMPLE_RATE = 24000   # Sample rate đầu ra thống nhất

# --- HẬU KỲ RIÊNG TỪNG GIỌNG (post-processing, KHÔNG can thiệp mạng neuron) ---
# Tất cả xử lý bên dưới được thực hiện SAU KHI model AI tạo xong audio.
# Dùng librosa (pitch/speed) và numpy (volume) — hoàn toàn bên ngoài model.

# 🇻🇳 Tiếng Việt (VieNeu)
VI_SPEED = 1.5          # Tốc độ: 1.0 = bình thường, 1.5 = nhanh 50%
VI_VOLUME_DB = -10.0      # Âm lượng (dB): 0 = giữ nguyên, +3 = to hơn, -3 = nhỏ hơn
VI_PITCH_SHIFT = 0      # Cao độ (semitones): 0 = bình thường, -2 = trầm, +2 = cao

# 🇺🇸 Tiếng Anh (Kokoro)
EN_SPEED = 1.1         # Tốc độ: 1.0 = bình thường, 1.25 = nhanh 25%
EN_VOLUME_DB = +10.0      # Âm lượng (dB): 0 = giữ nguyên, +3 = to hơn, -3 = nhỏ hơn
EN_PITCH_SHIFT = 0      # Cao độ (semitones): 0 = bình thường, -2 = trầm, +2 = cao

# --- Ngôn ngữ fallback ---
# Khi lingua không nhận ra ngôn ngữ → mặc định là gì?
FALLBACK_LANG = "vi"  # "vi" hoặc "en"

# ═══════════════════════════════════════════════════════════════


def clean_text_for_tts(raw_text: str) -> str:
    """Lọc markdown, emoji, ký tự đặc biệt khỏi văn bản."""
    t = raw_text
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
    t = re.sub(r'[—–•→←↓✅❌✓✗⭐🔊🚀💾📋👤🎧🦜…""\u201c\u201d\u2018\u2019`~|><=#]', '', t)
    t = re.sub(r'-', ' ', t)
    t = re.sub(r'^>\s*', '', t, flags=re.MULTILINE)
    t = re.sub(r'^[\-\*\+]\s+', '', t, flags=re.MULTILINE)
    t = re.sub(r'[{}\[\]()@&]', '', t)
    t = re.sub(r'[ \t]+', ' ', t)
    lines = [line.strip() for line in t.split('\n') if line.strip()]
    return '\n'.join(lines)


def split_into_sentences(text: str) -> list[str]:
    """Tách văn bản thành danh sách các câu riêng lẻ."""
    # Tách theo dấu câu kết thúc (.!?) hoặc xuống dòng
    sentences = re.split(r'(?<=[.!?。\n])\s+', text.strip())
    # Lọc câu rỗng và strip whitespace
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def detect_language_per_sentence(
    sentences: list[str],
    detector,
    fallback: str = "vi"
) -> list[tuple[str, str]]:
    """
    Nhận diện ngôn ngữ cho từng câu.
    
    Returns:
        List of (sentence, lang_code) tuples
        lang_code: "vi" hoặc "en"
    """
    results = []
    for sentence in sentences:
        # Bỏ qua câu quá ngắn (dưới 3 ký tự) → fallback
        if len(sentence.strip()) < 3:
            results.append((sentence, fallback))
            continue
        
        detected = detector.detect_language_of(sentence)
        
        if detected == Language.VIETNAMESE:
            results.append((sentence, "vi"))
        elif detected == Language.ENGLISH:
            results.append((sentence, "en"))
        else:
            # Không nhận ra → dùng heuristic đơn giản
            # Nếu câu chứa dấu tiếng Việt → tiếng Việt
            if _has_vietnamese_chars(sentence):
                results.append((sentence, "vi"))
            else:
                results.append((sentence, fallback))
    
    return results


def _has_vietnamese_chars(text: str) -> bool:
    """Kiểm tra xem text có chứa ký tự đặc trưng tiếng Việt không."""
    # Các ký tự có dấu đặc trưng tiếng Việt (không xuất hiện trong tiếng Anh)
    viet_pattern = re.compile(
        r'[àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợ'
        r'ùúủũụưứừửữựỳýỷỹỵđ'
        r'ÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ'
        r'ÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ]'
    )
    return bool(viet_pattern.search(text))


def batch_by_language(labeled_sentences: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """
    Gom các câu liên tiếp cùng ngôn ngữ thành 1 batch.
    
    Returns:
        List of (batch_text, lang_code)
    """
    if not labeled_sentences:
        return []
    
    batches = []
    current_lang = labeled_sentences[0][1]
    current_texts = [labeled_sentences[0][0]]
    
    for sentence, lang in labeled_sentences[1:]:
        if lang == current_lang:
            current_texts.append(sentence)
        else:
            # Kết thúc batch hiện tại
            batches.append((" ".join(current_texts), current_lang))
            current_lang = lang
            current_texts = [sentence]
    
    # Batch cuối
    if current_texts:
        batches.append((" ".join(current_texts), current_lang))
    
    return batches


def synthesize_vieneu(tts_vieneu, text: str, voice_data) -> np.ndarray:
    """Tổng hợp tiếng Việt bằng VieNeu."""
    audio = tts_vieneu.infer(text, voice=voice_data)
    if hasattr(audio, 'cpu'):
        audio = audio.cpu().numpy()
    audio = np.asarray(audio, dtype=np.float32)
    if audio.ndim > 1:
        audio = audio.flatten()
    return audio


def synthesize_kokoro(pipeline, text: str) -> np.ndarray:
    """Tổng hợp tiếng Anh bằng Kokoro-82M."""
    audio_chunks = []
    generator = pipeline(text, voice=KOKORO_VOICE)
    for _, _, audio in generator:
        if hasattr(audio, 'cpu'):
            audio = audio.cpu().numpy()
        audio = np.asarray(audio, dtype=np.float32)
        if audio.ndim > 1:
            audio = audio.flatten()
        audio_chunks.append(audio)
    
    if audio_chunks:
        return np.concatenate(audio_chunks)
    return np.array([], dtype=np.float32)


def resample_audio(audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
    """Resample audio nếu sample rate khác nhau."""
    if orig_sr == target_sr:
        return audio
    
    try:
        import librosa
        return librosa.resample(audio, orig_sr=orig_sr, target_sr=target_sr)
    except ImportError:
        # Fallback: simple linear interpolation
        ratio = target_sr / orig_sr
        n_samples = int(len(audio) * ratio)
        indices = np.linspace(0, len(audio) - 1, n_samples)
        return np.interp(indices, np.arange(len(audio)), audio).astype(np.float32)


def post_process_audio(
    audio: np.ndarray,
    sample_rate: int,
    speed: float = 1.0,
    volume_db: float = 0.0,
    pitch_shift: int = 0
) -> np.ndarray:
    """
    Hậu kỳ audio SAU KHI model AI đã tạo xong.
    Hoàn toàn dùng thư viện bên ngoài, KHÔNG can thiệp vào mạng neuron.
    
    Args:
        audio: numpy array audio từ model
        sample_rate: sample rate của audio
        speed: tốc độ nói (1.0 = bình thường, >1.0 = nhanh hơn)
        volume_db: chỉnh âm lượng theo dB (0 = giữ nguyên, +3 = to hơn ~2x, -3 = nhỏ hơn)
        pitch_shift: chỉnh cao độ theo semitones (0 = giữ nguyên)
    
    Returns:
        numpy array audio đã xử lý hậu kỳ
    """
    if audio is None or len(audio) == 0:
        return audio

    # 1. Chỉnh âm lượng (dB → linear gain)
    #    Công thức: gain = 10^(dB/20)
    #    +6 dB ≈ gấp đôi âm lượng, -6 dB ≈ giảm một nửa
    if volume_db != 0.0:
        gain = 10.0 ** (volume_db / 20.0)
        audio = audio * gain
        # Clip để tránh clipping distortion
        audio = np.clip(audio, -1.0, 1.0)

    # 2. Chỉnh cao độ (pitch shift) bằng librosa
    #    Thay đổi cao độ mà KHÔNG thay đổi tốc độ
    if pitch_shift != 0:
        import librosa
        audio = librosa.effects.pitch_shift(
            audio, sr=sample_rate, n_steps=pitch_shift
        )

    # 3. Chỉnh tốc độ (time stretch) bằng librosa
    #    Thay đổi tốc độ nói mà KHÔNG thay đổi cao độ
    if speed != 1.0 and speed > 0:
        import librosa
        audio = librosa.effects.time_stretch(audio, rate=speed)

    return audio.astype(np.float32)


def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    final_audio_path = os.path.join(project_dir, OUTPUT_AUDIO_FILE)
    temp_dir = os.path.join(project_dir, "temp_bilingual_chunks")
    os.makedirs(temp_dir, exist_ok=True)

    # ═══════════════════════════════════════════════════════════
    # GIAI ĐOẠN 0: ĐỌC VĂN BẢN
    # ═══════════════════════════════════════════════════════════
    print("=" * 60)
    print("🌐 Bilingual TTS v7.0 — VieNeu v3 + Kokoro-82M")
    print("   Tự nhận diện Việt/Anh theo câu")
    print("=" * 60)

    try:
        with open(
            os.path.join(project_dir, INPUT_TEXT_FILE), "r", encoding="utf8"
        ) as file:
            text = file.read()
            if not text.strip():
                print(f"Lỗi: File '{INPUT_TEXT_FILE}' không có nội dung.")
                sys.exit()
            print(f"\nSẽ đọc văn bản: {text[:100]}...\n")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{INPUT_TEXT_FILE}'.")
        sys.exit()
    except Exception as e:
        print(f"Gặp lỗi khi đọc file: {e}")
        sys.exit()

    # ═══════════════════════════════════════════════════════════
    # GIAI ĐOẠN 1: LỌC VĂN BẢN + TÁCH CÂU + NHẬN DIỆN NGÔN NGỮ
    # ═══════════════════════════════════════════════════════════
    cleaned = clean_text_for_tts(text)
    print("Văn bản sau khi lọc:")
    print("-" * 40)
    print(cleaned[:500])
    print("-" * 40)

    # Tách thành từng câu
    sentences = split_into_sentences(cleaned)
    print(f"\nTổng số câu: {len(sentences)}")

    # Khởi tạo bộ nhận diện ngôn ngữ (chỉ load 2 ngôn ngữ)
    print("Đang khởi tạo bộ nhận diện ngôn ngữ (lingua-py)...")
    detector = (
        LanguageDetectorBuilder
        .from_languages(Language.VIETNAMESE, Language.ENGLISH)
        .build()
    )

    # Nhận diện ngôn ngữ từng câu
    labeled = detect_language_per_sentence(sentences, detector, fallback=FALLBACK_LANG)

    # Thống kê
    vi_count = sum(1 for _, lang in labeled if lang == "vi")
    en_count = sum(1 for _, lang in labeled if lang == "en")
    print(f"  Tiếng Việt: {vi_count} câu")
    print(f"  Tiếng Anh:  {en_count} câu")

    # In chi tiết nhận diện (tối đa 20 câu đầu)
    print(f"\nChi tiết nhận diện (hiển thị tối đa 20 câu đầu):")
    for i, (sent, lang) in enumerate(labeled[:20]):
        flag = "🇻🇳" if lang == "vi" else "🇺🇸"
        preview = sent[:60] + "..." if len(sent) > 60 else sent
        print(f"  {flag} [{lang.upper()}] {preview}")
    if len(labeled) > 20:
        print(f"  ... và {len(labeled) - 20} câu nữa")

    # Gom batch
    batches = batch_by_language(labeled)
    print(f"\n--- Đã gom thành {len(batches)} batch ---")
    for i, (batch_text, lang) in enumerate(batches):
        flag = "🇻🇳" if lang == "vi" else "🇺🇸"
        word_count = len(batch_text.split())
        preview = batch_text[:50] + "..." if len(batch_text) > 50 else batch_text
        print(f"  Batch {i+1}: {flag} [{lang.upper()}] ({word_count} từ) {preview}")

    # ═══════════════════════════════════════════════════════════
    # GIAI ĐOẠN 2: KHỞI TẠO CÁC ENGINE TTS
    # ═══════════════════════════════════════════════════════════

    # --- Khởi tạo VieNeu (nếu có câu tiếng Việt) ---
    tts_vieneu = None
    voice_data = None
    if vi_count > 0:
        mode_label = VIENEU_MODE or "turbo"
        print(f"\n🇻🇳 Đang khởi tạo VieNeu v3 (mode={mode_label})...")
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
                print(f"   GPU: {torch.cuda.get_device_name(0)}")
            else:
                print("   CUDA không khả dụng, VieNeu chạy trên CPU")
        tts_vieneu = Vieneu(**init_kwargs)
        init_time = time.time() - start_init
        print(f"   Khởi tạo VieNeu xong trong {init_time:.1f}s")

        # Chọn giọng preset
        voices = tts_vieneu.list_preset_voices()
        print("   Giọng preset có sẵn:")
        for i, (desc, voice_id) in enumerate(voices):
            marker = " <-- đang dùng" if (VOICE_PRESET_INDEX is not None and i == VOICE_PRESET_INDEX) else ""
            print(f"     [{i}] {desc} (ID: {voice_id}){marker}")

        if VOICE_PRESET_INDEX is not None and VOICE_PRESET_INDEX < len(voices):
            _, voice_id = voices[VOICE_PRESET_INDEX]
            voice_data = tts_vieneu.get_preset_voice(voice_id)
            print(f"   Đang dùng giọng: {voices[VOICE_PRESET_INDEX][0]}")
        else:
            print("   Đang dùng giọng mặc định")
    else:
        print("\n🇻🇳 Không có câu tiếng Việt — bỏ qua VieNeu")

    # --- Khởi tạo Kokoro (nếu có câu tiếng Anh) ---
    kokoro_pipeline = None
    if en_count > 0:
        print(f"\n🇺🇸 Đang khởi tạo Kokoro-82M (lang={KOKORO_LANG}, voice={KOKORO_VOICE})...")
        start_init = time.time()
        kokoro_pipeline = KPipeline(lang_code=KOKORO_LANG)
        init_time = time.time() - start_init
        print(f"   Khởi tạo Kokoro xong trong {init_time:.1f}s")
    else:
        print("\n🇺🇸 Không có câu tiếng Anh — bỏ qua Kokoro")

    # ═══════════════════════════════════════════════════════════
    # GIAI ĐOẠN 3: TỔNG HỢP AUDIO THEO BATCH
    # ═══════════════════════════════════════════════════════════
    print(f"\n{'=' * 60}")
    print(f"Bắt đầu tổng hợp {len(batches)} batch...")
    print(f"{'=' * 60}\n")

    all_audio_segments = []
    start_time = time.time()

    for i, (batch_text, lang) in enumerate(tqdm(batches, desc="Tổng hợp audio")):
        try:
            if lang == "vi" and tts_vieneu is not None:
                audio = synthesize_vieneu(tts_vieneu, batch_text, voice_data)
                # Resample nếu cần
                audio = resample_audio(audio, VIENEU_SAMPLE_RATE, OUTPUT_SAMPLE_RATE)
                # Hậu kỳ riêng cho tiếng Việt (SAU KHI model chạy xong)
                audio = post_process_audio(
                    audio, OUTPUT_SAMPLE_RATE,
                    speed=VI_SPEED,
                    volume_db=VI_VOLUME_DB,
                    pitch_shift=VI_PITCH_SHIFT
                )

            elif lang == "en" and kokoro_pipeline is not None:
                audio = synthesize_kokoro(kokoro_pipeline, batch_text)
                # Resample nếu cần
                audio = resample_audio(audio, KOKORO_SAMPLE_RATE, OUTPUT_SAMPLE_RATE)
                # Hậu kỳ riêng cho tiếng Anh (SAU KHI model chạy xong)
                audio = post_process_audio(
                    audio, OUTPUT_SAMPLE_RATE,
                    speed=EN_SPEED,
                    volume_db=EN_VOLUME_DB,
                    pitch_shift=EN_PITCH_SHIFT
                )

            else:
                print(f"  ⚠ Batch {i+1}: Không có engine cho ngôn ngữ '{lang}' — bỏ qua")
                continue

            if audio is not None and len(audio) > 0:
                all_audio_segments.append(audio)

        except Exception as e:
            flag = "🇻🇳" if lang == "vi" else "🇺🇸"
            print(f"\n  ❌ Lỗi batch {i+1} ({flag}): {e}")
            print(f"     Text: {batch_text[:80]}...")
            continue

    total_synth_time = time.time() - start_time
    print(f"\n--- Tổng hợp xong trong {total_synth_time:.1f}s ---\n")

    if not all_audio_segments:
        print("Không có audio nào được tạo ra. Dừng.")
        if tts_vieneu:
            tts_vieneu.close()
        return

    # Ghép tất cả audio
    combined = np.concatenate(all_audio_segments)

    # ═══════════════════════════════════════════════════════════
    # GIAI ĐOẠN 4: XUẤT FILE
    # (Hậu kỳ speed/volume/pitch đã được áp dụng riêng từng batch ở trên)
    # ═══════════════════════════════════════════════════════════
    combined = np.asarray(combined, dtype=np.float32)
    if combined.ndim > 1:
        combined = combined.flatten()

    temp_wav = os.path.join(temp_dir, "combined.wav")
    sf.write(temp_wav, combined, OUTPUT_SAMPLE_RATE)

    # Xuất MP3
    audio_seg = AudioSegment.from_wav(temp_wav)
    audio_seg.export(final_audio_path, format="mp3", bitrate="192k")
    duration_sec = len(audio_seg) / 1000

    print(f"\n{'=' * 60}")
    print(f"✅ Đã lưu: {final_audio_path}")
    print(f"   Thời lượng audio: {duration_sec/60:.1f} phút ({duration_sec:.0f}s)")
    print(f"   Tốc độ tổng hợp: {duration_sec/total_synth_time:.1f}x realtime")
    print(f"   Tiếng Việt: {vi_count} câu (VieNeu v3)")
    print(f"      Hậu kỳ: tốc độ={VI_SPEED}x, âm lượng={VI_VOLUME_DB:+.1f}dB, cao độ={VI_PITCH_SHIFT:+} semitones")
    print(f"   Tiếng Anh:  {en_count} câu (Kokoro-82M)")
    print(f"      Hậu kỳ: tốc độ={EN_SPEED}x, âm lượng={EN_VOLUME_DB:+.1f}dB, cao độ={EN_PITCH_SHIFT:+} semitones")
    print(f"{'=' * 60}")

    # Dọn dẹp
    if tts_vieneu:
        tts_vieneu.close()
    try:
        import glob
        for f in glob.glob(os.path.join(temp_dir, "*")):
            os.remove(f)
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
