from __future__ import annotations
"""Pipeline điều phối toàn bộ quá trình: tách –> synth –> ghép –> dọn dẹp."""

from pathlib import Path
from typing import Optional
import logging
import shutil

from .splitter import TextSplitter
from .synthesizer import TtsSynthesizer
from .merger import AudioMerger

logger = logging.getLogger(__name__)


class TtsPipeline:
    """Điều phối quy trình đọc văn bản thành file mp3 duy nhất."""

    def __init__(
        self,
        language: str = "vi",
        num_chunks: int = 10,
        delay_between_requests: float = 2.0,
    ) -> None:
        self.splitter = TextSplitter(num_chunks=num_chunks)
        self.synthesizer = TtsSynthesizer(
            language=language,
            delay_between_requests=delay_between_requests,
            max_workers=num_chunks,
        )
        self.merger = AudioMerger()

    def run(
        self,
        text: str,
        output_path: Path,
        temp_dir: Optional[Path] = None,
    ) -> Path:
        """Chạy toàn bộ pipeline.

        Args:
            text: Nội dung văn bản cần đọc.
            output_path: Đường dẫn file mp3 đầu ra.
            temp_dir: Thư mục tạm; mặc định nằm cạnh output.
        Returns:
            Path: đường dẫn file mp3 đã tạo.
        """
        if temp_dir is None:
            temp_dir = output_path.parent / "temp_audio_chunks"
        temp_dir.mkdir(parents=True, exist_ok=True)

        chunks = self.splitter.split(text)
        logger.info("Đã chia văn bản thành %d chunk", len(chunks))

        temp_files = self.synthesizer.synthesize(chunks, temp_dir)
        logger.info("Hoàn tất sinh %d file tạm", len(temp_files))

        self.merger.merge(temp_files, output_path)

        # Dọn dẹp
        for file in temp_dir.iterdir():
            try:
                file.unlink()
            except OSError:
                logger.warning("Không thể xóa file %s", file)
        shutil.rmtree(temp_dir, ignore_errors=True)
        logger.info("Đã dọn dẹp thư mục tạm")
        return output_path 