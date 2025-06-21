# -*- coding: utf-8 -*-
"""
Điểm khởi chạy chính cho ứng dụng chuyển văn bản thành giọng nói.
"""
import os
from tts_processor import TtsProcessor

# --- CẤU HÌNH ---
INPUT_TEXT_FILE = "what_do_you_want_to_read.txt"
OUTPUT_AUDIO_DIR = "data" 
# Thư mục gốc của dự án
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# --- KẾT THÚC CẤU HÌNH ---

def main():
    """
    Khởi tạo và chạy bộ xử lý TTS.
    """
    print("--- Ứng dụng TTS chuyên nghiệp ---")
    
    # Xây dựng đường dẫn tuyệt đối, đầy đủ để đảm bảo tính ổn định
    input_file_path = os.path.join(PROJECT_ROOT, OUTPUT_AUDIO_DIR, INPUT_TEXT_FILE)
    output_dir_path = os.path.join(PROJECT_ROOT, OUTPUT_AUDIO_DIR)

    # Kiểm tra xem file đầu vào có tồn tại không trước khi bắt đầu
    if not os.path.exists(input_file_path):
        print(f"\nLỖI NGHIÊM TRỌNG: Không tìm thấy file đầu vào tại '{input_file_path}'")
        print("Vui lòng đảm bảo file tồn tại và đường dẫn trong main.py là chính xác.")
        return

    # Tạo và chạy bộ xử lý
    processor = TtsProcessor(
        text_file=input_file_path,
        output_dir=output_dir_path,
        language="vi",
        num_threads=10
    )
    processor.run()

if __name__ == "__main__":
    main() 