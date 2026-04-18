import srt
from deep_translator import GoogleTranslator
import time
import os
import random

def split_into_chunks(lst, n):
    """Chia list thành các phần nhỏ kích thước n"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def translate_srt_batched(input_path, output_path, src_lang='en', dest_lang='vi', batch_size=20):
    print(f"Đang đọc file: {input_path}")
    
    # Sử dụng GoogleTranslator từ deep_translator
    translator = GoogleTranslator(source=src_lang, target=dest_lang)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {input_path}")
        return

    try:
        subtitles = list(srt.parse(content))
    except Exception as e:
        print(f"Lỗi khi đọc định dạng SRT: {e}")
        return

    total_subs = len(subtitles)
    print(f"Tìm thấy {total_subs} dòng phụ đề.")
    print(f"Chia thành các batch nhỏ ({batch_size} dòng/lần) để gửi API...")

    # Tạo danh sách các chunk (lô)
    chunks = list(split_into_chunks(subtitles, batch_size))
    total_chunks = len(chunks)
    
    translated_count = 0

    for i, chunk in enumerate(chunks):
        # Lọc ra các text cần dịch trong chunk này
        texts_to_translate = [sub.content.strip() for sub in chunk if sub.content.strip()]
        
        # Mapping để gán lại kết quả sau khi dịch
        indices_to_update = [idx for idx, sub in enumerate(chunk) if sub.content.strip()]

        if not texts_to_translate:
            continue

        retries = 3
        while retries > 0:
            try:
                # deep_translator hỗ trợ gửi batch_translate
                results = translator.translate_batch(texts_to_translate)
                
                # Cập nhật nội dung vào subtitle gốc
                if results and len(results) == len(texts_to_translate):
                    for idx_result, translated_text in enumerate(results):
                        chunk_idx = indices_to_update[idx_result]
                        chunk[chunk_idx].content = translated_text
                else:
                    raise Exception("Số lượng kết quả trả về không khớp")

                translated_count += len(texts_to_translate)
                print(f"Đã xử lý batch {i+1}/{total_chunks} ({translated_count}/{total_subs} dòng)...")
                break # Thành công thì thoát vòng lặp retry

            except Exception as e:
                retries -= 1
                print(f"Lỗi ở batch {i+1}: {e}. Đang thử lại ({retries} lần nữa)...")
                time.sleep(random.uniform(2, 5)) 
                
                if retries == 0:
                    print(f"Bỏ qua batch {i+1} và thử dịch từng dòng...")
                    # Fallback: Dịch từng dòng nếu batch lỗi
                    for sub in chunk:
                        text = sub.content.strip()
                        if text:
                            try:
                                translated = translator.translate(text)
                                sub.content = translated
                                # Nghỉ ngắn sau mỗi dòng
                                time.sleep(0.2)
                            except Exception as ex:
                                print(f"  - Lỗi dòng riêng lẻ: {ex}")
                                pass
        
        # Nghỉ ngẫu nhiên giữa các batch
        time.sleep(random.uniform(0.5, 1.5))

        # Lưu file tạm thời sau mỗi 10 batch (đề phòng lỗi giữa chừng)
        if (i + 1) % 10 == 0:
             with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt.compose(subtitles))

    print("Đang lưu file kết quả cuối cùng...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(subtitles))
        
    print(f"Hoàn tất! File đã được lưu tại: {output_path}")

if __name__ == "__main__":
    input_file = r"tests/lecture0_720p_sdr-en.srt"
    output_file = r"tests/lecture0_720p_sdr-vi_full.srt"
    
    translate_srt_batched(input_file, output_file)
