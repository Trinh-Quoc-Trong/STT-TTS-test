import os
import queue
import threading
import time
import json
import numpy as np
import torch
import speech_recognition as sr
import pygame
import scipy.io.wavfile
from faster_whisper import WhisperModel
from transformers import MarianMTModel, MarianTokenizer, VitsModel, AutoTokenizer

# --- LOGGING SETUP ---
LOG_PATH = "debug.log"

def log_debug(hypothesis_id, message, data=None):
    # #region agent log
    try:
        log_entry = {
            "id": f"log_{time.time()}",
            "timestamp": int(time.time() * 1000),
            "location": "local_stream_translator.py",
            "message": message,
            "data": data or {},
            "sessionId": "debug-session-001",
            "runId": "run1",
            "hypothesisId": hypothesis_id
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        # print(f"[DEBUG] {message}") 
    except Exception:
        pass
    # #endregion

# --- CONFIG ---
WHISPER_SIZE = "small"
TRANS_MODEL_NAME = "Helsinki-NLP/opus-mt-en-vi"
TTS_MODEL_ID = "facebook/mms-tts-vie"
TTS_SPEED = 1.2

# Biến cờ để kiểm soát việc nói/nghe (Tránh thu lại giọng AI)
IS_SPEAKING = False

audio_queue = queue.Queue()

# --- MODEL LOADING ---
print("--- LOADING MODELS ---")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")

try:
    whisper_model = WhisperModel(WHISPER_SIZE, device="cuda" if torch.cuda.is_available() else "cpu", compute_type="float16" if torch.cuda.is_available() else "int8")
    trans_tokenizer = MarianTokenizer.from_pretrained(TRANS_MODEL_NAME)
    trans_model = MarianMTModel.from_pretrained(TRANS_MODEL_NAME).to(device)
    tts_tokenizer = AutoTokenizer.from_pretrained(TTS_MODEL_ID)
    tts_model = VitsModel.from_pretrained(TTS_MODEL_ID).to(device)
    tts_model.config.noise_scale = 0.3
    print(">>> SYSTEM READY <<<")
except Exception as e:
    print(f"Lỗi model: {e}")

def translate_text(text):
    if not text: return ""
    try:
        inputs = trans_tokenizer(text, return_tensors="pt", padding=True).to(device)
        translated = trans_model.generate(**inputs, max_length=128)
        result = trans_tokenizer.decode(translated[0], skip_special_tokens=True)
        return result
    except Exception:
        return text

def text_to_speech_file(text, filename):
    if not text: return False
    try:
        inputs = tts_tokenizer(text, return_tensors="pt").to(device)
        with torch.no_grad():
            output = tts_model(**inputs)
        
        waveform = output.waveform[0].cpu().float().numpy()
        save_rate = int(tts_model.config.sampling_rate * TTS_SPEED)
        scipy.io.wavfile.write(filename, save_rate, waveform)
        return True
    except Exception as e:
        print(f"TTS Error: {e}")
        return False

def play_audio(file_path):
    global IS_SPEAKING
    try:
        # Đánh dấu đang nói để luồng nghe tạm dừng xử lý
        IS_SPEAKING = True
        
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        os.remove(file_path)
    except Exception as e:
        print(f"Play Error: {e}")
    finally:
        # Nói xong, cho phép nghe lại
        IS_SPEAKING = False

def processing_worker():
    while True:
        try:
            audio_data = audio_queue.get(timeout=1)
        except queue.Empty:
            continue
            
        if audio_data is None: break
        
        # Nếu AI đang nói trong lúc đoạn này được thu, thì bỏ qua đoạn này (để tránh lặp)
        if IS_SPEAKING:
            # #region agent log
            log_debug("SKIP", "Skipped audio chunk because AI is speaking")
            # #endregion
            audio_queue.task_done()
            continue

        try:
            segments, _ = whisper_model.transcribe(audio_data, beam_size=5, language="en")
            full_en_text = " ".join([s.text for s in segments]).strip()
            
            if full_en_text:
                # Filter Hallucinations
                if len(full_en_text) < 2 or "Subscribe" in full_en_text or "watching" in full_en_text:
                     pass
                else:
                    vi_text = translate_text(full_en_text)
                    print(f"\nEN: {full_en_text}\nVI: {vi_text}")
                    
                    q_size = audio_queue.qsize()
                    temp_file = f"temp_{int(time.time())}_{q_size}.wav"
                    
                    if text_to_speech_file(vi_text, temp_file):
                        play_audio(temp_file)
        except Exception as e:
             print(f"Worker Error: {e}")
        
        audio_queue.task_done()

def get_stereo_mix_index():
    mics = sr.Microphone.list_microphone_names()
    print("\n--- DANH SÁCH THIẾT BỊ ---")
    detected_idx = None
    
    for i, name in enumerate(mics):
        print(f"[{i}] {name}")
        # Tìm ưu tiên
        if "Stereo Mix" in name or "Stereo Mix" in name:
            detected_idx = i
        elif "CABLE Output" in name and detected_idx is None:
            detected_idx = i

    if detected_idx is not None:
        print(f"\n>>> TỰ ĐỘNG CHỌN: [{detected_idx}] {mics[detected_idx]} <<<")
        return detected_idx
    else:
        print("\nKHÔNG TÌM THẤY 'Stereo Mix' HOẶC 'CABLE Output'.")
        print("Vui lòng nhập thủ công số Index thiết bị muốn dùng (nhìn list trên):")
        try:
            return int(input(">> Index: "))
        except:
            return 0 # Fallback

def main():
    t = threading.Thread(target=processing_worker, daemon=True)
    t.start()

    r = sr.Recognizer()
    r.energy_threshold = 1000
    r.pause_threshold = 0.8
    r.dynamic_energy_threshold = False

    # TỰ ĐỘNG CHỌN MIC / STEREO MIX
    mic_index = get_stereo_mix_index()

    # #region agent log
    log_debug("INIT", f"Selected mic index: {mic_index}")
    # #endregion

    try:
        with sr.Microphone(device_index=mic_index, sample_rate=16000) as source:
            print(f"\n--- ĐANG NGHE TỪ HỆ THỐNG (Index {mic_index}) ---")
            print("Mẹo: Nếu không thấy chữ chạy, hãy kiểm tra Volume của Stereo Mix trong Sound Settings.")
            
            r.adjust_for_ambient_noise(source, duration=1)
            
            while True:
                try:
                    # Giảm thời gian nghe mỗi câu xuống 5s để phản hồi nhanh hơn
                    audio = r.listen(source, phrase_time_limit=5)
                    
                    # Nếu đang nói thì không cần xử lý convert (tiết kiệm CPU)
                    if IS_SPEAKING: 
                        continue

                    data = np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0
                    audio_queue.put(data)
                except KeyboardInterrupt:
                    break
                except Exception:
                    pass
    except OSError as e:
        print(f"\nLỖI KẾT NỐI THIẾT BỊ ÂM THANH (Index {mic_index}):")
        print(f"{e}")
        print("Gợi ý: Vào Windows Sound Settings -> Recording -> Chuột phải 'Stereo Mix' -> Enable.")

if __name__ == "__main__":
    main()
