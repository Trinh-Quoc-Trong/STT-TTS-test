from __future__ import annotations
"""Module quản lý việc chuyển văn bản → giọng nói bằng gTTS ở chế độ đa luồng.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Sequence
import time

from gtts import gTTS


class TtsSynthesizer:
    """Bao bọc gTTS và sinh các file âm thanh tạm từ danh sách chunk."""

    def __init__(
        self,
        language: str = "vi",
        delay_between_requests: float = 2.0,
        max_workers: int | None = 10,
    ) -> None:
        self.language = language
        self.delay_between_requests = delay_between_requests
        self.max_workers = max_workers

    def _synthesize_chunk(self, text_chunk: str, index: int, output_dir: Path) -> Path:
        """Tạo file mp3 tạm từ *text_chunk* và trả về đường dẫn."""
        if not text_chunk:
            raise ValueError("Chunk văn bản rỗng.")

        # Dàn cách để tránh rate-limit
        sleep_time = index * self.delay_between_requests
        if sleep_time > 0:
            time.sleep(sleep_time)

        tmp_path = output_dir / f"temp_{index}.mp3"
        tmp_path_tmp = tmp_path.with_suffix(".mp3.tmp")

        tts = gTTS(text=text_chunk, lang=self.language, slow=False)
        tts.save(tmp_path_tmp.as_posix())

        # Đổi tên file .tmp sang mp3 chính thức
        tmp_path_tmp.rename(tmp_path)
        return tmp_path

    def synthesize(self, chunks: Sequence[str], output_dir: Path) -> List[Path]:
        """Sinh file âm thanh từ *chunks* và trả về list đường dẫn."""
        output_dir.mkdir(parents=True, exist_ok=True)
        results: List[Path] = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._synthesize_chunk, chunk, idx, output_dir): idx
                for idx, chunk in enumerate(chunks)
            }
            for future in as_completed(futures):
                path = future.result()
                results.append(path)
        # Sắp xếp theo thứ tự index
        results.sort(key=lambda p: int(p.stem.split("_")[1]))
        return results 