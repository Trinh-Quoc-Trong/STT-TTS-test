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







B. GIẢI THÍCH "KHẨU QUYẾT CHƠI" CỦA 20 NHÂN VẬT
Elon Musk: "Tốc độ R&D là vũ khí tối thượng."
Ý nghĩa: Trong cuộc chơi công nghệ, ai học hỏi, thử nghiệm và cải tiến nhanh hơn sẽ là người chiến thắng, chứ không phải ai có nhiều tiền hơn hay quy mô lớn hơn lúc đầu. Cuộc chơi được định đoạt bởi gia tốc sáng tạo.
Jeff Bezos: "Luôn là Ngày-1, nếu không bạn sẽ chết."
Ý nghĩa: Hãy luôn giữ tâm thế của một startup vào ngày đầu thành lập: khao khát, ám ảnh về khách hàng và sẵn sàng thử nghiệm. "Ngày-2" là trạng thái của sự tự mãn, trì trệ và suy vong. Cuộc chơi là phải duy trì được tinh thần "Ngày-1" mãi mãi.
Steve Jobs: "Nghệ sĩ thực thụ thì phải ra mắt sản phẩm."
Ý nghĩa: Ý tưởng dù có hay đến đâu cũng vô giá trị nếu không được thực thi và đưa ra thế giới. "Chiến thắng" là tạo ra một sản phẩm có sức ảnh hưởng, chứ không phải giữ một ý tưởng hoàn hảo trên giấy.
Kobe Bryant: "Tinh thần Mamba – hôm nay phải hơn hôm qua."
Ý nghĩa: Tập trung không ngừng nghỉ vào việc hoàn thiện bản thân. Đối thủ lớn nhất không phải đội khác, mà là chính bạn của ngày hôm qua. Cuộc chơi là một chuỗi nhiệm vụ hàng ngày để đạt đến sự tinh thông.
Michael Jordan: "Tôi cạnh tranh với chính tiềm năng của mình."
Ý nghĩa: Tương tự Kobe, thước đo thành công cuối cùng là liệu bạn có phát huy hết 100% tiềm năng của mình hay không. Chức vô địch chỉ là kết quả của việc chiến thắng trong cuộc chơi nội tâm này.
Serena Williams: "Tiến hóa hoặc biến mất."
Ý nghĩa: Trong một môi trường cạnh tranh khốc liệt, đứng yên đồng nghĩa với tụt lùi. Bạn phải liên tục thích nghi kỹ năng, chiến lược và tư duy để giữ vững đỉnh cao. Cuộc chơi là sự tiến hóa không ngừng.
Warren Buffett: "Bảng điểm nội tại đánh bại tiếng vỗ tay bên ngoài."
Ý nghĩa: Nguyên tắc và sự phán đoán của riêng bạn quan trọng hơn ý kiến đám đông hay biến động thị trường. Chiến thắng là khi bạn trung thành với lý trí của mình, bất chấp sự tung hô hay chê bai từ bên ngoài.
Charlie Munger: "Đọc 500 trang mỗi ngày – lãi kép cho não bộ."
Ý nghĩa: Tri thức có sức mạnh của lãi kép. Cuộc chơi là một quá trình tích lũy trí tuệ lâu dài, thứ sẽ cho bạn một lợi thế không thể bị sao chép.
Naval Ravikant: "Kiếm tiền bằng đòn bẩy, chơi những ván lặp lại."
Ý nghĩa: Hãy xây dựng các hệ thống (code, media, vốn) có thể làm việc thay bạn. Tham gia vào các mối quan hệ và lĩnh vực mà ở đó uy tín và danh tiếng được bồi đắp qua thời gian, mang lại lợi íchทบซ้อน. Đừng chơi những ván ăn thua một lần rồi thôi.
Ray Dalio: "Đau đớn + Suy ngẫm = Tiến bộ."
Ý nghĩa: Thất bại và sai lầm không phải là bước lùi, mà là dữ liệu quý giá. Hãy phân tích chúng một cách khách quan để rút ra bài học. Đây là vòng lặp cốt lõi để "lên level" trong cuộc chơi.
Satya Nadella: "Luôn-học-hỏi quan trọng hơn là Biết-tuốt."
Ý nghĩa: Một văn hóa "luôn học hỏi" sẽ cởi mở với ý tưởng mới và không ngừng phát triển. Một văn hóa "biết tuốt" sẽ tự mãn và trì trệ. Cuộc chơi được thắng bởi tổ chức nào học nhanh nhất.
Richard Branson: "Kệ nó, làm tới đi."
Ý nghĩa: Thể hiện tinh thần ưu tiên hành động, sẵn sàng chấp nhận rủi ro có tính toán cho những cuộc phiêu lưu mới. Đừng để việc phân tích quá mức làm bạn tê liệt.
Phil Knight (Nike): "Không có vạch đích nào cả."
Ý nghĩa: Cuộc đua đến sự xuất sắc là vô tận. Khi bạn đạt được một mục tiêu, ngay lập tức hãy đặt ra một mục tiêu mới cao hơn. Đây là một cuộc chơi vô hạn về việc phá vỡ các giới hạn.
Sam Altman: "Tham vọng phải lớn hơn nguồn lực."
Ý nghĩa: Những mục tiêu vĩ đại buộc bạn phải sáng tạo và xoay xở. Nếu tham vọng bị giới hạn bởi nguồn lực hiện tại, bạn sẽ không bao giờ đạt được kết quả đột phá (10x).
Yvon Chouinard (Patagonia): "Trái Đất là cổ đông duy nhất của chúng tôi."
Ý nghĩa: Mục đích tối thượng của công ty không phải là lợi nhuận cho cổ đông, mà là phục vụ một lý tưởng cao cả hơn (hành tinh). Điều này định nghĩa "điều kiện chiến thắng" của họ.
Tim Grover: "Chiến thắng trong những giờ không ai thấy."
Ý nghĩa: Vinh quang thực sự được tạo nên từ những giờ luyện tập không ngừng nghỉ, không hào nhoáng và không ai chứng kiến. Màn trình diễn trước công chúng chỉ là kết quả của công sức bỏ ra trong bóng tối.
Jack Ma: "Hôm nay khó khăn, ngày mai còn khó khăn hơn, nhưng ngày kia sẽ là ngày nắng đẹp."
Ý nghĩa: Nhấn mạnh sự kiên cường và tầm nhìn dài hạn. Con đường của người kiến tạo đầy rẫy thử thách, nhưng sự bền bỉ sẽ dẫn đến thành công cuối cùng. Đây là một cuộc chơi của sức bền.
Oprah Winfrey: "Sự xuất sắc là biện pháp răn đe tốt nhất cho nạn phân biệt chủng tộc hay giới tính."
Ý nghĩa: Cách tối thượng để vượt qua định kiến và các rào cản bên ngoài là trở nên giỏi đến mức không thể bị phớt lờ. Chiến thắng là đạt được sự tinh thông như một hình thức khẳng định sức mạnh.
Howard Schultz: "Hãy rót cả trái tim mình vào trong tách cà phê."
Ý nghĩa: Đam mê và cam kết với chất lượng trong từng chi tiết nhỏ nhất là thứ tạo nên một sản phẩm và thương hiệu vĩ đại. Cuộc chơi được thắng bằng sự tận tâm với chính công việc.
Angela Merkel: "Chúng ta làm được mà."
Ý nghĩa: Một tuyên ngôn về năng lực tự quyết tập thể. Đó là niềm tin rằng bất chấp những thách thức to lớn, một nhóm (hay một quốc gia) có đủ khả năng để vượt qua.
C. GIẢI THÍCH NGUYÊN TẮC VẬN HÀNH CỦA 20 CÔNG TY
Google: OKR + "Gấp 10 lần chứ không phải 10%".
Ý nghĩa: Đặt ra những mục tiêu tham vọng, có thể đo lường (OKR) nhằm tạo ra sự đột phá (10x), thay vì chỉ cải tiến nhỏ (10%). Điều này buộc tổ chức phải tư duy lại vấn đề từ gốc rễ.
Amazon: "Làm việc ngược từ tương lai", "Tư duy Ngày-1".
Ý nghĩa: Bắt đầu bằng việc hình dung trải nghiệm khách hàng lý tưởng rồi mới xây dựng sản phẩm. Kết hợp điều này với tinh thần "Ngày-1" (khẩn trương, ám ảnh khách hàng) để luôn dẫn đầu.
Tesla/SpaceX: "Tư duy từ nguyên tắc gốc", "Thử nghiệm mẫu thất bại-nhanh-rẻ".
Ý nghĩa: Phân rã một vấn đề về các định luật vật lý cơ bản nhất, không dựa trên các giả định có sẵn. Sau đó, nhanh chóng thử nghiệm các nguyên mẫu rẻ tiền để học hỏi, làm cho vòng lặp đổi mới cực nhanh.
Apple: "Tuyệt vời đến điên rồ" – chất lượng quyết định chiến thắng.
Ý nghĩa: Điều kiện "chiến thắng" được định nghĩa bằng việc tạo ra sản phẩm có chất lượng và trải nghiệm người dùng xuất sắc đến mức nó trở thành tiêu chuẩn của ngành và truyền cảm hứng cho lòng trung thành sâu sắc.
Netflix: "Tự do & Trách nhiệm" + "Bài kiểm tra giữ người".
Ý nghĩa: Thuê những người giỏi nhất, trao cho họ sự tự do tối đa và yêu cầu hiệu suất cao. "Bài kiểm tra giữ người" hỏi các quản lý: "Bạn có đấu tranh để giữ người này lại không?". Điều này đảm bảo đội ngũ luôn là những "người chơi hạng A".
Spotify: "Mô hình Biệt đội - Bộ lạc" – đề cao sự tự chủ.
Ý nghĩa: Tổ chức thành các đội nhỏ, tự chủ ("Biệt đội") chịu trách nhiệm từ đầu đến cuối cho một tính năng. Mô hình này tối đa hóa tốc độ, quyền sở hữu và sự đổi mới, giống như các nhóm nhỏ tấn công các phần khác nhau của bản đồ game.
Valve: "Bàn làm việc có bánh xe" – tự do chọn dự án.
Ý nghĩa: Một cấu trúc phẳng nơi nhân viên tự chọn dự án họ tin rằng sẽ tạo ra nhiều giá trị nhất. Quyền lực và tài nguyên chảy một cách tự nhiên đến những "nhiệm vụ" hứa hẹn nhất.
Toyota: "Kaizen", "Dây kéo Andon" – tạm dừng cuộc chơi khi có lỗi.
Ý nghĩa: Một văn hóa cải tiến liên tục từ tất cả mọi người. Trao quyền cho bất kỳ công nhân nào được "kéo dây" để dừng dây chuyền sản xuất và sửa lỗi ngay lập tức. Điều này đảm bảo chất lượng được tích hợp sẵn, không phải chỉ kiểm tra ở cuối.
Patagonia: "Sứ mệnh trên lợi nhuận", "Cuộc chơi vô hạn vì hành tinh".
Ý nghĩa: Kinh doanh là một công cụ để đạt được sứ mệnh: cứu lấy hành tinh. Lợi nhuận là cần thiết để duy trì cuộc chơi, nhưng nó không phải là mục tiêu cuối cùng. "Chiến thắng" là tác động tích cực đến môi trường.
Nike: "Cứ làm đi" – hành động chính là cuộc chơi.
Ý nghĩa: Cổ vũ tinh thần hành động và trao quyền cho cá nhân để họ chủ động. Đó là lời kêu gọi hãy bước vào sân đấu và cạnh tranh, thay vì chỉ đứng xem.
Microsoft (dưới thời Nadella): "Doanh nghiệp với tư duy tăng trưởng".
Ý nghĩa: Chuyển toàn bộ văn hóa công ty từ "tư duy cố định" (bảo vệ các sản phẩm cũ) sang "tư duy tăng trưởng" (học hỏi, hợp tác và khám phá những lĩnh vực mới). Cuộc chơi chuyển từ phòng thủ sang thám hiểm.
Atlassian: "Công ty mở, không nói nhảm."
Ý nghĩa: Cam kết về sự minh bạch và giao tiếp thẳng thắn. Điều này tăng tốc độ ra quyết định và xây dựng lòng tin, rất cần thiết cho một cuộc chơi đồng đội hiệu suất cao.
Samsung: "Tinh thần tiên phong" – chinh phục trận địa mới mỗi thập kỷ.
Ý nghĩa: Sẵn sàng tham gia và cạnh tranh trong các ngành công nghiệp mới và khó khăn. Cuộc chơi là liên tục tìm kiếm và chinh phục các lãnh thổ mới.
Tencent: "Kết nối là dịch vụ" – mở rộng bản đồ hệ sinh thái.
Ý nghĩa: Chiến lược cốt lõi là xây dựng một hệ sinh thái dịch vụ rộng lớn, kết nối với nhau (mạng xã hội, game, thanh toán) để tạo ra giá trị khổng lồ và giữ chân người dùng. "Chiến thắng" là sở hữu toàn bộ bản đồ game.
Pixar: "Phản hồi từ Hội đồng tinh hoa" – demo sớm, sửa sớm.
Ý nghĩa: Một quy trình cốt lõi nơi một nhóm các nhà lãnh đạo sáng tạo đáng tin cậy (Braintrust) đưa ra phản hồi thẳng thắn, mang tính xây dựng về các bộ phim đang trong giai đoạn phát triển ban đầu. Việc này giúp tìm và sửa các vấn đề về câu chuyện từ sớm, làm cho sản phẩm cuối cùng mạnh mẽ hơn.
Airbnb: "Thuộc về bất cứ đâu" – cuộc chơi vô hạn trong ngành khách sạn.
Ý nghĩa: Sứ mệnh không chỉ là cho thuê phòng, mà là tạo ra một thế giới nơi mọi người có thể cảm thấy thân thuộc ở bất cứ đâu. Đây là một cuộc chơi vô hạn, có mục đích, vượt ra ngoài bản chất giao dịch của ngành khách sạn.
3M: "15% thời gian cho nhiệm vụ phụ".
Ý nghĩa: Cho phép các kỹ sư dành một phần thời gian của họ cho các dự án đam mê cá nhân. Điều này khuyến khích thử nghiệm và là nguồn gốc của nhiều đột phá lớn nhất của 3M (như giấy ghi chú Post-it).
Dropbox: "Chúng tôi giải quyết vấn đề nhanh chóng" – văn hoá ra mắt sản phẩm.
Ý nghĩa: Ưu tiên thực thi và cung cấp giải pháp cho các vấn đề của khách hàng hơn là thảo luận vô tận. "Chiến thắng" là đưa được bản sửa lỗi đến tay người dùng.
Haier (Rendanheyi): Mỗi "doanh nghiệp siêu nhỏ" là một "người chơi con" tự kiếm điểm.
Ý nghĩa: Chia nhỏ tập đoàn thành hàng trăm đơn vị độc lập, hoạt động như các startup nhỏ. Họ trực tiếp làm việc với khách hàng và tự chịu trách nhiệm về doanh thu, lợi nhuận của mình. Điều này biến toàn bộ tổ chức thành một trò chơi khởi nghiệp nhiều người chơi quy mô lớn.
Hàng không Southwest: "Muốn đi trốn không?" – vui vẻ và chi phí thấp sẽ thắng đường dài.
Ý nghĩa: Chiến lược là thắng một cuộc chơi cụ thể: du lịch giá rẻ. Họ đạt được điều này với một văn hóa vui vẻ, lấy nhân viên làm trung tâm, từ đó thúc đẩy hiệu quả và lòng trung thành của khách hàng. Họ chứng minh rằng bạn có thể thắng cuộc chơi đường dài bằng cách vừa rẻ vừa vui.








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

def progressive_merger(temp_dir, num_chunks, final_audio_path):
    """
    Theo dõi và ghép các file audio ngay khi chúng sẵn sàng theo đúng thứ tự.
    Chạy trong một luồng riêng.
    """
    print("Tiến trình ghép file bắt đầu chạy song song.")
    combined_audio = AudioSegment.empty()
    files_merged_count = 0
    
    # Vòng lặp sẽ tiếp tục cho đến khi tất cả các chunk được ghép
    while files_merged_count < num_chunks:
        chunk_file_path = os.path.join(temp_dir, f"temp_{files_merged_count}.mp3")
        
        # Chờ file tiếp theo trong chuỗi xuất hiện và có nội dung
        if os.path.exists(chunk_file_path) and os.path.getsize(chunk_file_path) > 0:
            try:
                # Đợi một chút để đảm bảo file đã được ghi xong hoàn toàn
                time.sleep(0.2) 
                segment = AudioSegment.from_mp3(chunk_file_path)
                combined_audio += segment
                print(f"-> Đã ghép xong chunk {files_merged_count + 1}/{num_chunks}.")
                
                # Xóa file tạm ngay sau khi ghép
                try:
                    os.remove(chunk_file_path)
                except OSError as e:
                    print(f"Lỗi khi xóa file tạm {chunk_file_path}: {e}")

                files_merged_count += 1
            except Exception as e:
                # Có thể file đang được ghi dở, hoặc bị lỗi. Đợi và thử lại.
                print(f"Lỗi khi xử lý file {chunk_file_path}: {e}. Sẽ thử lại sau giây lát.")
                time.sleep(1)
        else:
            # File chưa sẵn sàng, đợi một chút rồi kiểm tra lại
            time.sleep(0.5)

    # Lưu file cuối cùng khi đã ghép tất cả
    if len(combined_audio) > 0:
        print(f"Đã ghép xong tất cả. Lưu file vào: {final_audio_path}")
        combined_audio.export(final_audio_path, format="mp3")
    else:
        print("Không có file audio nào được tạo ra để ghép.")

def cleanup(temp_dir):
    """Dọn dẹp thư mục tạm sau khi quá trình hoàn tất."""
    print("Bắt đầu dọn dẹp...")
    if not os.path.exists(temp_dir):
        print("Thư mục tạm không tồn tại, không cần dọn dẹp.")
        return
        
    # Các file con đã được luồng ghép xóa. Thư mục giờ đây phải rỗng.
    try:
        if len(os.listdir(temp_dir)) > 0:
            print(f"Cảnh báo: Vẫn còn file trong thư mục tạm {temp_dir}. Sẽ không xóa thư mục.")
        else:
            os.rmdir(temp_dir)
            print(f"Đã xóa thành công thư mục tạm: {temp_dir}")
    except OSError as e:
        print(f"Lỗi khi xóa thư mục tạm {temp_dir}: {e}.")

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

    # Điều chỉnh số luồng nếu số chunk ít hơn
    actual_num_threads = len(text_chunks)
    
    print(f"Bắt đầu xử lý {actual_num_threads} chunk văn bản với {actual_num_threads} luồng...")

    # Bắt đầu luồng ghép file chạy nền
    merger_thread = threading.Thread(
        target=progressive_merger, 
        args=(temp_dir, actual_num_threads, final_audio_path)
    )
    merger_thread.start()

    # Tạo và bắt đầu các luồng tải về
    threads = []
    for i in range(actual_num_threads):
        thread = threading.Thread(target=text_to_audio_chunk, args=(text_chunks[i], i, language_, temp_dir))
        threads.append(thread)
        thread.start()

    # Đợi tất cả các luồng tải về hoàn thành
    for thread in threads:
        thread.join()
    print("Tất cả các luồng tải về đã hoàn thành.")

    # Đợi luồng ghép file hoàn thành công việc của nó
    merger_thread.join()
    print("Tiến trình ghép file đã kết thúc.")
    
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

