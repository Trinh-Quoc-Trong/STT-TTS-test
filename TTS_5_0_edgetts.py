# -*- coding: utf-8 -*-
# PHIÊN BẢN 5.2 - ĐẢM BẢO THỨ TỰ BẰNG CÁCH TÁCH BIỆT TẢI VÀ GHÉP FILE

import os
import asyncio
import edge_tts
import threading
from pydub import AudioSegment
import time
import sys

# --- YÊU CẦU CÀI ĐẶT ---
# pip install edge-tts pydub
#
# LƯU Ý: pydub yêu cầu ffmpeg để xử lý file MP3.
# Bạn cần tải và cài đặt ffmpeg, sau đó thêm nó vào PATH của hệ thống.
# Hướng dẫn có thể tìm thấy trên mạng, ví dụ: https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/

# --- CẤU HÌNH ---
# Danh sách các giọng đọc tiếng Việt sẽ được sử dụng luân phiên.
# Giọng Nam: vi-VN-NamMinhNeural
# Giọng Nữ: vi-VN-HoaiMyNeural
# VOICES_TO_USE = ["vi-VN-HoaiMyNeural", "vi-VN-NamMinhNeural"]
VOICES_TO_USE = ["vi-VN-NamMinhNeural"]
# VOICES_TO_USE = ["vi-VN-HoaiMyNeural"]

NUM_THREADS = 10  # Số lượng chunk văn bản sẽ được tạo
INPUT_TEXT_FILE = "run_text.txt"
OUTPUT_AUDIO_FILE = "doc_len_002_merged_edge.mp3" # File output mới

# -----------------

try:
    with open(INPUT_TEXT_FILE, "r", encoding="utf8") as file:
        text = file.read()
        if not text.strip():
            print(f"Lỗi: File '{INPUT_TEXT_FILE}' không có nội dung. Dừng chương trình.")
            sys.exit()
        print(f"\nSẽ đọc văn bản: {text[0:100]}...\n")
except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file '{INPUT_TEXT_FILE}'.\nVui lòng tạo file này, đặt nội dung cần đọc vào và chạy lại script.")
    sys.exit()
except Exception as e:
    print(f"Gặp lỗi khi đọc file: {e}")
    sys.exit()


def split_text_by_word_count(text_to_split: str, num_chunks: int, min_word_threshold: int = 50):
    """Chia văn bản thành *num_chunks* phần dựa trên số lượng từ."""
    words = text_to_split.strip().split()
    total_words = len(words)

    if total_words <= min_word_threshold:
        return [text_to_split.strip()]

    base_size = total_words // num_chunks
    remainder = total_words % num_chunks

    chunks = []
    start_idx = 0
    for i in range(num_chunks):
        add_one = 1 if i < remainder else 0
        end_idx = start_idx + base_size + add_one
        chunk_words = words[start_idx:end_idx]
        chunks.append(' '.join(chunk_words))
        start_idx = end_idx

    return [c for c in chunks if c]

async def text_to_audio_chunk_async(text_chunk, index, voice, temp_dir, status_report, status_lock):
    """
    [ASYNC] Chuyển một đoạn văn bản thành file audio bằng edge-tts.
    Đây là một coroutine, chạy đồng thời với các coroutine khác trong event loop của asyncio.
    """
    try:
        with status_lock:
            status_report[index]["download_status"] = "Đang xử lý"

        if not text_chunk:
            raise ValueError("Chunk văn bản rỗng.")

        final_temp_path = os.path.join(temp_dir, f"temp_{index}.mp3")

        print(f"Tác vụ {index}: Đang gửi yêu cầu tới API với giọng đọc '{voice}'...")
        
        communicate = edge_tts.Communicate(text_chunk, voice)
        await communicate.save(final_temp_path)

        print(f"Tác vụ {index}: Đã lưu chunk vào {final_temp_path}")
        with status_lock:
            status_report[index]["download_status"] = "Thành công"
    except Exception as e:
        error_message = f"Lỗi trong tác vụ {index}: {e}"
        print(error_message)
        with status_lock:
            status_report[index]["download_status"] = "Thất bại"
            status_report[index]["error"] = error_message

def print_summary_table(status_report):
    """In bảng tóm tắt trạng thái các luồng."""
    print("\n\n" + "="*78)
    print("BẢNG TÓM TẮT KẾT QUẢ".center(78))
    print("="*78)
    print(f"| {'Chunk':<5} | {'Trạng thái Tải về':<25} | {'Trạng thái Ghép file':<25} | {'Ghi chú':<10} |")
    print(f"|{'-'*7}|{'-'*27}|{'-'*27}|{'-'*12}|")
    
    all_successful = True
    for report in status_report:
        chunk_id = report['id'] + 1
        download_status = report['download_status']
        merge_status = report['merge_status']
        error_msg = "Có lỗi" if report['error'] else "OK"
        
        if download_status != "Thành công" or merge_status not in ["Đã ghép", "Bỏ qua (lỗi tải)", "Bỏ qua (không tìm thấy)"]:
             all_successful = False
            
        print(f"| {chunk_id:<5} | {download_status:<25} | {merge_status:<25} | {error_msg:<10} |")
        
    print("="*78)
    if all_successful:
        print("Tổng kết: Mọi hoạt động đã hoàn tất thành công!".center(78))
    else:
        print("Tổng kết: Có lỗi xảy ra trong quá trình xử lý.".center(78))
    print("="*78 + "\n")

def cleanup(temp_dir):
    """Dọn dẹp thư mục tạm và các file rác sau khi quá trình hoàn tất."""
    print("Bắt đầu dọn dẹp...")
    if not os.path.exists(temp_dir):
        print("Thư mục tạm không tồn tại, không cần dọn dẹp.")
        return
        
    try:
        files_in_temp = os.listdir(temp_dir)
        if files_in_temp:
            print(f"Cảnh báo: Vẫn còn file trong thư mục tạm. Sẽ tiến hành dọn dẹp...")
            for filename in files_in_temp:
                file_path = os.path.join(temp_dir, filename)
                try:
                    os.remove(file_path)
                    print(f" - Đã xóa file rác: {filename}")
                except OSError as e:
                    print(f" - Lỗi khi xóa file rác {file_path}: {e}")
        
        os.rmdir(temp_dir)
        print(f"Đã xóa thành công thư mục tạm: {temp_dir}")
    except OSError as e:
        print(f"Lỗi khi dọn dẹp thư mục tạm {temp_dir}: {e}.")

async def amain():
    """Hàm chính: Tải về đồng loạt, sau đó ghép file tuần tự."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    final_audio_path = os.path.join(project_dir, OUTPUT_AUDIO_FILE)
    temp_dir = os.path.join(project_dir, "temp_audio_chunks_edge") # Thư mục tạm mới

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    text_chunks = split_text_by_word_count(text, NUM_THREADS)
    
    if not text_chunks:
        print("Văn bản rỗng hoặc không thể chia nhỏ.")
        return
        
    if not VOICES_TO_USE:
        print("Lỗi: Danh sách giọng đọc 'VOICES_TO_USE' đang bị rỗng. Vui lòng thêm ít nhất một giọng đọc.")
        sys.exit()

    num_chunks = len(text_chunks)
    status_lock = threading.Lock()
    status_report = [{"id": i, "download_status": "Chưa xử lý", "merge_status": "Chưa xử lý", "error": None} for i in range(num_chunks)]

    print(f"Bắt đầu xử lý {num_chunks} chunk văn bản...")
    print(f"Các giọng đọc sẽ được sử dụng: {', '.join(VOICES_TO_USE)}")

    # --- GIAI ĐOẠN 1: TẢI XUỐNG ĐỒNG LOẠT ---
    print("\n--- Bắt đầu giai đoạn tải xuống ---")
    tasks = []
    for i in range(num_chunks):
        voice = VOICES_TO_USE[i % len(VOICES_TO_USE)]
        task = text_to_audio_chunk_async(text_chunks[i], i, voice, temp_dir, status_report, status_lock)
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    print("--- Tất cả các tác vụ tải về đã hoàn thành ---\n")

    # --- GIAI ĐOẠN 2: GHÉP FILE TUẦN TỰ ---
    print("--- Bắt đầu giai đoạn ghép file ---")
    combined_audio = AudioSegment.empty()
    for i in range(num_chunks):
        chunk_file_path = os.path.join(temp_dir, f"temp_{i}.mp3")
        
        with status_lock:
            is_failed = status_report[i]['download_status'] == 'Thất bại'

        if not is_failed and os.path.exists(chunk_file_path):
            try:
                with open(chunk_file_path, 'rb') as f:
                    segment = AudioSegment.from_file(f, format="mp3")
                combined_audio += segment
                with status_lock:
                    status_report[i]["merge_status"] = "Đã ghép"
                print(f"-> Đã ghép chunk {i + 1}/{num_chunks}.")
            except Exception as e:
                error_message = f"Lỗi khi xử lý file {chunk_file_path}: {e}"
                print(error_message)
                with status_lock:
                    status_report[i]['merge_status'] = 'Lỗi ghép file'
                    status_report[i]['error'] = error_message
        elif is_failed:
             with status_lock:
                status_report[i]['merge_status'] = 'Bỏ qua (lỗi tải)'
             print(f"-> Bỏ qua chunk {i + 1}/{num_chunks} do lỗi tải về.")
        else:
             with status_lock:
                status_report[i]['merge_status'] = 'Bỏ qua (không tìm thấy)'
             print(f"-> Cảnh báo: Bỏ qua chunk {i + 1}/{num_chunks} do không tìm thấy file, dù không báo lỗi tải.")

    # --- GIAI ĐOẠN 3: XUẤT FILE VÀ DỌN DẸP ---
    if len(combined_audio) > 0:
        print(f"Đã ghép xong tất cả. Lưu file vào: {final_audio_path}")
        combined_audio.export(final_audio_path, format="mp3")
    else:
        print("Không có file audio nào được tạo ra để ghép.")
    
    print_summary_table(status_report)

    if os.path.exists(final_audio_path):
        print(f"Đang mở file audio: {final_audio_path}")
        if sys.platform == "win32":
            os.startfile(final_audio_path)
    else:
        print("Không tìm thấy file audio cuối cùng. Có thể đã có lỗi xảy ra.")

    cleanup(temp_dir)

if __name__ == "__main__":
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
    except Exception as e:
        print(f"\nLỗi không xác định: {e}") 