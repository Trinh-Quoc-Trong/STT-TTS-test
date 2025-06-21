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







B. GIẢI THÍCH “KHẨU QUYẾT CHƠI” CỦA 20 NHÂN VẬT
Elon Musk: “Tốc độ R&D là vũ khí tối thượng.”
Ý nghĩa: Trong cuộc chơi công nghệ, ai học hỏi, thử nghiệm và cải tiến nhanh hơn sẽ là người chiến thắng, chứ không phải ai có nhiều tiền hơn hay quy mô lớn hơn lúc đầu. Cuộc chơi được định đoạt bởi gia tốc sáng tạo.
Jeff Bezos: “Luôn là Ngày-1, nếu không bạn sẽ chết.”
Ý nghĩa: Hãy luôn giữ tâm thế của một startup vào ngày đầu thành lập: khao khát, ám ảnh về khách hàng và sẵn sàng thử nghiệm. "Ngày-2" là trạng thái của sự tự mãn, trì trệ và suy vong. Cuộc chơi là phải duy trì được tinh thần "Ngày-1" mãi mãi.
Steve Jobs: “Nghệ sĩ thực thụ thì phải ra mắt sản phẩm.”
Ý nghĩa: Ý tưởng dù có hay đến đâu cũng vô giá trị nếu không được thực thi và đưa ra thế giới. "Chiến thắng" là tạo ra một sản phẩm có sức ảnh hưởng, chứ không phải giữ một ý tưởng hoàn hảo trên giấy.
Kobe Bryant: “Tinh thần Mamba – hôm nay phải hơn hôm qua.”
Ý nghĩa: Tập trung không ngừng nghỉ vào việc hoàn thiện bản thân. Đối thủ lớn nhất không phải đội khác, mà là chính bạn của ngày hôm qua. Cuộc chơi là một chuỗi nhiệm vụ hàng ngày để đạt đến sự tinh thông.
Michael Jordan: “Tôi cạnh tranh với chính tiềm năng của mình.”
Ý nghĩa: Tương tự Kobe, thước đo thành công cuối cùng là liệu bạn có phát huy hết 100% tiềm năng của mình hay không. Chức vô địch chỉ là kết quả của việc chiến thắng trong cuộc chơi nội tâm này.
Serena Williams: “Tiến hóa hoặc biến mất.”
Ý nghĩa: Trong một môi trường cạnh tranh khốc liệt, đứng yên đồng nghĩa với tụt lùi. Bạn phải liên tục thích nghi kỹ năng, chiến lược và tư duy để giữ vững đỉnh cao. Cuộc chơi là sự tiến hóa không ngừng.
Warren Buffett: “Bảng điểm nội tại đánh bại tiếng vỗ tay bên ngoài.”
Ý nghĩa: Nguyên tắc và sự phán đoán của riêng bạn quan trọng hơn ý kiến đám đông hay biến động thị trường. Chiến thắng là khi bạn trung thành với lý trí của mình, bất chấp sự tung hô hay chê bai từ bên ngoài.
Charlie Munger: “Đọc 500 trang mỗi ngày – lãi kép cho não bộ.”
Ý nghĩa: Tri thức có sức mạnh của lãi kép. Cuộc chơi là một quá trình tích lũy trí tuệ lâu dài, thứ sẽ cho bạn một lợi thế không thể bị sao chép.
Naval Ravikant: “Kiếm tiền bằng đòn bẩy, chơi những ván lặp lại.”
Ý nghĩa: Hãy xây dựng các hệ thống (code, media, vốn) có thể làm việc thay bạn. Tham gia vào các mối quan hệ và lĩnh vực mà ở đó uy tín và danh tiếng được bồi đắp qua thời gian, mang lại lợi íchทบซ้อน. Đừng chơi những ván ăn thua một lần rồi thôi.
Ray Dalio: “Đau đớn + Suy ngẫm = Tiến bộ.”
Ý nghĩa: Thất bại và sai lầm không phải là bước lùi, mà là dữ liệu quý giá. Hãy phân tích chúng một cách khách quan để rút ra bài học. Đây là vòng lặp cốt lõi để "lên level" trong cuộc chơi.
Satya Nadella: “Luôn-học-hỏi quan trọng hơn là Biết-tuốt.”
Ý nghĩa: Một văn hóa "luôn học hỏi" sẽ cởi mở với ý tưởng mới và không ngừng phát triển. Một văn hóa "biết tuốt" sẽ tự mãn và trì trệ. Cuộc chơi được thắng bởi tổ chức nào học nhanh nhất.
Richard Branson: “Kệ nó, làm tới đi.”
Ý nghĩa: Thể hiện tinh thần ưu tiên hành động, sẵn sàng chấp nhận rủi ro có tính toán cho những cuộc phiêu lưu mới. Đừng để việc phân tích quá mức làm bạn tê liệt.
Phil Knight (Nike): “Không có vạch đích nào cả.”
Ý nghĩa: Cuộc đua đến sự xuất sắc là vô tận. Khi bạn đạt được một mục tiêu, ngay lập tức hãy đặt ra một mục tiêu mới cao hơn. Đây là một cuộc chơi vô hạn về việc phá vỡ các giới hạn.
Sam Altman: “Tham vọng phải lớn hơn nguồn lực.”
Ý nghĩa: Những mục tiêu vĩ đại buộc bạn phải sáng tạo và xoay xở. Nếu tham vọng bị giới hạn bởi nguồn lực hiện tại, bạn sẽ không bao giờ đạt được kết quả đột phá (10x).
Yvon Chouinard (Patagonia): “Trái Đất là cổ đông duy nhất của chúng tôi.”




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

