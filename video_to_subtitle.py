import os
import sys
from moviepy.video.io.VideoFileClip import VideoFileClip # Cú pháp mới cho MoviePy 2.0+
import whisper
import warnings

# Tắt cảnh báo của ffmpeg (nếu có) từ moviepy
warnings.filterwarnings("ignore", category=UserWarning, module="moviepy")

def extract_audio(input_path: str, output_audio_path: str) -> str:
    """
    Trích xuất âm thanh từ file video hoặc trả về đường dẫn file nếu đã là âm thanh.
    Hỗ trợ các định dạng video phổ biến (.mp4, .avi, .mkv, .mov, .flv, .wmv)
    và các định dạng âm thanh phổ biến (.mp3, .wav, .aac, .flac, .ogg).
    """
    if not os.path.exists(input_path):
        print(f"Lỗi: Không tìm thấy file đầu vào tại '{input_path}'")
        sys.exit(1)

    # Các định dạng video và âm thanh phổ biến
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm']
    audio_extensions = ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a']

    file_extension = os.path.splitext(input_path)[1].lower()

    if file_extension in audio_extensions:
        print(f"File đầu vào đã là file âm thanh ({file_extension}). Bỏ qua bước trích xuất.")
        return input_path
    elif file_extension in video_extensions:
        print(f"Trích xuất âm thanh từ video: '{input_path}'...")
        try:
            video = VideoFileClip(input_path)
            audio = video.audio
            audio.write_audiofile(output_audio_path, logger=None) # logger=None để tắt log của moviepy
            video.close() # Đảm bảo giải phóng tài nguyên
            print(f"Đã trích xuất âm thanh thành công vào: '{output_audio_path}'")
            return output_audio_path
        except Exception as e:
            print(f"Lỗi khi trích xuất âm thanh: {e}")
            sys.exit(1)
    else:
        print(f"Lỗi: Định dạng file '{file_extension}' không được hỗ trợ. Vui lòng cung cấp file video hoặc audio.")
        sys.exit(1)

def transcribe_audio(audio_path: str, model_name: str = "base") -> str:
    """
    Chuyển đổi file âm thanh thành văn bản sử dụng mô hình Whisper.
    Các model có sẵn: 'tiny', 'base', 'small', 'medium', 'large'.
    Chọn 'base' là mặc định cho sự cân bằng giữa tốc độ và độ chính xác.
    Để có độ chính xác cao nhất, hãy thử 'large'.
    """
    if not os.path.exists(audio_path):
        print(f"Lỗi: Không tìm thấy file âm thanh để chuyển đổi tại '{audio_path}'")
        sys.exit(1)

    print(f"Đang tải mô hình Whisper '{model_name}' (có thể mất một lúc nếu lần đầu tiên)...")
    try:
        model = whisper.load_model(model_name)
    except Exception as e:
        print(f"Lỗi khi tải mô hình Whisper: {e}")
        print("Vui lòng đảm bảo bạn đã cài đặt PyTorch và Whisper đúng cách.")
        sys.exit(1)

    print(f"Bắt đầu chuyển đổi âm thanh thành văn bản từ '{audio_path}'...")
    try:
        result = model.transcribe(audio_path)
        print("Chuyển đổi hoàn tất.")
        return result["text"]
    except Exception as e:
        print(f"Lỗi khi chuyển đổi âm thanh: {e}")
        sys.exit(1)

def main():
    # Ví dụ sử dụng: Thay đổi đường dẫn tới file video/audio của bạn
    INPUT_FILE = r"audio\tests\iLoveYt.net_YouTube_Cu-danh-Cuoc-Doi_Media_3uctnEEyiMQ_002_360p.mp4" # <--- ĐIỀN ĐƯỜNG DẪN FILE CỦA BẠN VÀO ĐÂY
    
    # if len(sys.argv) < 2:
    #     print("Cách sử dụng: python video_to_subtitle.py <đường_dẫn_tới_file_video_hoặc_audio>")
    #     sys.exit(1)

    # input_file = sys.argv[1]
    input_file = INPUT_FILE # Sử dụng biến INPUT_FILE đã khai báo
    
    # Đặt tên file âm thanh tạm thời
    output_audio_file = os.path.join(os.path.dirname(input_file), f"extracted_audio_{os.path.basename(os.path.splitext(input_file)[0])}.mp3")
    
    # Bước 1: Trích xuất âm thanh
    audio_for_transcription = extract_audio(input_file, output_audio_file)

    # Bước 2: Chuyển đổi âm thanh thành văn bản
    # Bạn có thể thay đổi "base" thành "small", "medium", "large" tùy thuộc vào yêu cầu độ chính xác và tài nguyên máy.
    # "large" là chính xác nhất nhưng yêu cầu nhiều RAM và thời gian xử lý hơn.
    transcribed_text = transcribe_audio(audio_for_transcription, model_name="base")

    print("\n--- KẾT QUẢ PHỤ ĐỀ ---\n")
    print(transcribed_text)

    # Dọn dẹp file âm thanh tạm thời nếu nó được tạo ra từ video
    if input_file != audio_for_transcription and os.path.exists(audio_for_transcription):
        try:
            os.remove(audio_for_transcription)
            print(f"Đã xóa file âm thanh tạm thời: '{audio_for_transcription}'")
        except Exception as e:
            print(f"Cảnh báo: Không thể xóa file âm thanh tạm thời '{audio_for_transcription}': {e}")

if __name__ == "__main__":
    main() 