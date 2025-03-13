
import speech_recognition as sr

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
        # Mở file âm thanh 
        with sr.AudioFile(file_path) as source:
            # Đọc toàn bộ file âm thanh
            audio_data = recognizer.record(source)
            
            try:
                # Thử chuyển giọng nói thành văn bản
                text = recognizer.recognize_google(audio_data, language=language)
                print("Nội dung file âm thanh:")
                print(text)
                return text
            
            except sr.UnknownValueError:
                print("Không thể nhận dạng âm thanh từ file")
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
file_path = r"[FIL20] Practice 10, 11.mp3"
result = speech_to_text_from_file(file_path)
