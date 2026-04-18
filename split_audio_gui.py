import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import whisper
from pydub import AudioSegment

# Kiểm tra xem ffmpeg có sẵn không (cần thiết cho pydub)
# Nếu người dùng đã cài pydub và chạy được STT_1_0.py thì có thể đã ok.
# Nếu không, cần hướng dẫn cài ffmpeg.

class AudioSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phần Mềm Cắt Audio Theo Câu")
        self.root.geometry("600x450")
        
        # Biến lưu đường dẫn
        self.input_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.model_name = tk.StringVar(value="base")
        self.status_var = tk.StringVar(value="Sẵn sàng")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chọn file đầu vào
        ttk.Label(main_frame, text="1. Chọn file Audio/Video:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable=self.input_path, width=50).grid(row=1, column=0, sticky="ew", pady=5)
        ttk.Button(main_frame, text="Chọn File", command=self.browse_input).grid(row=1, column=1, padx=5)
        
        # Chọn thư mục đầu ra
        ttk.Label(main_frame, text="2. Chọn thư mục lưu kết quả:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable=self.output_dir, width=50).grid(row=3, column=0, sticky="ew", pady=5)
        ttk.Button(main_frame, text="Chọn Thư Mục", command=self.browse_output).grid(row=3, column=1, padx=5)
        
        # Chọn Model
        ttk.Label(main_frame, text="3. Chọn độ chính xác (Model):").grid(row=4, column=0, sticky="w", pady=5)
        model_frame = ttk.Frame(main_frame)
        model_frame.grid(row=5, column=0, sticky="w", pady=5)
        models = ["tiny", "base", "small", "medium", "large"]
        ttk.Combobox(model_frame, textvariable=self.model_name, values=models, state="readonly").pack(side=tk.LEFT)
        ttk.Label(model_frame, text="(Tiny nhanh nhất, Large chính xác nhất)").pack(side=tk.LEFT, padx=10)
        
        # Nút xử lý
        self.process_btn = ttk.Button(main_frame, text="Bắt Đầu Cắt Audio", command=self.start_processing)
        self.process_btn.grid(row=6, column=0, columnspan=2, pady=20, sticky="ew")
        
        # Log/Status
        ttk.Label(main_frame, text="Trạng thái:").grid(row=7, column=0, sticky="w")
        self.log_text = tk.Text(main_frame, height=8, width=70, state="disabled")
        self.log_text.grid(row=8, column=0, columnspan=2, pady=5)
        
    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Media Files", "*.mp3 *.wav *.mp4 *.mkv *.avi *.flac *.m4a"), ("All Files", "*.*")]
        )
        if filename:
            self.input_path.set(filename)
            # Tự động gợi ý thư mục output
            default_out = os.path.join(os.path.dirname(filename), "cut_segments")
            self.output_dir.set(default_out)

    def browse_output(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.output_dir.set(dirname)
            
    def start_processing(self):
        input_file = self.input_path.get()
        output_folder = self.output_dir.get()
        model = self.model_name.get()
        
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Lỗi", "Vui lòng chọn file đầu vào hợp lệ.")
            return
            
        if not output_folder:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục lưu kết quả.")
            return

        # Chạy trong luồng riêng để không đơ giao diện
        self.process_btn.config(state="disabled")
        thread = threading.Thread(target=self.process_audio, args=(input_file, output_folder, model))
        thread.start()
        
    def process_audio(self, input_file, output_folder, model_name):
        try:
            self.log(f"--- Bắt đầu xử lý: {os.path.basename(input_file)} ---")
            
            # Tạo thư mục đầu ra nếu chưa có
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                self.log(f"Đã tạo thư mục: {output_folder}")

            # Bước 1: Transcribe bằng Whisper
            self.log(f"Đang tải model Whisper '{model_name}'... (có thể mất vài phút lần đầu)")
            model = whisper.load_model(model_name)
            
            self.log("Đang nhận dạng văn bản và timestamp...")
            result = model.transcribe(input_file)
            segments = result["segments"]
            
            self.log(f"Tìm thấy {len(segments)} câu.")
            
            # Bước 2: Cắt audio bằng Pydub
            self.log("Đang đọc file audio nguồn...")
            # Pydub tự động xử lý mp3/wav/mp4 nếu ffmpeg được cài
            try:
                audio = AudioSegment.from_file(input_file)
            except Exception as e:
                self.log(f"Lỗi đọc audio (có thể do thiếu ffmpeg): {e}")
                self.process_btn.config(state="normal")
                return

            self.log("Bắt đầu cắt file...")
            for i, segment in enumerate(segments):
                start_ms = int(segment["start"] * 1000)
                end_ms = int(segment["end"] * 1000)
                text = segment["text"].strip()
                
                # Cắt
                segment_audio = audio[start_ms:end_ms]
                
                # Tên file: 001_text_preview.mp3 (lọc ký tự đặc biệt)
                safe_text = "".join([c for c in text if c.isalnum() or c in " _-"])[:30]
                out_name = f"{i+1:03d}_{safe_text}.mp3"
                out_path = os.path.join(output_folder, out_name)
                
                segment_audio.export(out_path, format="mp3")
                self.log(f"Đã lưu: {out_name}")
                
            self.log("\n--- HOÀN TẤT! ---")
            messagebox.showinfo("Thành công", f"Đã cắt xong {len(segments)} đoạn audio!")
            
        except Exception as e:
            self.log(f"Lỗi nghiêm trọng: {e}")
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
        finally:
            self.process_btn.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSplitterApp(root)
    root.mainloop()
















