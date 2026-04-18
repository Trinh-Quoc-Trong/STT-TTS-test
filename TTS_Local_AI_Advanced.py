# -*- coding: utf-8 -*-
# PHIÊN BẢN LOCAL AI FIX LỖI BATCH & OUTPUT - CHẠY ỔN ĐỊNH
# Model: facebook/mms-tts-vie

import os
import torch
import scipy.io.wavfile
import numpy as np
from transformers import VitsModel, AutoTokenizer
from pydub import AudioSegment
from tqdm import tqdm
import sys
import re  # Thêm thư viện regex

# --- CẤU HÌNH ---
MODEL_ID = "facebook/mms-tts-vie"
INPUT_TEXT_FILE = "run_text.txt"
OUTPUT_AUDIO_FILE = "doc_len_local_AI_Batch_Advanced.mp3"
TEMP_DIR = "temp_audio_chunks_batch"

# --- BẢNG ĐIỀU KHIỂN ---
BATCH_SIZE = 8             # Giữ mức an toàn
LENGTH_SCALE = 0.85
NOISE_SCALE = 0.4
NOISE_SCALE_W = 0.4
AUDIO_SPEED_FACTOR = 1.2
PITCH_SHIFT_SEMITONES = 2.0 
SILENCE_DURATION = 30

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, 'reconfigure'): sys.stderr.reconfigure(encoding="utf-8")
    except: pass

def load_model():
    print("--- ĐANG KHỞI TẠO MODEL (BATCH MODE) ---")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Thiết bị: {device.upper()}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = VitsModel.from_pretrained(MODEL_ID).to(device)
    
    # Cấu hình model
    model.config.length_scale = LENGTH_SCALE
    model.config.noise_scale = NOISE_SCALE
    model.config.noise_scale_w = NOISE_SCALE_W
    return tokenizer, model, device

def change_pitch_and_speed(sound, speed=1.0, pitch_semitones=0.0):
    if pitch_semitones != 0:
        pitch_factor = 2.0 ** (pitch_semitones / 12.0)
        new_sample_rate = int(sound.frame_rate * pitch_factor)
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        sound = sound.set_frame_rate(sound.frame_rate)
    
    if speed != 1.0:
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        })
        sound = sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)
    return sound

def clean_text(text):
    """
    Làm sạch văn bản: Loại bỏ ký tự lạ, URL, emoji, dấu câu thừa.
    """
    # 1. Xóa URL/Link
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # 2. Xóa các ký tự đặc biệt không phải dấu câu tiếng Việt cơ bản
    # Giữ lại: Chữ cái (bao gồm tiếng Việt), số, khoảng trắng, và .,?!:;'"-()
    # Loại bỏ: @#$%^&*[]{}<>|~`_+=/ và emoji
    text = re.sub(r'[^\w\s.,?!:;\'"()\-\u00C0-\u1EF9]', ' ', text)
    
    # 3. Thay thế khoảng trắng thừa (nhiều khoảng trắng liên tiếp thành 1)
    text = re.sub(r'\s+', ' ', text)
    
    # 4. Xóa dấu câu đứng đầu/cuối câu vô nghĩa (ví dụ: ". Xin chào")
    text = text.strip(" .,?!:;")
    
    return text.strip()

def split_text_smart(text, max_chars=200):
    # Bước 1: Làm sạch văn bản trước khi chia
    text = clean_text(text)
    
    text = text.replace('\n', '. ')
    sentences = text.split('.')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence: continue
        
        # Nếu cộng thêm câu này mà dài quá thì ngắt
        if len(current_chunk) + len(sentence) > max_chars:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
        else:
            current_chunk += sentence + ". "
            
    if current_chunk: chunks.append(current_chunk.strip())
    return chunks

def run_tts_batch():
    if not os.path.exists(INPUT_TEXT_FILE):
        print("Thiếu file input.")
        return

    with open(INPUT_TEXT_FILE, "r", encoding="utf8") as f:
        text = f.read()

    if not os.path.exists(TEMP_DIR): os.makedirs(TEMP_DIR)
    
    tokenizer, model, device = load_model()
    if not model: return

    chunks = split_text_smart(text, max_chars=200)
    batches = [chunks[i:i + BATCH_SIZE] for i in range(0, len(chunks), BATCH_SIZE)]
    generated_files = [] 
    global_idx = 0
    
    print("\n--- BẮT ĐẦU SINH GIỌNG (BATCH INFERENCE) ---")
    
    for batch in tqdm(batches, desc="Processing Batches"):
        try:
            inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True).to(device)
            
            with torch.no_grad():
                output = model(**inputs)
            
            if hasattr(output, 'waveform'):
                waveform_batch = output.waveform
            else:
                waveform_batch = output[0]

            waveform_np = waveform_batch.cpu().float().numpy()
            
            for i in range(len(batch)):
                if waveform_np.ndim == 3:
                    data = waveform_np[i][0]
                else:
                    data = waveform_np[i]
                
                temp_path = os.path.join(TEMP_DIR, f"chunk_{global_idx}.wav")
                scipy.io.wavfile.write(temp_path, rate=model.config.sampling_rate, data=data)
                generated_files.append(temp_path)
                global_idx += 1
                
        except Exception as e:
            print(f"\nLỗi Batch tại index {global_idx}: {e}")
            torch.cuda.empty_cache()

    print("\n--- XỬ LÝ HẬU KỲ & GHÉP FILE ---")
    if not generated_files:
        print("Lỗi: Không tạo được file audio nào!")
        return

    final_audio = AudioSegment.empty()
    silence = AudioSegment.silent(duration=SILENCE_DURATION)
    
    for file_path in tqdm(generated_files, desc="Merging"):
        try:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                segment = AudioSegment.from_wav(file_path)
                if PITCH_SHIFT_SEMITONES != 0 or AUDIO_SPEED_FACTOR != 1.0:
                    segment = change_pitch_and_speed(segment, speed=AUDIO_SPEED_FACTOR, pitch_semitones=PITCH_SHIFT_SEMITONES)
                final_audio += segment + silence
        except Exception as e:
            print(f"Lỗi ghép file {file_path}: {e}")

    if len(final_audio) > 0:
        final_audio.export(OUTPUT_AUDIO_FILE, format="mp3")
        print(f"\nHOÀN TẤT! File: {OUTPUT_AUDIO_FILE}")
        if sys.platform == "win32":
            os.startfile(OUTPUT_AUDIO_FILE)
    else:
        print("File kết quả rỗng.")
    
    # Dọn dẹp
    for f in generated_files:
        try: os.remove(f)
        except: pass
    try: os.rmdir(TEMP_DIR)
    except: pass

if __name__ == "__main__":
    run_tts_batch()