# 📖 Tài liệu kỹ thuật chi tiết cho dự án STT-TTS-test

> **Mục tiêu**  
> 1. Mô tả toàn diện kiến trúc, thuật toán, luồng xử lý & các điểm then chốt về công nghệ cho hệ thống Text-to-Speech (TTS) thế hệ mới.
> 2. Cung cấp hướng dẫn cài đặt và vận hành chi tiết nhằm tái tạo dễ dàng, đặc biệt là cách tận dụng tối đa GPU phần cứng.
> 3. Giải thích rõ ràng các lựa chọn thiết kế, tối ưu hoá bộ nhớ (VRAM) và tốc độ tạo giọng nói.

---

## 1. Tổng quan kiến trúc hệ thống

Trọng tâm của dự án hiện tại là **Phiên bản 6.0 (`TTS_6_0_vieneu.py`)**. Các phiên bản cũ sử dụng API trực tuyến (gTTS, Edge-TTS) đã được đưa vào kho lưu trữ (`old_scripts/`) do phụ thuộc vào kết nối mạng và giới hạn số lần gọi (Rate Limit).

Phiên bản 6.0 hoàn toàn **OFFLINE 100%**, bảo mật dữ liệu tuyệt đối và chạy siêu tốc trên card đồ họa (GPU).

```text
┌─────────────────┐       (Đọc file)       ┌────────────────────────┐
│  run_text.txt   │ ─────────────────────▶ │ Lọc Markdown, Normalize│
└─────────────────┘                        └────────────────────────┘
                                                       │
                                                       ▼
                                           ┌────────────────────────┐
                                           │ Chia Chunk (30-40 từ)  │
                                           └────────────────────────┘
                                                       │
               +───────────────────────────────────────┼───────────────────────────────────────+
               │                                                                               │
   (GPU) Llama-cpp-python                                                          (CPU) ONNX Runtime
   Sinh Acoustic Tokens (Tốc độ cao)                                               Giải mã Tokens thành Waveform
               │                                                                               │
               +───────────────────────────────────────┼───────────────────────────────────────+
                                                       ▼
                                           ┌────────────────────────┐
                                           │ Ghép Audio & Hậu kỳ    │
                                           │ (Tốc độ, Cao độ - MP3) │
                                           └────────────────────────┘
                                                       │
                                                       ▼
                                              doc_len_vieneu.mp3
```

---

## 2. Công nghệ cốt lõi & Thư viện

| Thư viện / Công nghệ | Vai trò & Mục đích | Ghi chú |
| :--- | :--- | :--- |
| **`vieneu`** | Cung cấp model AI tạo giọng nói tiếng Việt chất lượng cao. | Model 0.3B tham số, chạy offline hoàn toàn. |
| **`llama-cpp-python`** | Engine cốt lõi để chạy mô hình ngôn ngữ trên GPU. | **Cực kỳ quan trọng**: Cần bản build hỗ trợ CUDA (cu124) để không bị nghẽn ở CPU. |
| **`librosa`** | Tiền xử lý, hậu kỳ âm thanh (thay đổi tốc độ, cao độ). | Giữ nguyên pitch khi tăng tốc độ (time-stretch). |
| **`pydub` & `soundfile`** | Xử lý mảng âm thanh, ghi và chuyển đổi định dạng xuất ra MP3. | Phụ thuộc vào `ffmpeg`. |
| **`tqdm`** | Hiển thị thanh tiến trình (progress bar) trực quan trên Terminal. | |

---

## 3. Phân tích chi tiết mô-đun `TTS_6_0_vieneu.py`

### 3.1. Thuật toán Chunking thông minh (Sequential Batching)
Khác với các phiên bản trước sử dụng Multi-threading (đa luồng) gây ra lỗi tràn bộ nhớ VRAM (Out-of-Memory) và nghẽn cổ chai (Context Switching) trên GPU, phiên bản 6.0 xử lý theo cơ chế **Chunking nối tiếp**.

- Thuật toán sẽ dùng Regex để tách văn bản gốc thành các câu hoàn chỉnh (dựa trên dấu câu `.` `?` `!`).
- Kế tiếp, nó sẽ gom các câu ngắn lại thành một khối (chunk) có độ dài khoảng **30-40 từ**.
- **Lý do:** Mô hình Auto-regressive sẽ sinh từ rất chậm và tốn RAM nếu chuỗi đầu vào quá dài. Mức 30-40 từ (tương đương 10-15s âm thanh) là "điểm ngọt" (sweet spot) giúp GPU nội suy nhanh nhất (lên tới **7.5x Realtime** trên RTX 3060).

### 3.2. Quản lý thiết bị (GPU vs CPU)
Mô hình TTS của VieNeu gồm 2 phần:
1. **Backbone (LLM)**: Được offload hoàn toàn 100% layer lên GPU thông qua `llama-cpp-python`.
2. **Codec Decoder (ONNX)**: Được thiết kế chỉ chạy trên CPU. (Sẽ có cảnh báo vàng khi chạy, đây là hành vi bình thường).

### 3.3. Hậu kỳ (Post-processing)
Sau khi GPU tạo ra hàng loạt các mảng numpy arrays, code sẽ:
1. Nối (`np.concatenate`) tất cả thành một mảng âm thanh dài.
2. Dùng `librosa` áp dụng biến đổi **Pitch Shift** (cao độ) hoặc **Time Stretch** (tốc độ).
3. Xuất file thông qua `soundfile` tạo file `.wav` tạm, sau đó dùng `pydub` nén lại thành MP3 192kbps chất lượng cao.

---

## 4. Hướng dẫn cài đặt môi trường (Dành riêng cho Linux / Ubuntu có GPU NVIDIA)

Để tránh lỗi thư viện rơi vào trạng thái chạy CPU (cực chậm), vui lòng tuân thủ chính xác các bước dưới đây.

**Bước 1: Tạo và kích hoạt môi trường ảo (Conda/Venv)**
```bash
conda create -n tts_env python=3.10 -y
conda activate tts_env
```

**Bước 2: Cài đặt các thư viện lõi**
```bash
pip install numpy pydub tqdm soundfile torch librosa
```

**Bước 3: Cài đặt thư viện VieNeu**
```bash
pip install vieneu[gpu]
```

**Bước 4: Ép buộc cài đặt `llama-cpp-python` có hỗ trợ CUDA (Quan trọng nhất 🚨)**
Bản `llama-cpp-python` tải về bằng pip thông thường trên Linux sẽ CHỈ hỗ trợ CPU. Bạn cần gỡ nó ra và cài bản đã được build sẵn cho CUDA (ví dụ CUDA 12.4):
```bash
pip uninstall -y llama-cpp-python
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124
```
*(Nếu máy bạn dùng bản CUDA khác, hãy thay `cu124` thành `cu118` hoặc `cu121` tương ứng).*

**Bước 5: Cài đặt `ffmpeg` (để xuất MP3)**
```bash
sudo apt update
sudo apt install ffmpeg -y
```

---

## 5. Hướng dẫn sử dụng

Chỉ cần để văn bản cần đọc vào file `run_text.txt` nằm ở cùng thư mục, sau đó chạy:

```bash
python3 TTS_6_0_vieneu.py
```

### Chỉnh sửa cấu hình trong code
Mở file `TTS_6_0_vieneu.py` và sửa các tham số ở phần đầu file:

- `VOICE_PRESET_INDEX`: Thay đổi ID giọng đọc (0: Bình, 1: Tuyên, 2: Vĩnh, 3: Đoan, 4: Ly, 5: Ngọc).
- `SPEED`: Tốc độ nói (1.0 là mặc định, 1.2 là nhanh hơn).
- `PITCH_SHIFT`: Cao độ (0 là mặc định, -2 là trầm hơn, +2 là cao hơn).

---

## 6. Lộ trình nâng cấp (Roadmap)
- [ ] Tích hợp API Server (FastAPI) để nhận văn bản từ web/mobile trả về luồng âm thanh trực tiếp (Streaming).
- [ ] Chuyển đổi mã bộ giải mã (Codec) của ONNX sang TensorRT để đưa luôn công đoạn giải mã lên GPU, tăng tốc độ tổng hợp lên trên mức 15x realtime.
- [ ] Xây dựng giao diện UI (Streamlit/Gradio) để dễ tương tác hơn.
