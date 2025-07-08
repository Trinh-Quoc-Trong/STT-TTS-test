# -*- coding: utf-8 -*-
# PHIÊN BẢN 6.0 - SỬ DỤNG MODEL TTS LOCAL VỚI PIPER

import os
import sys
import json
import wave
import shutil
from pydub import AudioSegment
from piper.voice import PiperVoice

# --- YÊU CẦU CÀI ĐẶT ---
# pip install piper-tts pydub
#
# LƯU Ý QUAN TRỌNG:
# 1. Lần chạy đầu tiên, script sẽ tải model giọng nói về máy (khoảng 150MB).
#    Các lần sau sẽ sử dụng lại model đã tải.
# 2. pydub yêu cầu ffmpeg để xử lý file MP3.
#    Bạn cần tải và cài đặt ffmpeg, sau đó thêm nó vào PATH của hệ thống.
#    Hướng dẫn: https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/

# --- CẤU HÌNH ---
INPUT_TEXT_FILE = "run_text.txt"
OUTPUT_AUDIO_FILE = "doc_len_003_merged_piper.mp3"

# Model giọng nói tiếng Việt từ Piper.
# Bạn có thể tìm các model khác tại: https://huggingface.co/rhasspy/piper-voices/tree/main
PIPER_VOICE_MODEL = "vi_VN-vivos-x-low"

# Chia văn bản thành các đoạn nhỏ hơn để xử lý, tránh quá tải bộ nhớ.
# Piper hoạt động tốt nhất với các câu ngắn.
MAX_WORDS_PER_CHUNK = 50

# -----------------

def check_ffmpeg():
    """Kiểm tra sự tồn tại của ffmpeg trong PATH hệ thống."""
    if shutil.which("ffmpeg") is None:
        print("CẢNH BÁO: Không tìm thấy 'ffmpeg' trong PATH hệ thống.")
        print("Thư viện 'pydub' cần ffmpeg để xuất file MP3.")
        print("Vui lòng cài đặt ffmpeg và thêm vào PATH để tiếp tục.")
        print("Hướng dẫn: https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/")
        # Mặc dù cảnh báo, script vẫn sẽ thử chạy.
        # pydub có thể gây lỗi nếu không có ffmpeg.
        return False
    print("Đã tìm thấy ffmpeg.")
    return True

def split_text_by_word_count(text_to_split: str, max_words: int):
    """Chia văn bản thành các phần có số từ không vượt quá max_words."""
    words = text_to_split.strip().split()
    if not words:
        return []

    chunks = []
    current_chunk = []
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def cleanup(temp_dir):
    """Dọn dẹp thư mục tạm và các file rác."""
    if os.path.exists(temp_dir):
        print(f"Bắt đầu dọn dẹp thư mục tạm: {temp_dir}")
        try:
            shutil.rmtree(temp_dir)
            print("Đã xóa thành công thư mục tạm.")
        except OSError as e:
            print(f"Lỗi khi xóa thư mục tạm {temp_dir}: {e}")

def main():
    """Hàm chính: Tải model, tổng hợp âm thanh tuần tự, sau đó ghép file."""
    check_ffmpeg()

    project_dir = os.path.dirname(os.path.abspath(__file__))
    final_audio_path = os.path.join(project_dir, OUTPUT_AUDIO_FILE)
    temp_dir = os.path.join(project_dir, "temp_audio_chunks_piper")

    # Đọc file văn bản
    try:
        with open(INPUT_TEXT_FILE, "r", encoding="utf8") as file:
            text = file.read()
            if not text.strip():
                print(f"Lỗi: File '{INPUT_TEXT_FILE}' không có nội dung. Dừng chương trình.")
                return
            print(f"\nSẽ đọc văn bản: {text[:100]}...\n")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{INPUT_TEXT_FILE}'.")
        print("Vui lòng tạo file này, đặt nội dung cần đọc vào và chạy lại script.")
        return
    except Exception as e:
        print(f"Gặp lỗi khi đọc file: {e}")
        return

    # Tạo thư mục tạm
    if os.path.exists(temp_dir):
        cleanup(temp_dir)
    os.makedirs(temp_dir)

    # --- GIAI ĐOẠN 1: KHỞI TẠO MODEL ---
    print("--- Bắt đầu giai đoạn khởi tạo model ---")
    print(f"Đang tải hoặc tìm model giọng nói: {PIPER_VOICE_MODEL}")
    print("Lưu ý: Lần đầu có thể mất vài phút để tải model về máy.")
    try:
        voice = PiperVoice.from_id(PIPER_VOICE_MODEL)
        print("Model đã sẵn sàng.")
    except Exception as e:
        print(f"Lỗi nghiêm trọng khi tải model: {e}")
        print("Vui lòng kiểm tra lại tên model và kết nối mạng (nếu là lần đầu).")
        cleanup(temp_dir)
        return

    # --- GIAI ĐOẠN 2: TỔNG HỢP ÂM THANH (TUẦN TỰ) ---
    print("\n--- Bắt đầu giai đoạn tổng hợp âm thanh ---")
    text_chunks = split_text_by_word_count(text, MAX_WORDS_PER_CHUNK)
    num_chunks = len(text_chunks)
    if num_chunks == 0:
        print("Không có văn bản để xử lý.")
        cleanup(temp_dir)
        return

    print(f"Văn bản đã được chia thành {num_chunks} chunk.")
    
    synthesized_files = []
    for i, chunk in enumerate(text_chunks):
        print(f"Đang xử lý chunk {i + 1}/{num_chunks}...")
        wav_path = os.path.join(temp_dir, f"temp_{i}.wav")
        try:
            with wave.open(wav_path, "wb") as wav_file:
                voice.synthesize(chunk, wav_file)
            synthesized_files.append(wav_path)
            print(f"-> Đã lưu chunk {i + 1} thành công.")
        except Exception as e:
            print(f"Lỗi khi xử lý chunk {i + 1}: {e}")

    # --- GIAI ĐOẠN 3: GHÉP FILE ---
    print("\n--- Bắt đầu giai đoạn ghép file ---")
    if not synthesized_files:
        print("Không có chunk audio nào được tạo thành công. Dừng quá trình.")
        cleanup(temp_dir)
        return

    combined_audio = AudioSegment.empty()
    for wav_path in synthesized_files:
        try:
            segment = AudioSegment.from_wav(wav_path)
            combined_audio += segment
        except Exception as e:
            print(f"Lỗi khi đọc file chunk {wav_path}: {e}")

    # --- GIAI ĐOẠN 4: XUẤT FILE VÀ DỌN DẸP ---
    if len(combined_audio) > 0:
        print(f"\nĐã ghép xong. Đang lưu file vào: {final_audio_path}")
        try:
            combined_audio.export(final_audio_path, format="mp3")
            print("Lưu file thành công!")
        except Exception as e:
            print(f"Lỗi khi xuất file MP3: {e}")
            print("Vui lòng đảm bảo ffmpeg đã được cài đặt và thêm vào PATH.")
    else:
        print("\nKhông có dữ liệu audio để tạo file cuối cùng.")

    # Dọn dẹp
    cleanup(temp_dir)

    # Mở file sau khi hoàn tất
    if os.path.exists(final_audio_path):
        print(f"\nĐang mở file audio: {final_audio_path}")
        if sys.platform == "win32":
            os.startfile(final_audio_path)
    else:
        print("\nKhông tìm thấy file audio cuối cùng. Có thể đã có lỗi xảy ra.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
    except Exception as e:
        print(f"\nLỗi không xác định: {e}")
        # Dọn dẹp phòng trường hợp lỗi giữa chừng
        project_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(project_dir, "temp_audio_chunks_piper")
        cleanup(temp_dir) 