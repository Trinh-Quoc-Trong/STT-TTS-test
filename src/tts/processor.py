# -*- coding: utf-8 -*-
"""
Module chính điều phối quá trình chuyển văn bản thành giọng nói.
"""
import os
import threading
import time

from .status_manager import StatusManager
from .audio_handler import AudioHandler

class TtsProcessor:
    """
    Lớp điều phối chính, quản lý toàn bộ quy trình chuyển đổi TTS.
    Sử dụng StatusManager và AudioHandler để thực hiện các tác vụ cụ thể.
    """
    def __init__(self, text_file: str, output_dir: str, language: str = "vi", num_threads: int = 10, delay: int = 2):
        """
        Khởi tạo TtsProcessor.
        """
        self.text_file = text_file
        self.output_dir = output_dir
        self.language = language
        self.num_threads = num_threads
        self.delay_between_requests = delay
        
        project_dir = os.path.dirname(output_dir)
        self.temp_dir = os.path.join(project_dir, "temp_audio_chunks")
        self.final_audio_path = os.path.join(self.output_dir, "doc_len_001_merged.mp3")

        self.text_chunks = []
        self.status_manager = None
        self.audio_handler = None

    def run(self):
        """
        Phương thức chính để thực thi toàn bộ quy trình TTS.
        """
        print("Bắt đầu xử lý chuyển văn bản thành giọng nói...")
        
        if not self._prepare():
            return

        actual_num_threads = len(self.text_chunks)
        self.status_manager = StatusManager(actual_num_threads)
        self.audio_handler = AudioHandler(self.language, self.temp_dir)

        print(f"Đang xử lý {actual_num_threads} chunk văn bản với {actual_num_threads} luồng...")

        merger_thread = threading.Thread(
            target=self.audio_handler.merge_audio_chunks, 
            args=(actual_num_threads, self.final_audio_path, self.status_manager)
        )
        merger_thread.start()

        download_threads = []
        for i in range(actual_num_threads):
            thread = threading.Thread(
                target=self._download_worker, 
                args=(self.text_chunks[i], i)
            )
            download_threads.append(thread)
            thread.start()
        
        for thread in download_threads:
            thread.join()
        print("Tất cả các luồng tải về đã hoàn thành.")

        merger_thread.join()
        print("Quá trình ghép audio đã kết thúc.")
        
        self.status_manager.print_summary_table()
        self._open_final_audio()
        self._cleanup()
        print("Xử lý TTS đã hoàn tất.")
    
    def _prepare(self) -> bool:
        """
        Chuẩn bị các thư mục và dữ liệu văn bản.
        Trả về True nếu thành công, False nếu thất bại.
        """
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
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
        
        self.text_chunks = self._split_text(text)
        if not self.text_chunks:
            print("Văn bản rỗng hoặc không thể chia nhỏ.")
            return False
        
        return True

    def _split_text(self, text_to_split: str, min_word_threshold: int = 50) -> list:
        """Chia văn bản thành các chunk dựa trên số lượng từ."""
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

    def _download_worker(self, text_chunk: str, index: int):
        """
        Worker function cho mỗi luồng tải về.
        Bao gồm cả việc chờ và xử lý lỗi.
        """
        try:
            self.status_manager.update_download_status(index, "Đang xử lý")

            sleep_time = index * self.delay_between_requests
            if sleep_time > 0:
                print(f"Luồng {index}: Đang chờ {sleep_time}s...")
                time.sleep(sleep_time)
            
            file_path = self.audio_handler.download_audio_chunk(text_chunk, index)
            
            print(f"Luồng {index}: Chunk đã được lưu vào {file_path}")
            self.status_manager.update_download_status(index, "Thành công")
        except Exception as e:
            error_message = f"Lỗi trong luồng {index}: {e}"
            print(error_message)
            self.status_manager.update_download_status(index, "Thất bại", str(e))

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