# script dùng để lấy ra những thông tin trong văn bản 

FILE_PATH = 'run_text.txt'

def main():
    print("name:", FILE_PATH)
    print("Bắt đầu đọc file...")
    
    try:
        # doc file
        with open(file= FILE_PATH, mode= 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"Độ dài file: {len(content)} ký tự")
            
            if len(content) > 100:
                print('Ký tự thứ 100:', repr(content[100]))
                print('Nội dung từ ký tự 95-105:', repr(content[95:105]))
            else:
                print('File quá ngắn!')
                print('Nội dung đầy đủ:', repr(content[:200]))
                
    except Exception as e:
        print(f"Lỗi: {e}")
        
if __name__ == "__main__":
    main()