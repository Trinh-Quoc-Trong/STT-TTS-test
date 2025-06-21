"""CLI: đọc văn bản trong file chỉ định và sinh file mp3.

Sử dụng:
    python -m cli.read_text --input data/what_do_you_want_to_read.txt --output data/output.mp3
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
import sys

# Thêm src vào sys.path khi chạy dưới dạng script trực tiếp
sys.path.append(str(Path(__file__).resolve().parents[1]))

from tts.pipeline import TtsPipeline  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Đọc văn bản và xuất mp3")
    parser.add_argument("--input", "-i", type=Path, required=True, help="Đường dẫn file văn bản")
    parser.add_argument("--output", "-o", type=Path, default=Path("data/output.mp3"), help="File mp3 đầu ra")
    parser.add_argument("--language", "-l", default="vi", help="Ngôn ngữ gTTS")
    parser.add_argument("--threads", "-t", type=int, default=10, help="Số luồng tối đa")
    parser.add_argument("--delay", "-d", type=float, default=2.0, help="Delay (giây) giữa các request")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        print(f"Không tìm thấy file {args.input}")
        sys.exit(1)
    text = args.input.read_text(encoding="utf-8")
    pipeline = TtsPipeline(language=args.language, num_chunks=args.threads, delay_between_requests=args.delay)
    pipeline.run(text, args.output)


if __name__ == "__main__":
    main() 