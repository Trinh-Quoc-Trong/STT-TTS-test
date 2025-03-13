# <(6O9)>  
import os
from gtts import gTTS
from playsound import playsound  # Chuyển văn bản thành giọng nói  
import io             # Quản lý file trong bộ nhớ  
import threading      # Xử lý đa luồng để tăng tốc  

def text_to_audio_play(text, language='en'): 
    save_path = r"D:\code\phanMemDoc\doc_len_001.mp3"
    # Chuyển văn bản thành file mp3 trong bộ nhớ  
    tts = gTTS(text=text, lang=language, slow=False)  
    tts.save(save_path) # lưu file mp3

    os.startfile(save_path)

text = (
r"""
















"""
)





def text_to_speech(text, language="en"):  
    # Chạy xử lý trong một thread để chương trình không bị chặn  
    threading.Thread(target=text_to_audio_play, args=(text, language)).start()  
text_to_speech(text)  # Gọi hàm đọc văn bản

