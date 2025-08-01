# -*- coding: utf-8 -*-
# PHIÊN BẢN 5.2 - TÍCH HỢP CONTOUR VÀ HƯỚNG DẪN SSML
# Dựa trên phiên bản 5.1, thêm tùy chỉnh Contour và giải thích cách dùng SSML.

import os
import asyncio
import edge_tts
import threading
from pydub import AudioSegment
import time
import sys
from tqdm import tqdm

# --- YÊU CẦU CÀI ĐẶT ---
# pip install edge-tts pydub
#
# LƯU Ý: pydub yêu cầu ffmpeg để xử lý file MP3.
# Bạn cần tải và cài đặt ffmpeg, sau đó thêm nó vào PATH của hệ thống.
# Hướng dẫn có thể tìm thấy trên mạng, ví dụ: https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/

# --- CẤU HÌNH ---
# Giọng Nam: vi-VN-NamMinhNeural
VOICE_TO_USE = "vi-VN-NamMinhNeural"

# --- TÙY CHỈNH GIỌNG NÓI ---
# Rate: Tốc độ nói. Dạng chuỗi, ví dụ: "-10%". Mặc định là "+0%".
# Giảm để nói chậm hơn, tăng để nói nhanh hơn.
RATE = "+25%" 

# Volume: Âm lượng. Dạng chuỗi, ví dụ: "+20%". Mặc định là "+0%".
VOLUME = "+20%"

# Pitch: Cao độ. Dạng chuỗi, ví dụ: "-15Hz". Mặc định là "+0Hz".
# Giảm để giọng trầm hơn, tăng để giọng cao hơn.
PITCH = "-18Hz"

# --- SỬ DỤNG TÍNH NĂNG NÂNG CAO (SSML) ---
# Đối với Emphasis, Style, và Role-play, bạn cần sử dụng cú pháp SSML
# trực tiếp trong file `run_text.txt`. Script sẽ tự động xử lý.
#
# Ví dụ nội dung file `run_text.txt`:
#
#   Câu nói bình thường.
#   <mstts:express-as style="cheerful">
#       Câu này sẽ được đọc với giọng vui vẻ.
#   </mstts:express-as>
#   Câu này <emphasis level="strong">có từ được nhấn mạnh</emphasis>.
#
# Lưu ý: Các thẻ SSML phức tạp như <speak>, <voice> không cần thiết vì
# thư viện đã xử lý. Bạn chỉ cần chèn các thẻ điều khiển như trên.
# Tính năng và các style có sẵn phụ thuộc vào từng giọng đọc.

NUM_THREADS = 20  # Số lượng chunk văn bản sẽ được tạo
INPUT_TEXT_FILE = "run_text.txt"
OUTPUT_AUDIO_FILE = "doc_len_003_merged_edge_stronger.mp3" # File output mới

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
    for i in tqdm(range(num_chunks), desc="Chia văn bản thành các chunk"):
        add_one = 1 if i < remainder else 0
        end_idx = start_idx + base_size + add_one
        chunk_words = words[start_idx:end_idx]
        chunks.append(' '.join(chunk_words))
        start_idx = end_idx

    return [c for c in chunks if c]

async def text_to_audio_chunk_async(text_chunk, index, voice, temp_dir, status_report, status_lock, rate, volume, pitch):
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

        # Tắt log để giao diện gọn hơn, thanh tiến trình đã thể hiện trạng thái
        # print(f"Tác vụ {index}: Đang gửi yêu cầu tới API với giọng đọc '{voice}' (Rate: {rate}, Volume: {volume}, Pitch: {pitch})...")
        
        communicate = edge_tts.Communicate(text_chunk, voice, rate=rate, volume=volume, pitch=pitch)
        await communicate.save(final_temp_path)

        # Tắt log thành công, vì thanh tiến trình đã cập nhật rồi
        # print(f"Tác vụ {index}: Đã lưu chunk vào {final_temp_path}")
        with status_lock:
            status_report[index]["download_status"] = "Thành công"
    except Exception as e:
        # Sử dụng tqdm.write để log lỗi mà không làm hỏng thanh tiến trình
        error_message = f"Lỗi trong tác vụ {index + 1}: {e}"
        tqdm.write(error_message)
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
    temp_dir = os.path.join(project_dir, "temp_audio_chunks_edge_stronger") # Thư mục tạm mới

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    text_chunks = split_text_by_word_count(text, NUM_THREADS)
    
    if not text_chunks:
        print("Văn bản rỗng hoặc không thể chia nhỏ.")
        return
        
    if not VOICE_TO_USE:
        print("Lỗi: Giọng đọc 'VOICE_TO_USE' đang bị rỗng.")
        sys.exit()

    num_chunks = len(text_chunks)
    status_lock = threading.Lock()
    status_report = [{"id": i, "download_status": "Chưa xử lý", "merge_status": "Chưa xử lý", "error": None} for i in range(num_chunks)]

    print(f"Bắt đầu xử lý {num_chunks} chunk văn bản...")
    print(f"Giọng đọc sẽ được sử dụng: {VOICE_TO_USE}")
    print(f"Tùy chỉnh - Tốc độ: {RATE}, Âm lượng: {VOLUME}, Cao độ: {PITCH}")


    # --- GIAI ĐOẠN 1: TẢI XUỐNG ĐỒNG LOẠT ---
    print("\n--- Bắt đầu giai đoạn tải xuống ---")
    tasks = []
    # Bỏ tqdm ở vòng lặp tạo task để tránh hiển thị thừa
    for i in range(num_chunks):
        task = text_to_audio_chunk_async(
            text_chunks[i], i, VOICE_TO_USE, temp_dir, status_report, status_lock, 
            rate=RATE, volume=VOLUME, pitch=PITCH
        )
        tasks.append(task)
    
    # Sử dụng `asyncio.as_completed` với `tqdm` để có thanh tiến trình thực
    # khi các tác vụ thực sự hoàn thành.
    for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Tải xuống các chunk", unit="chunk"):
        await f

    print("--- Tất cả các tác vụ tải về đã hoàn thành ---\n")

    # --- GIAI ĐOẠN 2: GHÉP FILE TUẦN TỰ ---
    print("--- Bắt đầu giai đoạn ghép file ---")
    combined_audio = AudioSegment.empty()
    for i in tqdm(range(num_chunks), desc="Ghép các chunk", unit="chunk"):
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
                # Tắt log ghép file thành công để gọn terminal
                # print(f"-> Đã ghép chunk {i + 1}/{num_chunks}.")
            except Exception as e:
                error_message = f"Lỗi khi xử lý file {chunk_file_path}: {e}"
                tqdm.write(error_message)
                with status_lock:
                    status_report[i]['merge_status'] = 'Lỗi ghép file'
                    status_report[i]['error'] = error_message
        elif is_failed:
             with status_lock:
                status_report[i]['merge_status'] = 'Bỏ qua (lỗi tải)'
             tqdm.write(f"-> Bỏ qua chunk {i + 1}/{num_chunks} do lỗi tải về.")
        else:
             with status_lock:
                status_report[i]['merge_status'] = 'Bỏ qua (không tìm thấy)'
             tqdm.write(f"-> Cảnh báo: Bỏ qua chunk {i + 1}/{num_chunks} do không tìm thấy file, dù không báo lỗi tải.")

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