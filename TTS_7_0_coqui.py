# -*- coding: utf-8 -*-
# PHIÊN BẢN 7.0 - SỬ DỤNG MODEL TTS LOCAL VỚI COQUI TTS

import os
import sys
import shutil
import torch
from TTS.api import TTS
from pydub import AudioSegment

# --- YÊU CẦU CÀI ĐẶT ---
# pip install TTS pydub
#
# LƯU Ý QUAN TRỌNG:
# 1. Lần chạy đầu tiên, script sẽ tải model giọng nói về máy. Quá trình này có thể
#    mất một lúc và yêu cầu kết nối Internet. Các lần sau sẽ nhanh hơn.
#    Model cho tiếng Việt có thể nặng vài trăm MB.
# 2. pydub yêu cầu ffmpeg để xử lý file MP3.
#    Bạn cần tải và cài đặt ffmpeg, sau đó thêm nó vào PATH của hệ thống.
#    Hướng dẫn: https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/

# --- CẤU HÌNH ---
INPUT_TEXT_FILE = "run_text.txt"
OUTPUT_AUDIO_FILE = "doc_len_004_merged_coqui.mp3"

# Model giọng nói tiếng Việt từ Coqui TTS.
# Danh sách các model có sẵn: https://tts.readthedocs.io/en/latest/models.html
# "tts_models/vi/vivos/vinbigdata-vietnamese-v1" là một lựa chọn tốt.
COQUI_VOICE_MODEL = "tts_models/vi/vivos/vinbigdata-vietnamese-v1"

# Chia văn bản thành các câu để xử lý, Coqui hoạt động tốt nhất với từng câu.
# Sử dụng các dấu câu để tách.
SENTENCE_SPLITTERS = '.!?'

# -----------------

def check_ffmpeg():
    """Kiểm tra sự tồn tại của ffmpeg trong PATH hệ thống."""
    if shutil.which("ffmpeg") is None:
        print("CẢNH BÁO: Không tìm thấy 'ffmpeg' trong PATH hệ thống.")
        print("Vui lòng cài đặt ffmpeg và thêm vào PATH để có thể xuất file MP3.")
        return False
    print("Đã tìm thấy ffmpeg.")
    return True

def split_text_into_sentences(text: str):
    """Chia văn bản thành các câu dựa trên các dấu chấm câu."""
    import re
    sentences = re.split(f'([{SENTENCE_SPLITTERS}])', text)
    # Gộp lại dấu câu với câu trước nó
    result = [sentences[i] + (sentences[i+1] if i+1 < len(sentences) else '') for i in range(0, len(sentences), 2)]
    # Loại bỏ các chuỗi rỗng
    return [s.strip() for s in result if s.strip()]

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
    """Hàm chính: Tải model, tổng hợp âm thanh, sau đó ghép file."""
    check_ffmpeg()

    project_dir = os.path.dirname(os.path.abspath(__file__))
    final_audio_path = os.path.join(project_dir, OUTPUT_AUDIO_FILE)
    temp_dir = os.path.join(project_dir, "temp_audio_chunks_coqui")

    # Đọc file văn bản
    try:
        with open(INPUT_TEXT_FILE, "r", encoding="utf8") as file:
            text = file.read()
            if not text.strip():
                print(f"Lỗi: File '{INPUT_TEXT_FILE}' không có nội dung.")
                return
            print(f"\nSẽ đọc văn bản: {text[:100]}...\n")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{INPUT_TEXT_FILE}'.")
        return

    # Tạo thư mục tạm
    if os.path.exists(temp_dir):
        cleanup(temp_dir)
    os.makedirs(temp_dir)

    # --- GIAI ĐOẠN 1: KHỞI TẠO MODEL ---
    print("--- Bắt đầu giai đoạn khởi tạo model Coqui TTS ---")
    print("Lưu ý: Lần đầu có thể mất vài phút để tải model về máy.")
    
    # Kiểm tra xem có GPU không
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Sử dụng thiết bị: {device.upper()}")

    try:
        tts = TTS(model_name=COQUI_VOICE_MODEL, progress_bar=True).to(device)
        print("Model Coqui TTS đã sẵn sàng.")
    except Exception as e:
        print(f"Lỗi nghiêm trọng khi tải model Coqui TTS: {e}")
        cleanup(temp_dir)
        return

    # --- GIAI ĐOẠN 2: TỔNG HỢP ÂM THANH (TUẦN TỰ) ---
    print("\n--- Bắt đầu giai đoạn tổng hợp âm thanh ---")
    sentences = split_text_into_sentences(text)
    num_sentences = len(sentences)
    if num_sentences == 0:
        print("Không có câu nào để xử lý.")
        cleanup(temp_dir)
        return

    print(f"Văn bản đã được chia thành {num_sentences} câu.")
    
    synthesized_files = []
    for i, sentence in enumerate(sentences):
        print(f"Đang xử lý câu {i + 1}/{num_sentences}: \"{sentence[:50]}...\"")
        wav_path = os.path.join(temp_dir, f"temp_{i}.wav")
        try:
            # Tổng hợp audio từ text
            tts.tts_to_file(text=sentence, file_path=wav_path)
            synthesized_files.append(wav_path)
            print(f"-> Đã lưu câu {i + 1} thành công.")
        except Exception as e:
            print(f"Lỗi khi xử lý câu {i + 1}: {e}")

    # --- GIAI ĐOẠN 3: GHÉP FILE ---
    print("\n--- Bắt đầu giai đoạn ghép file ---")
    if not synthesized_files:
        print("Không có file audio nào được tạo. Dừng lại.")
        cleanup(temp_dir)
        return

    combined_audio = AudioSegment.empty()
    for wav_path in synthesized_files:
        if os.path.getsize(wav_path) > 0:
            try:
                segment = AudioSegment.from_wav(wav_path)
                combined_audio += segment
            except Exception as e:
                print(f"Lỗi khi đọc file chunk {wav_path}: {e}")
        else:
            print(f"Cảnh báo: Bỏ qua file rỗng {wav_path}")


    # --- GIAI ĐOẠN 4: XUẤT FILE VÀ DỌN DẸP ---
    if len(combined_audio) > 0:
        print(f"\nĐã ghép xong. Đang lưu file vào: {final_audio_path}")
        try:
            combined_audio.export(final_audio_path, format="mp3")
            print("Lưu file thành công!")
        except Exception as e:
            print(f"Lỗi khi xuất file MP3: {e}")
    else:
        print("\nKhông có dữ liệu audio để tạo file cuối cùng.")

    cleanup(temp_dir)

    if os.path.exists(final_audio_path):
        print(f"\nĐang mở file audio: {final_audio_path}")
        if sys.platform == "win32":
            os.startfile(final_audio_path)
    else:
        print("\nKhông tìm thấy file audio cuối cùng.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
    except Exception as e:
        print(f"\nLỗi không xác định: {e}")
        project_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(project_dir, "temp_audio_chunks_coqui")
        cleanup(temp_dir) 