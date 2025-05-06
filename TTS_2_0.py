# <(6O9)>  
import os
from gtts import gTTS
from playsound import playsound  # Chuyển văn bản thành giọng nói  
import io             # Quản lý file trong bộ nhớ  
import threading      # Xử lý đa luồng để tăng tốc  

language_ = "vi"
text = (
r"""




Sự nghiệp đối với tôi không chỉ là một con đường thăng tiến, mà là một cuộc hành trình đầy thử thách và cơ hội để tạo ra ảnh hưởng. Tôi tận hiến với từng chi tiết nhỏ nhất, coi công việc như một chiến trường khốc liệt, nơi tôi là kẻ chinh phục. Bề ngoài, tôi giản dị, khiêm nhường, hòa mình vào dòng chảy cuộc sống một cách kín đáo. Nhưng ẩn sâu bên trong lớp vỏ bọc ấy là một mạng lưới ảnh hưởng mà tôi đã xây dựng qua nhiều năm, nơi tôi lặng lẽ đóng vai trò quan trọng trong các quyết định then chốt.

Ngay từ những bước chân đầu tiên trong sự nghiệp, khi còn là một nhân viên bình thường, tôi đã là một người đóng góp quan trọng nhưng không phô trương. Tôi là cánh tay đắc lực, người âm thầm phân tích, dự đoán và đề xuất chiến lược cho cấp trên. Tôi, một chuyên gia kỹ thuật hoặc nhà chiến lược, nắm giữ những hiểu biết then chốt và thường xuyên đóng góp ý tưởng từ trong bóng tối.

Kỹ năng và tầm nhìn của tôi vượt xa vị trí quản lý hiện tại, và tôi thường được mời tham gia vào các cuộc thảo luận chiến lược quan trọng của công ty. Công việc của tôi ảnh hưởng trực tiếp đến sự phát triển của công ty, và mức lương của tôi phản ánh giá trị mà tôi mang lại, dù tôi không phải là người đứng đầu.

Tham vọng của tôi không dừng lại ở đó. Tôi khao khát trở thành một chuyên gia hàng đầu trong lĩnh vực công nghệ thông tin, đặc biệt là trong trí tuệ nhân tạo. Kiến thức và công nghệ tiên tiến là vũ khí tối thượng, giúp tôi tự tin dẫn dắt và đóng góp vào những dự án tiên tiến. Tôi chỉ hứng thú với những dự án tầm cỡ, những thách thức xứng tầm với khát khao của mình.

Vòng tròn quan hệ của tôi trải rộng khắp nhiều tầng lớp, từ những nhân vật có ảnh hưởng trong ngành cho đến những người tài năng và khôn khéo. Tôi đánh giá cao vẻ đẹp, trí tuệ và sự tinh tế của những người phụ nữ xuất chúng. Tôi kín đáo trong chuyện tình cảm, không phô trương, nhưng tôi có một mạng lưới xã hội rộng lớn và thường xuyên tương tác với những người thú vị. Sự thành công và phong cách của tôi thu hút sự chú ý, và tôi thường được những người tài năng và hấp dẫn tìm đến.

Hình mẫu lý tưởng của tôi là những người phụ nữ thông minh, độc lập và có sự nghiệp thành công. Tôi là một người có tầm nhìn quốc tế, lạnh lùng và bản lĩnh, vừa chinh phục đỉnh cao sự nghiệp, vừa tận hưởng cuộc sống đẳng cấp. Tôi luôn biết cách cân bằng giữa công việc và cuộc sống cá nhân, khéo léo duy trì một hình ảnh chuyên nghiệp và kín đáo.




"""
)

def text_to_audio_play(text, language=language_): 
    save_path = r"D:\code\phanMemDoc\doc_len_001.mp3"
    # Chuyển văn bản thành file mp3 trong bộ nhớ  
    tts = gTTS(text=text, lang=language, slow=False)  
    tts.save(save_path) # lưu file mp3

    os.startfile(save_path)





def text_to_speech(text, language=language_):  
    # Chạy xử lý trong một thread để chương trình không bị chặn  
    threading.Thread(target=text_to_audio_play, args=(text, language)).start()  
text_to_speech(text)  # Gọi hàm đọc văn bản

