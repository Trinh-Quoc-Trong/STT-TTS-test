# -*- coding: utf-8 -*-
"""
Module để xử lý các tác vụ liên quan đến audio: tải về và ghép file.
"""
import os
import time
from gtts import gTTS
from pydub import AudioSegment

class AudioHandler:
    """
    Xử lý việc tải các chunk audio từ gTTS và ghép chúng lại với nhau.
    """
    def __init__(self, language: str = "vi", temp_dir: str = "temp_audio_chunks"):
        """
        Khởi tạo AudioHandler.

        Args:
            language (str): Ngôn ngữ cho việc chuyển đổi TTS.
            temp_dir (str): Thư mục tạm để lưu các chunk audio.
        """
        self.language = language
        self.temp_dir = temp_dir

    def download_audio_chunk(self, text_chunk: str, index: int) -> str:
        """
        Tải một chunk audio, lưu vào file tạm và trả về đường dẫn.
        
        Args:
            text_chunk (str): Đoạn văn bản cần chuyển đổi.
            index (int): Chỉ số của chunk, dùng để đặt tên file.

        Returns:
            str: Đường dẫn đến file mp3 tạm đã được tạo.
        
        Raises:
            Exception: Nếu có lỗi xảy ra trong quá trình tải về hoặc lưu file.
        """
        if not text_chunk:
            raise ValueError("Chunk văn bản rỗng.")
        
        final_temp_path = os.path.join(self.temp_dir, f"temp_{index}.mp3")
        temp_file_path_tmp = final_temp_path + ".tmp"

        print(f"Luồng {index}: Đang gửi yêu cầu tới API...")
        tts = gTTS(text=text_chunk, lang=self.language, slow=False)
        tts.save(temp_file_path_tmp)
        
        # Đổi tên file nháp thành file chính thức khi đã lưu xong
        os.rename(temp_file_path_tmp, final_temp_path)
        
        return final_temp_path

    def merge_audio_chunks(self, num_chunks: int, final_audio_path: str, status_manager):
        """
        Theo dõi và ghép các file audio ngay khi chúng sẵn sàng theo đúng thứ tự.
        
        Args:
            num_chunks (int): Tổng số chunk cần ghép.
            final_audio_path (str): Đường dẫn để lưu file audio cuối cùng.
            status_manager (StatusManager): Đối tượng để cập nhật và kiểm tra trạng thái.
        """
        print("Quá trình ghép file bắt đầu chạy song song.")
        combined_audio = AudioSegment.empty()
        files_processed_count = 0
        
        while files_processed_count < num_chunks:
            idx = files_processed_count
            chunk_file_path = os.path.join(self.temp_dir, f"temp_{idx}.mp3")
            
            is_downloaded = os.path.exists(chunk_file_path) and os.path.getsize(chunk_file_path) > 0
            is_failed = status_manager.get_download_status(idx) == 'Thất bại'

            if is_downloaded:
                try:
                    time.sleep(0.2) 
                    segment = AudioSegment.from_mp3(chunk_file_path)
                    combined_audio += segment
                    print(f"-> Đã ghép chunk {idx + 1}/{num_chunks}.")
                    status_manager.update_merge_status(idx, "Đã ghép")
                    self._delete_temp_file(chunk_file_path)
                    files_processed_count += 1
                except Exception as e:
                    error_message = f"Lỗi khi xử lý {chunk_file_path}: {e}"
                    print(error_message)
                    status_manager.update_merge_status(idx, 'Lỗi ghép file', str(e))
                    files_processed_count += 1
            elif is_failed:
                print(f"-> Bỏ qua chunk {idx + 1}/{num_chunks} do lỗi tải về.")
                status_manager.update_merge_status(idx, 'Đã bỏ qua')
                files_processed_count += 1
            else:
                time.sleep(0.5)

        if len(combined_audio) > 0:
            print(f"Đã ghép xong tất cả các chunk. Đang xuất file ra: {final_audio_path}")
            combined_audio.export(final_audio_path, format="mp3")
        else:
            print("Không có audio nào được tạo để ghép.")

    def _delete_temp_file(self, file_path: str):
        """Thử xóa một file tạm với vài lần thử lại."""
        for _ in range(3):
            try:
                os.remove(file_path)
                return
            except OSError:
                time.sleep(0.5)
        print(f"Cảnh báo: Không thể xóa file tạm {file_path}.") 