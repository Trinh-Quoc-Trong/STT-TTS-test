import speech_recognition as sr
import os
from pydub import AudioSegment
import tempfile

def speech_to_text_from_file(file_path, language="vi-VN"):
    """
    Chuyển đổi file âm thanh (MP3) thành văn bản
    
    Args:
        file_path (str): Đường dẫn tới file MP3
        language (str, optional): Ngôn ngữ nhận dạng. Mặc định là tiếng Việt.
    
    Returns:
        str: Văn bản được nhận dạng từ file âm thanh
    """
    # Khởi tạo recognizer
    recognizer = sr.Recognizer()
    
    try:
        # Kiểm tra định dạng file
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.mp3':
            print(f"Đang chuyển đổi file MP3 sang WAV...")
            # Tạo temporary file
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_wav.close()
            
            # Chuyển đổi MP3 sang WAV
            sound = AudioSegment.from_mp3(file_path)
            sound.export(temp_wav.name, format="wav")
            
            # Cập nhật đường dẫn file
            audio_file_path = temp_wav.name
            print(f"Đã chuyển đổi sang {audio_file_path}")
        else:
            audio_file_path = file_path
        
        # Mở file âm thanh 
        with sr.AudioFile(audio_file_path) as source:
            # Đọc toàn bộ file âm thanh
            audio_data = recognizer.record(source)
            
            try:
                # Thử chuyển giọng nói thành văn bản
                text = recognizer.recognize_google(audio_data, language=language)
                print("Nội dung file âm thanh:")
                print(text)
                
                # Xóa temp file nếu đã tạo
                if file_ext == '.mp3' and os.path.exists(temp_wav.name):
                    os.unlink(temp_wav.name)
                    
                return text
            
            except sr.UnknownValueError:
                print("Không thể nhận dạng âm thanh từ file.")
                return None
            
            except sr.RequestError as e:
                print(f"Lỗi kết nối với dịch vụ nhận dạng giọng nói: {e}")
                return None
    
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        return None
    
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        return None

# Ví dụ sử dụng
file_path = r"D:\code\phanMemDoc\[TE] L15_Practice 2.mp3"
result = speech_to_text_from_file(file_path)
