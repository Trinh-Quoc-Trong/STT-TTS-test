# -*- coding: utf-8 -*-
"""
Module để xử lý chuyển văn bản thành giọng nói (Text-to-Speech) sử dụng gTTS.
"""
import os
import threading
import time
import sys
from gtts import gTTS
from pydub import AudioSegment

class TtsProcessor:
    """
    Lớp để xử lý văn bản và chuyển đổi thành giọng nói sử dụng đa luồng.
    """
    def __init__(self, text_file: str, output_dir: str, language: str = "vi", num_threads: int = 10, delay: int = 2):
        """
        Khởi tạo TtsProcessor.

        Args:
            text_file (str): Đường dẫn đến file văn bản đầu vào.
            output_dir (str): Thư mục để lưu file audio đã được ghép cuối cùng.
            language (str): Ngôn ngữ cho việc chuyển đổi TTS.
            num_threads (int): Số luồng sử dụng để tải các chunk audio.
            delay (int): Độ trễ (giây) giữa các yêu cầu của mỗi luồng để tránh bị giới hạn tốc độ.
        """
        self.text_file = text_file
        self.output_dir = output_dir
        self.language = language
        self.num_threads = num_threads
        self.delay_between_requests = delay
        
        self.project_dir = os.path.dirname(output_dir)
        self.temp_dir = os.path.join(self.project_dir, "temp_audio_chunks")
        self.final_audio_path = os.path.join(self.output_dir, "doc_len_001_merged.mp3")

        self.text_chunks = []
        self.status_report = []
        self.status_lock = threading.Lock()

    def run(self):
        """
        Phương thức chính để thực thi toàn bộ quy trình TTS.
        """
        print("Bắt đầu xử lý chuyển văn bản thành giọng nói...")
        
        # 1. Thiết lập và chuẩn bị
        if not self._prepare_directories_and_text():
            return # Dừng lại nếu chuẩn bị thất bại

        actual_num_threads = len(self.text_chunks)
        self._initialize_status_report(actual_num_threads)
        print(f"Đang xử lý {actual_num_threads} chunk văn bản với {actual_num_threads} luồng...")

        # 2. Bắt đầu các luồng xử lý
        merger_thread = threading.Thread(
            target=self._progressive_merger, 
            args=(actual_num_threads,)
        )
        merger_thread.start()

        download_threads = []
        for i in range(actual_num_threads):
            thread = threading.Thread(
                target=self._text_to_audio_chunk, 
                args=(self.text_chunks[i], i)
            )
            download_threads.append(thread)
            thread.start()
        
        # 3. Đợi hoàn thành
        for thread in download_threads:
            thread.join()
        print("Tất cả các luồng tải về đã hoàn thành.")

        merger_thread.join()
        print("Quá trình ghép audio đã kết thúc.")
        
        # 4. Các bước cuối cùng
        self._print_summary_table()
        self._open_final_audio()
        self._cleanup()
        print("Xử lý TTS đã hoàn tất.")
    
    def _prepare_directories_and_text(self) -> bool:
        """
        Đọc văn bản, chia nhỏ và tạo các thư mục cần thiết.
        Trả về True nếu thành công, False nếu thất bại.
        """
        # Tạo thư mục
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Đọc văn bản từ file
        try:
            with open(self.text_file, "r", encoding="utf8") as f:
                text = f.read()
            if not text.strip():
                print(f"Lỗi: File '{self.text_file}' rỗng. Dừng chương trình.")
                return False
            print(f"Đã đọc thành công văn bản: {text[:100]}...")
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file '{self.text_file}'.")
            return False
        except Exception as e:
            print(f"Đã xảy ra lỗi khi đọc file: {e}")
            return False
        
        # Chia văn bản thành các chunk
        self.text_chunks = self._split_text_by_word_count(text)
        if not self.text_chunks:
            print("Văn bản rỗng hoặc không thể chia nhỏ.")
            return False
        
        return True

    def _split_text_by_word_count(self, text_to_split: str, min_word_threshold: int = 50) -> list:
        """Chia văn bản thành self.num_threads chunk dựa trên số lượng từ."""
        words = text_to_split.strip().split()
        total_words = len(words)

        if total_words <= min_word_threshold:
            return [text_to_split.strip()]

        base_size = total_words // self.num_threads
        remainder = total_words % self.num_threads

        chunks = []
        start_idx = 0
        for i in range(self.num_threads):
            add_one = 1 if i < remainder else 0
            end_idx = start_idx + base_size + add_one
            chunk_words = words[start_idx:end_idx]
            chunks.append(' '.join(chunk_words))
            start_idx = end_idx

        return [c for c in chunks if c]

    def _initialize_status_report(self, num_chunks: int):
        """Tạo danh sách báo cáo trạng thái ban đầu."""
        self.status_report = [
            {
                "id": i,
                "download_status": "Chờ xử lý",
                "merge_status": "Chờ xử lý",
                "error": None
            }
            for i in range(num_chunks)
        ]

    def _text_to_audio_chunk(self, text_chunk: str, index: int):
        """Chuyển một chunk văn bản thành một file audio."""
        try:
            with self.status_lock:
                self.status_report[index]["download_status"] = "Đang xử lý"

            if not text_chunk:
                raise ValueError("Chunk văn bản rỗng.")

            sleep_time = index * self.delay_between_requests
            if sleep_time > 0:
                print(f"Luồng {index}: Đang chờ {sleep_time}s...")
                time.sleep(sleep_time)
            
            final_temp_path = os.path.join(self.temp_dir, f"temp_{index}.mp3")
            temp_file_path_tmp = final_temp_path + ".tmp"

            print(f"Luồng {index}: Đang gửi yêu cầu tới API...")
            tts = gTTS(text=text_chunk, lang=self.language, slow=False)
            tts.save(temp_file_path_tmp)
            
            os.rename(temp_file_path_tmp, final_temp_path)
            
            print(f"Luồng {index}: Chunk đã được lưu vào {final_temp_path}")
            with self.status_lock:
                self.status_report[index]["download_status"] = "Thành công"
        except Exception as e:
            error_message = f"Lỗi trong luồng {index}: {e}"
            print(error_message)
            with self.status_lock:
                self.status_report[index]["download_status"] = "Thất bại"
                self.status_report[index]["error"] = str(e)

    def _progressive_merger(self, num_chunks: int):
        """Ghép các chunk audio ngay khi chúng sẵn sàng."""
        print("Quá trình ghép file bắt đầu chạy song song.")
        combined_audio = AudioSegment.empty()
        files_processed_count = 0
        
        while files_processed_count < num_chunks:
            idx = files_processed_count
            chunk_file_path = os.path.join(self.temp_dir, f"temp_{idx}.mp3")
            
            is_downloaded = os.path.exists(chunk_file_path) and os.path.getsize(chunk_file_path) > 0
            
            with self.status_lock:
                is_failed = self.status_report[idx]['download_status'] == 'Thất bại'

            if is_downloaded:
                try:
                    time.sleep(0.2) 
                    segment = AudioSegment.from_mp3(chunk_file_path)
                    combined_audio += segment
                    print(f"-> Đã ghép chunk {idx + 1}/{num_chunks}.")
                    with self.status_lock:
                        self.status_report[idx]["merge_status"] = "Đã ghép"
                    
                    self._delete_temp_file(chunk_file_path)
                    files_processed_count += 1
                except Exception as e:
                    error_message = f"Lỗi khi xử lý {chunk_file_path}: {e}"
                    print(error_message)
                    with self.status_lock:
                        self.status_report[idx]['merge_status'] = 'Lỗi ghép file'
                        self.status_report[idx]['error'] = str(e)
                    files_processed_count += 1
            elif is_failed:
                print(f"-> Bỏ qua chunk {idx + 1}/{num_chunks} do lỗi tải về.")
                with self.status_lock:
                    self.status_report[idx]['merge_status'] = 'Đã bỏ qua'
                files_processed_count += 1
            else:
                time.sleep(0.5)

        if len(combined_audio) > 0:
            print(f"Đã ghép xong tất cả các chunk. Đang xuất file ra: {self.final_audio_path}")
            combined_audio.export(self.final_audio_path, format="mp3")
        else:
            print("Không có audio nào được tạo để ghép.")

    def _delete_temp_file(self, file_path: str):
        """Thử xóa một file tạm với vài lần thử lại."""
        for i in range(3):
            try:
                os.remove(file_path)
                return
            except OSError:
                time.sleep(0.5)
        print(f"Cảnh báo: Không thể xóa file tạm {file_path}.")

    def _print_summary_table(self):
        """In ra bảng tóm tắt kết quả xử lý."""
        print("\n\n" + "="*80)
        print("TÓM TẮT".center(80))
        print("="*80)
        print(f"| {'Chunk':<5} | {'Trạng thái Tải về':<25} | {'Trạng thái Ghép':<25} | {'Ghi chú':<15} |")
        print(f"|{'-'*7}|{'-'*27}|{'-'*27}|{'-'*17}|")
        
        for report in self.status_report:
            chunk_id = report['id'] + 1
            download_status = report['download_status']
            merge_status = report['merge_status']
            error_msg = "Lỗi" if report['error'] else "OK"
            print(f"| {chunk_id:<5} | {download_status:<25} | {merge_status:<25} | {error_msg:<15} |")
            
        print("="*80 + "\n")

    def _open_final_audio(self):
        """Mở file audio cuối cùng nếu nó tồn tại."""
        if os.path.exists(self.final_audio_path):
            print("Đang mở file audio cuối cùng...")
            try:
                os.startfile(self.final_audio_path)
            except AttributeError:
                print("Lệnh os.startfile() không khả dụng. Vui lòng mở file thủ công:")
                print(self.final_audio_path)
        else:
            print("Không tìm thấy file audio cuối cùng. Có thể đã xảy ra lỗi.")

    def _cleanup(self):
        """Dọn dẹp thư mục tạm."""
        print("Đang dọn dẹp các file tạm...")
        if not os.path.exists(self.temp_dir):
            return
            
        try:
            files_in_temp = os.listdir(self.temp_dir)
            if files_in_temp:
                print(f"Cảnh báo: Tìm thấy các file còn sót lại trong thư mục tạm. Đang xóa...")
                for filename in files_in_temp:
                    os.remove(os.path.join(self.temp_dir, filename))
            
            os.rmdir(self.temp_dir)
            print(f"Đã xóa thành công thư mục tạm: {self.temp_dir}")
        except OSError as e:
            print(f"Lỗi trong quá trình dọn dẹp {self.temp_dir}: {e}.") 