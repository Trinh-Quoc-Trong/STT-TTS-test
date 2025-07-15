# -*- coding: utf-8 -*-
# <(6O9)>  
import os
from gtts import gTTS
import threading
from pydub import AudioSegment # Cần cài đặt: pip install pydub
import time
import math
import sys

# LƯU Ý: pydub yêu cầu ffmpeg để xử lý file MP3. 
# Bạn cần tải và cài đặt ffmpeg, sau đó thêm nó vào PATH của hệ thống.
# Hướng dẫn có thể tìm thấy trên mạng, ví dụ: https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/

# --- CẤU HÌNH ---
# Luôn cố gắng tạo 10 luồng, trừ khi văn bản quá ngắn (<50 từ)
NUM_THREADS = 10
DELAY_BETWEEN_REQUESTS = 0 # Giây. Tăng giá trị này nếu vẫn gặp lỗi 429.
# -----------------

language_ = "vi" # "vi" or "en" chọn ngôn ngữ
try:
    with open("run_text.txt", "r", encoding = "utf8") as file:
        # Đọc văn bản từ file run_text.txt
        text = file.read()
        if not text.strip():
            print("Lỗi: File 'run_text.txt' không có nội dung. Dừng chương trình.")
            sys.exit()
        print(f"\nSẽ đọc văn bản: {text[0:100]}...\n")
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file 'run_text.txt'.\nVui lòng tạo file này, đặt nội dung cần đọc vào và chạy lại script.")
    sys.exit()
except Exception as e:
    print(f"Gặp lỗi khi đọc file: {e}")
    sys.exit()


def split_text_by_word_count(text_to_split: str, num_chunks: int, min_word_threshold: int = 50):
    """Chia văn bản thành *num_chunks* phần dựa trên số lượng từ.

    - Nếu tổng số từ <= *min_word_threshold* thì trả về 1 chunk duy nhất.
    - Ngược lại, cố gắng chia đều thành *num_chunks* chunk (có thể một số chunk ngắn hơn 1 từ nếu quá ít từ)."""

    # Tách từ, bỏ các khoảng trắng thừa
    words = text_to_split.strip().split()
    total_words = len(words)

    # Văn bản quá ngắn, không cần chia
    if total_words <= min_word_threshold:
        return [text_to_split.strip()]

    # Tính toán kích thước cơ bản của mỗi chunk
    base_size = total_words // num_chunks
    remainder = total_words % num_chunks

    chunks = []
    start_idx = 0
    for i in range(num_chunks):
        # Phát cho những chunk đầu dư 1 từ nếu remainder > 0
        add_one = 1 if i < remainder else 0
        end_idx = start_idx + base_size + add_one
        chunk_words = words[start_idx:end_idx]
        chunks.append(' '.join(chunk_words))
        start_idx = end_idx

    # Loại bỏ các chunk rỗng (có thể xảy ra nếu tổng từ < num_chunks * 1)
    return [c for c in chunks if c]


def text_to_audio_chunk(text_chunk, index, language, temp_dir, status_report, status_lock):
    """Chuyển một đoạn văn bản thành file audio và lưu vào thư mục tạm."""
    try:
        with status_lock:
            status_report[index]["download_status"] = "Đang xử lý"

        if not text_chunk:
            raise ValueError("Chunk văn bản rỗng.")

        # Dàn cách các yêu cầu để tránh bị giới hạn tốc độ (rate limiting)
        sleep_time = index * DELAY_BETWEEN_REQUESTS
        if sleep_time > 0:
            print(f"Luồng {index}: Đang chờ {sleep_time} giây...")
            time.sleep(sleep_time)
            
        final_temp_path = os.path.join(temp_dir, f"temp_{index}.mp3")
        temp_file_path_tmp = final_temp_path + ".tmp" # Lưu vào file nháp

        print(f"Luồng {index}: Đang gửi yêu cầu tới API...")
        tts = gTTS(text=text_chunk, lang=language, slow=False)
        tts.save(temp_file_path_tmp) # Lưu vào file .tmp
        
        # Đổi tên file nháp thành file chính thức khi đã lưu xong
        os.rename(temp_file_path_tmp, final_temp_path)
        
        print(f"Luồng {index}: Đã lưu chunk vào {final_temp_path}")
        with status_lock:
            status_report[index]["download_status"] = "Thành công"
    except Exception as e:
        error_message = f"Lỗi trong luồng {index}: {e}"
        print(error_message)
        with status_lock:
            status_report[index]["download_status"] = "Thất bại"
            status_report[index]["error"] = error_message

def progressive_merger(temp_dir, num_chunks, final_audio_path, status_report, status_lock):
    """
    Theo dõi và ghép các file audio ngay khi chúng sẵn sàng theo đúng thứ tự.
    Chạy trong một luồng riêng.
    """
    print("Tiến trình ghép file bắt đầu chạy song song.")
    combined_audio = AudioSegment.empty()
    files_processed_count = 0
    
    # Vòng lặp sẽ tiếp tục cho đến khi tất cả các chunk được xử lý (ghép hoặc bỏ qua)
    while files_processed_count < num_chunks:
        current_chunk_index = files_processed_count
        chunk_file_path = os.path.join(temp_dir, f"temp_{current_chunk_index}.mp3")
        
        is_downloaded = os.path.exists(chunk_file_path) and os.path.getsize(chunk_file_path) > 0
        
        with status_lock:
            is_failed = status_report[current_chunk_index]['download_status'] == 'Thất bại'

        if is_downloaded:
            try:
                # Đợi một chút để đảm bảo file đã được ghi xong hoàn toàn
                time.sleep(0.2) 
                segment = AudioSegment.from_mp3(chunk_file_path)
                combined_audio += segment
                print(f"-> Đã ghép xong chunk {current_chunk_index + 1}/{num_chunks}.")
                with status_lock:
                    status_report[current_chunk_index]["merge_status"] = "Đã ghép"
                
                # Xóa file tạm ngay sau khi ghép
                deleted = False
                for i in range(3): # Thử tối đa 3 lần
                    try:
                        os.remove(chunk_file_path)
                        deleted = True
                        break
                    except OSError:
                        time.sleep(0.5)
                if not deleted:
                    print(f"CẢNH BÁO: Không thể xóa file tạm {chunk_file_path}.")

                files_processed_count += 1
            except Exception as e:
                error_message = f"Lỗi khi xử lý file {chunk_file_path}: {e}"
                print(error_message)
                with status_lock:
                    status_report[current_chunk_index]['merge_status'] = 'Lỗi ghép file'
                    status_report[current_chunk_index]['error'] = error_message
                files_processed_count += 1 # Bỏ qua chunk này và tiếp tục
        elif is_failed:
            print(f"-> Bỏ qua chunk {current_chunk_index + 1}/{num_chunks} do lỗi tải về.")
            with status_lock:
                status_report[current_chunk_index]['merge_status'] = 'Bỏ qua'
            files_processed_count += 1
        else:
            # File chưa sẵn sàng, đợi một chút rồi kiểm tra lại
            time.sleep(0.5)

    # Lưu file cuối cùng khi đã ghép tất cả các chunk thành công
    if len(combined_audio) > 0:
        print(f"Đã ghép xong tất cả. Lưu file vào: {final_audio_path}")
        combined_audio.export(final_audio_path, format="mp3")
    else:
        print("Không có file audio nào được tạo ra để ghép.")

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
        
        if download_status != "Thành công":
             all_successful = False
        if merge_status not in ["Đã ghép", "Bỏ qua"]:
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
        # Dọn dẹp các file rác còn sót lại (nếu có)
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
        
        # Xóa thư mục tạm nếu nó rỗng
        os.rmdir(temp_dir)
        print(f"Đã xóa thành công thư mục tạm: {temp_dir}")
    except OSError as e:
        print(f"Lỗi khi dọn dẹp thư mục tạm {temp_dir}: {e}.")

def main():
    """Hàm chính điều phối việc chia văn bản, xử lý đa luồng, và ghép file tiến độ."""
    project_dir = r"D:\code\phanMemDoc"
    final_audio_path = os.path.join(project_dir, "doc_len_001_merged.mp3")
    temp_dir = os.path.join(project_dir, "temp_audio_chunks")
    num_threads = NUM_THREADS

    # Tạo thư mục tạm nếu chưa có
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Chia văn bản thành các phần theo số từ
    text_chunks = split_text_by_word_count(text, num_threads)
    
    if not text_chunks:
        print("Văn bản rỗng hoặc không thể chia nhỏ.")
        return

    # Điều chỉnh số luồng nếu số chunk ít hơn và khởi tạo bảng báo cáo
    actual_num_threads = len(text_chunks)
    status_lock = threading.Lock()
    status_report = [
        {
            "id": i,
            "download_status": "Chưa xử lý",
            "merge_status": "Chưa xử lý",
            "error": None
        }
        for i in range(actual_num_threads)
    ]

    print(f"Bắt đầu xử lý {actual_num_threads} chunk văn bản với {actual_num_threads} luồng...")

    # Bắt đầu luồng ghép file chạy nền
    merger_thread = threading.Thread(
        target=progressive_merger, 
        args=(temp_dir, actual_num_threads, final_audio_path, status_report, status_lock)
    )
    merger_thread.start()

    # Tạo và bắt đầu các luồng tải về
    threads = []
    for i in range(actual_num_threads):
        thread = threading.Thread(target=text_to_audio_chunk, args=(text_chunks[i], i, language_, temp_dir, status_report, status_lock))
        threads.append(thread)
        thread.start()

    # Đợi tất cả các luồng tải về hoàn thành
    for thread in threads:
        thread.join()
    print("Tất cả các luồng tải về đã hoàn thành.")

    # Đợi luồng ghép file hoàn thành công việc của nó
    merger_thread.join()
    print("Tiến trình ghép file đã kết thúc.")
    
    # In bảng tóm tắt
    print_summary_table(status_report)

    # Kiểm tra xem file cuối cùng có tồn tại không trước khi mở
    if os.path.exists(final_audio_path):
        print("Đang mở file audio...")
        os.startfile(final_audio_path)
    else:
        print("Không tìm thấy file audio cuối cùng. Có thể đã có lỗi xảy ra.")

    # Dọn dẹp thư mục tạm
    cleanup(temp_dir)


if __name__ == "__main__":
    main()

