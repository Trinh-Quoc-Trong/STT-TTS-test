import speech_recognition as sr

# Example of using the speech_recognition module
recognizer = sr.Recognizer()
print("Speech recognition module successfully imported.")

# You can add your specific code here, for example:
# file_path = r"D:\code\phanMemDoc\[TE] L15_Practice 2.mp3"
# try:
#     with sr.AudioFile(file_path) as source:
#         audio_data = recognizer.record(source)
#         text = recognizer.recognize_google(audio_data, language="vi-VN")
#         print("Nội dung file âm thanh:", text)
# except Exception as e:
#     print(f"Error: {e}")