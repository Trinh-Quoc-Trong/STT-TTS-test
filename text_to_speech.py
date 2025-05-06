from playsound import playsound # thư viện giúp phát âm thanh
from gtts import gTTS # thu vien dung de chuyển  văn bản thành giọng nói
import os # thư viện giúp tương tác hệ điều hành


def text_to_speech(text, language="vi"):

    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(r"D:\code\phanMemDoc\docLen.mp3") # lưu file mp3

    if len(text) < 100:
        playsound(r"D:\code\phanMemDoc\docLen.mp3") # Phát âm thanh
    elif len(text) >= 100:
        os.startfile(r"D:\code\phanMemDoc\docLen.mp3")

text = (
r"""


"""
)
text_to_speech(text)
