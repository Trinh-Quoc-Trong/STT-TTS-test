from __future__ import annotations
"""Module ghép các file mp3 thành một file duy nhất theo đúng thứ tự."""

from pathlib import Path
from typing import List
import time
import logging

from pydub import AudioSegment

logger = logging.getLogger(__name__)


class AudioMerger:
    """Ghép nhiều file mp3 thành 1 file duy nhất."""

    def __init__(self, wait_interval: float = 0.5):
        self.wait_interval = wait_interval

    def merge(self, temp_files: List[Path], output_path: Path) -> None:
        """Ghép *temp_files* theo thứ tự vào *output_path*.

        Chỉ ghép những file thực sự tồn tại.
        """
        combined = AudioSegment.empty()
        for idx, file_path in enumerate(temp_files):
            attempts = 0
            while not file_path.exists() and attempts < 10:
                time.sleep(self.wait_interval)
                attempts += 1
            if not file_path.exists():
                logger.warning("Bỏ qua chunk %s do không tìm thấy file", file_path.name)
                continue
            segment = AudioSegment.from_mp3(file_path.as_posix())
            combined += segment
            logger.info("Đã ghép chunk %s", idx)
        if len(combined) == 0:
            raise RuntimeError("Không có dữ liệu audio để ghép.")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        combined.export(output_path.as_posix(), format="mp3")
        logger.info("Đã lưu file hoàn chỉnh: %s", output_path) 