# -*- coding: utf-8 -*-
# <(6O9)>  
import os
from gtts import gTTS
import threading
from pydub import AudioSegment # Cần cài đặt: pip install pydub
import time
import math

# LƯU Ý: pydub yêu cầu ffmpeg để xử lý file MP3. 
# Bạn cần tải và cài đặt ffmpeg, sau đó thêm nó vào PATH của hệ thống.
# Hướng dẫn có thể tìm thấy trên mạng, ví dụ: https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/

# --- CẤU HÌNH ---
# Luôn cố gắng tạo 10 luồng, trừ khi văn bản quá ngắn (<50 từ)
NUM_THREADS = 10
DELAY_BETWEEN_REQUESTS = 2 # Giây. Tăng giá trị này nếu vẫn gặp lỗi 429.
# -----------------

language_ = "vi"
text = (
r"""



Nó Có Hại Như Thế Nào?
Sự trì hoãn không chỉ đơn giản là một thói quen xấu, nó có thể gây ra những tác động tiêu cực nghiêm trọng và lan rộng đến nhiều khía cạnh của cuộc sống:
1. Ảnh hưởng đến hiệu suất và sự nghiệp:
Chất lượng công việc kém: Làm việc vội vã vào phút chót hiếm khi tạo ra kết quả tốt nhất.
Bỏ lỡ cơ hội: Bạn có thể bỏ lỡ các cơ hội thăng tiến hoặc học hỏi vì không hoàn thành nhiệm vụ đúng hạn.
Tổn hại danh tiếng: Việc liên tục trễ deadline hoặc giao sản phẩm kém chất lượng sẽ khiến đồng nghiệp và cấp trên mất lòng tin vào bạn.
2. Hủy hoại sức khỏe tinh thần:
Tăng mức độ căng thẳng (stress) và lo âu (anxiety): Áp lực của deadline đang đến gần gây ra sự căng thẳng cực độ.
Cảm giác tội lỗi và xấu hổ: Sau khi trì hoãn, bạn thường cảm thấy tội lỗi vì đã không làm việc, dẫn đến lòng tự trọng thấp.
Tạo ra vòng lặp tiêu cực: Bạn cảm thấy tồi tệ -> bạn trì hoãn để né tránh cảm giác tồi tệ -> bạn lại càng cảm thấy tồi tệ hơn. Đây là một cái bẫy rất khó thoát ra.
3. Gây hại cho sức khỏe thể chất:
Sự căng thẳng mãn tính do trì hoãn có thể dẫn đến các vấn đề sức khỏe như mất ngủ, cao huyết áp, và hệ miễn dịch suy yếu.
Mọi người cũng thường trì hoãn các hành động liên quan đến sức khỏe như đi khám bác sĩ, tập thể dục, hoặc ăn uống lành mạnh, dẫn đến hậu quả lâu dài.
4. Vấn đề về tài chính và các mối quan hệ:
Trì hoãn việc trả hóa đơn có thể dẫn đến phí phạt. Trì hoãn việc lên kế hoạch tài chính có thể khiến bạn mất đi các cơ hội đầu tư.
Trong các mối quan hệ, việc trì hoãn những cuộc trò chuyện quan trọng hoặc không thực hiện lời hứa có thể gây ra xung đột và làm tổn thương người khác.
Tóm lại, thói quen trì hoãn là một cơ chế đối phó ngắn hạn với cảm xúc tiêu cực nhưng lại gây ra những hậu quả vô cùng tai hại trong dài hạn.





"""
)

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


def text_to_audio_chunk(text_chunk, index, language, temp_dir):
    """Chuyển một đoạn văn bản thành file audio và lưu vào thư mục tạm."""
    try:
        if not text_chunk:
            print(f"Luồng {index}: Không có văn bản để xử lý.")
            return

        # Dàn cách các yêu cầu để tránh bị giới hạn tốc độ (rate limiting)
        sleep_time = index * DELAY_BETWEEN_REQUESTS
        if sleep_time > 0:
            print(f"Luồng {index}: Đang chờ {sleep_time} giây...")
            time.sleep(sleep_time)
            
        temp_file_path = os.path.join(temp_dir, f"temp_{index}.mp3")
        print(f"Luồng {index}: Đang gửi yêu cầu tới API...")
        tts = gTTS(text=text_chunk, lang=language, slow=False)
        tts.save(temp_file_path)
        print(f"Luồng {index}: Đã lưu chunk vào {temp_file_path}")
    except Exception as e:
        print(f"Lỗi trong luồng {index}: {e}")

def cleanup(temp_dir, num_files):
    """Dọn dẹp các file tạm và thư mục tạm."""
    print("Bắt đầu dọn dẹp file tạm...")
    for i in range(num_files):
        temp_file_path = os.path.join(temp_dir, f"temp_{i}.mp3")
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError as e:
                print(f"Lỗi khi xóa file tạm {temp_file_path}: {e}")
    
    try:
        os.rmdir(temp_dir)
        print(f"Đã xóa thư mục tạm: {temp_dir}")
    except OSError as e:
        print(f"Lỗi khi xóa thư mục tạm {temp_dir}: {e}. Có thể do thư mục không rỗng.")

def main():
    """Hàm chính điều phối việc chia văn bản, xử lý đa luồng, ghép file và phát âm thanh."""
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

    # Điều chỉnh số luồng nếu số chunk ít hơn
    actual_num_threads = len(text_chunks)
    threads = []

    print(f"Bắt đầu xử lý {actual_num_threads} chunk văn bản với {actual_num_threads} luồng...")
    # Tạo và bắt đầu các luồng
    for i in range(actual_num_threads):
        thread = threading.Thread(target=text_to_audio_chunk, args=(text_chunks[i], i, language_, temp_dir))
        threads.append(thread)
        thread.start()

    # Đợi tất cả các luồng hoàn thành
    for i, thread in enumerate(threads):
        thread.join()
    print("Tất cả các luồng đã hoàn thành.")

    # Ghép các file audio lại
    print("Bắt đầu ghép các file audio...")
    combined_audio = AudioSegment.empty()
    try:
        for i in range(actual_num_threads):
            chunk_file_path = os.path.join(temp_dir, f"temp_{i}.mp3")
            if os.path.exists(chunk_file_path) and os.path.getsize(chunk_file_path) > 0:
                segment = AudioSegment.from_mp3(chunk_file_path)
                combined_audio += segment
                print(f"Đã ghép file: {chunk_file_path}")
    except Exception as e:
        print(f"Lỗi khi đang ghép file audio: {e}")
        # Dọn dẹp và thoát nếu có lỗi
        cleanup(temp_dir, actual_num_threads)
        return

    if len(combined_audio) > 0:
        print(f"Đã ghép xong. Lưu file vào: {final_audio_path}")
        combined_audio.export(final_audio_path, format="mp3")
        
        # Phát file
        print("Đang mở file audio...")
        os.startfile(final_audio_path)
    else:
        print("Không có file audio nào được tạo ra.")

    # Dọn dẹp file và thư mục tạm
    cleanup(temp_dir, actual_num_threads)


if __name__ == "__main__":
    main()

