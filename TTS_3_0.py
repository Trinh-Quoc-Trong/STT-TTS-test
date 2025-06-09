# -*- coding: utf-8 -*-
# <(6O9)>  
import os
from gtts import gTTS
import threading
from pydub import AudioSegment # Cần cài đặt: pip install pydub

# LƯU Ý: pydub yêu cầu ffmpeg để xử lý file MP3. 
# Bạn cần tải và cài đặt ffmpeg, sau đó thêm nó vào PATH của hệ thống.
# Hướng dẫn có thể tìm thấy trên mạng, ví dụ: https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/

language_ = "vi"
text = (
r"""

Báo cáo chuyên sâu: Khơi dậy hứng thú và nhận diện dấu hiệu nghiện hành vi
I. Giới thiệu: Hành trình khám phá động lực và sự gắn kết

Hứng thú và ham muốn là những yếu tố then chốt định hình hành vi và trải nghiệm của con người, đóng vai trò là động lực cơ bản thúc đẩy sự học hỏi, phát triển và đạt được mục tiêu. Sự hiện diện của hứng thú và ham muốn lành mạnh không chỉ mang lại niềm vui, sự thỏa mãn mà còn là nguồn năng lượng tinh thần dồi dào, thúc đẩy sự sáng tạo và khả năng thích ứng với môi trường. Chúng là nền tảng cho một cuộc sống có ý nghĩa, giúp cá nhân vượt qua thử thách và kiến tạo giá trị cho bản thân và cộng đồng.

Tuy nhiên, ranh giới giữa một niềm đam mê lành mạnh và một hành vi nghiện ngập đôi khi rất tinh tế và dễ bị nhầm lẫn. Cả hai đều liên quan đến sự gắn kết sâu sắc với một hoạt động, nhưng chúng khác biệt cơ bản về bản chất và tác động lên cuộc sống cá nhân. Đam mê lành mạnh được định nghĩa là một sự lựa chọn tự nguyện, mang lại niềm vui, giá trị và sự thỏa mãn, đồng thời cho phép cá nhân có thể dừng lại hoặc điều chỉnh khi cần thiết. Ngược lại, nghiện ngập là một nhu cầu cưỡng bức, kiểm soát cá nhân, khiến họ khó lòng từ bỏ ngay cả khi nhận thức được những hậu quả tiêu cực.   

Sự khác biệt cốt lõi giữa đam mê và nghiện nằm ở khả năng kiểm soát của cá nhân đối với hành vi và tác động tổng thể của hành vi đó lên cuộc sống. Đam mê nâng cao giá trị cuộc sống và là một hành vi được lựa chọn, trong khi nghiện ngập phá vỡ các khía cạnh khác và mang tính cưỡng bức. Điều này cho thấy rằng ranh giới giữa hai khái niệm này không phải là nhị phân mà là một phổ liên tục, đòi hỏi sự tự nhận thức và đánh giá liên tục để phân biệt. Khi một hoạt động bắt đầu kiểm soát một người và lấy đi các lĩnh vực khác trong cuộc sống, đó là một dấu hiệu cho thấy nó đang chuyển từ đam mê sang nghiện.

II. Các yếu tố và phương pháp kích thích hứng thú, ham muốn

Để khơi dậy và duy trì hứng thú, ham muốn trong bất kỳ hoạt động nào, việc hiểu rõ nền tảng sinh học và tâm lý là vô cùng cần thiết.

2.1. Nền tảng sinh học của động lực: Vai trò của Dopamine và các Hormone

Dopamine là một chất dẫn truyền thần kinh và hormone hữu cơ quan trọng, được giải phóng chủ yếu bởi vùng dưới đồi tại não bộ. Khi nồng độ dopamine trong cơ thể tăng lên, nó mang lại cảm giác sảng khoái, thích thú, tràn đầy cảm hứng và động lực. Chất này đóng vai trò trung tâm trong nhiều chức năng quan trọng của cơ thể, bao gồm chuyển động, trí nhớ, và đặc biệt là hệ thống khen thưởng và động lực. Dopamine là một phần không thể thiếu trong hệ thống khen thưởng tự nhiên của cơ thể. Khi một người trải qua trạng thái hạnh phúc, đạt được mục tiêu hoặc nhận được phần thưởng, một lượng lớn dopamine sẽ được giải phóng vào não, tạo ra cảm giác hưng phấn và niềm vui. Chính cảm giác tích cực này thúc đẩy con người muốn lặp lại hành vi đó để tái tạo trải nghiệm tương tự.   

Dopamine hoạt động như một cơ chế củng cố thần kinh. Não bộ "học" cách liên kết các hoạt động nhất định với việc giải phóng dopamine, từ đó thúc đẩy mong muốn lặp lại chúng. Đây là cơ sở sinh học cho cả động lực lành mạnh và, khi bị rối loạn, là cơ chế hình thành nghiện. Cảm giác sảng khoái, thích thú, tràn đầy cảm hứng và động lực mà dopamine mang lại khiến cơ thể luôn muốn trải nghiệm cảm giác này nhiều hơn, tạo nên một vòng lặp học hỏi: hoạt động dẫn đến dopamine, dopamine dẫn đến khoái cảm, và khoái cảm dẫn đến mong muốn lặp lại hoạt động. Đây là cơ chế cốt lõi của sự củng cố hành vi.

Ham muốn và động lực không chỉ chịu ảnh hưởng của dopamine mà còn bởi sự cân bằng của các hormone khác và tình trạng sức khỏe thể chất tổng thể. Các hormone sinh dục như testosterone (ở cả nam và nữ) và estrogen (ở nữ) đóng vai trò quan trọng trong việc điều chỉnh ham muốn. Sự sụt giảm nồng độ các hormone này có thể dẫn đến giảm ham muốn đáng kể. Ngoài ra, sức khỏe tổng thể, bao gồm các trạng thái như mang thai, mãn kinh, các vấn đề về sức khỏe sinh sản (ví dụ: rối loạn cương dương), các bệnh lý toàn thân nghiêm trọng (như ung thư, bệnh thận), thiếu ngủ, căng thẳng kéo dài, trầm cảm, và tác dụng phụ của một số loại thuốc (điều trị tim mạch, huyết áp, trầm cảm) đều có thể làm suy giảm ham muốn và động lực. Việc lạm dụng rượu và các chất kích thích, mặc dù ban đầu có thể gây hưng phấn, nhưng về lâu dài sẽ làm suy yếu hệ thần kinh và gây tác dụng ngược, làm giảm ham muốn.   

Sự tương tác phức tạp giữa các yếu tố sinh học (hormone, sức khỏe thể chất) và tâm lý (căng thẳng, trầm cảm) là cực kỳ quan trọng đối với động lực. Điều này cho thấy một cách tiếp cận toàn diện đối với sức khỏe tổng thể là nền tảng để duy trì hứng thú và ham muốn bền vững. Ví dụ, khi cơ thể bị stress và căng thẳng kéo dài, một số hormone như cortisol và adrenaline được tiết ra, gây giảm ham muốn tình dục. Điều này minh họa mối liên hệ chặt chẽ giữa trạng thái tinh thần và cân bằng sinh lý. Việc giải quyết vấn đề động lực không chỉ là về khía cạnh tâm lý mà còn về việc duy trì một cơ thể khỏe mạnh và cân bằng nội tiết.   

Để tối ưu hóa mức dopamine một cách tự nhiên và bền vững, có nhiều phương pháp có thể áp dụng, liên quan trực tiếp đến các lựa chọn lối sống hàng ngày. Việc các lựa chọn lối sống lành mạnh, đơn giản có thể tác động trực tiếp đến nồng độ chất dẫn truyền thần kinh nhấn mạnh mối liên hệ sâu sắc giữa sức khỏe thể chất và động lực tinh thần. Điều này thay đổi nhận thức từ quan điểm cho rằng "động lực hoàn toàn là ý chí" sang nhận định rằng "động lực cũng là một trạng thái sinh hóa bị ảnh hưởng bởi thói quen hàng ngày."

Bảng 1: Các phương pháp tự nhiên để tối ưu hóa mức Dopamine

Phương pháp	Mô tả và Tác động	Nguồn tham khảo
Hoạt động thể chất	Tập thể dục, thiền, yoga, xoa bóp, đi dạo giúp tăng nồng độ dopamine, mang lại cảm giác vui vẻ và thư giãn.	
Thiết lập và đạt mục tiêu	Lập kế hoạch mục tiêu rõ ràng. Khi đạt được mục tiêu, cơ thể kích thích sản xuất thêm dopamine, củng cố động lực.	
Dinh dưỡng cân bằng	Bổ sung các vitamin và khoáng chất như sắt, niacin, folate, vitamin B6 hỗ trợ sản xuất dopamine.	
Tiếp xúc ánh nắng mặt trời	Giúp cơ thể hấp thụ đủ ánh sáng, kích thích sản xuất dopamine và cải thiện tâm trạng.	
Ngủ đủ giấc	Đảm bảo ngủ 7-9 giờ mỗi đêm giúp não hoạt động ổn định và duy trì mức dopamine cân bằng. Thiếu ngủ làm gián đoạn nhịp điệu tự nhiên này.	
Hoạt động thư giãn tâm trí	Thiền, vẽ tranh, âm nhạc, nhiếp ảnh, khiêu vũ giúp tăng mức dopamine và cải thiện tâm trạng.	




"""
)

def split_text_by_paragraphs(text_to_split, num_chunks):
    """Chia văn bản thành các phần dựa trên các đoạn văn."""
    paragraphs = text_to_split.strip().split('\n\n')
    # Loại bỏ các đoạn trống nếu có
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    if not paragraphs:
        return []

    # Phân phối các đoạn văn vào các chunk một cách đều đặn (round-robin)
    chunks = [''] * num_chunks
    for i, p in enumerate(paragraphs):
        chunks[i % num_chunks] += p + '\n\n'
    
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def text_to_audio_chunk(text_chunk, index, language, temp_dir):
    """Chuyển một đoạn văn bản thành file audio và lưu vào thư mục tạm."""
    try:
        if not text_chunk:
            print(f"Luồng {index}: Không có văn bản để xử lý.")
            return
            
        temp_file_path = os.path.join(temp_dir, f"temp_{index}.mp3")
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
    num_threads = 5

    # Tạo thư mục tạm nếu chưa có
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Chia văn bản thành các phần
    text_chunks = split_text_by_paragraphs(text, num_threads)
    
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

