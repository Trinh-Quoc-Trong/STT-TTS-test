import srt
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from tqdm import tqdm # Thư viện tạo thanh tiến trình
import os

def split_into_batches(lst, batch_size):
    """Chia list thành các batch nhỏ"""
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]

def translate_local(input_path, output_path, model_name="vinai/vinai-translate-en2vi", batch_size=8):
    print(f"Dang khoi tao model AI: {model_name}...")
    
    # Kiểm tra xem có GPU không (CUDA) để chạy cho nhanh
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Dang chay tren thiet bi: {device.upper()}")

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name, src_lang="en_XX")
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    except Exception as e:
        print(f"Loi tai model: {e}")
        return

    # Đọc file SRT
    print(f"Dang doc file: {input_path}")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        subtitles = list(srt.parse(content))
    except Exception as e:
        print(f"Loi doc file: {e}")
        return

    total_subs = len(subtitles)
    print(f"Tim thay {total_subs} dong phu de.")

    # Lọc ra các dòng có nội dung để dịch
    # Chúng ta cần giữ index để gán ngược lại sau khi dịch
    subs_with_content = []
    for idx, sub in enumerate(subtitles):
        text = sub.content.strip()
        if text:
            subs_with_content.append((idx, text))
    
    print("Bat dau dich...")
    
    # Tạo các batch để đưa vào model
    # Model xử lý theo batch sẽ nhanh hơn nhiều so với từng dòng
    batches = list(split_into_batches(subs_with_content, batch_size))
    
    for batch in tqdm(batches, desc="Tiến độ dịch"):
        indices = [item[0] for item in batch]
        texts = [item[1] for item in batch]
        
        try:
            # Tokenize input
            inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True).to(device)
            
            # Generate translation
            # VinAI model thuong can decoder_start_token_id de bat dau dich sang tieng Viet
            translated = model.generate(
                **inputs, 
                max_length=512,
                num_beams=5,
                early_stopping=True,
                decoder_start_token_id=tokenizer.lang_code_to_id["vi_VN"]
            )
            
            # Decode output
            decoded_texts = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
            
            # Cập nhật lại vào danh sách subtitles gốc
            for i, translated_text in enumerate(decoded_texts):
                original_idx = indices[i]
                subtitles[original_idx].content = translated_text
                
        except Exception as e:
            print(f"Loi xu ly batch: {e}")
            # Nếu lỗi batch, có thể thử dịch từng dòng hoặc bỏ qua (ở đây ta bỏ qua để code đơn giản)

    # Lưu file
    print(f"Dang luu file ket qua: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(subtitles))
    
    print("Hoan tat!")

if __name__ == "__main__":
    # Cần cài đặt: pip install transformers sentencepiece torch srt tqdm
    
    input_file = r"translate\visual_studio_code_for_cs50-720p-en.srt"
    output_file = r"translate\visual_studio_code_for_cs50-720p-vn.srt"
    
    # Batch size: Tăng lên nếu VRAM GPU lớn (32, 64), giảm xuống nếu dùng CPU (8, 16)
    translate_local(input_file, output_file, batch_size=8)

