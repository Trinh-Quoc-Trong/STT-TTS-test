from __future__ import annotations
"""Module chia văn bản thành các đoạn nhỏ.

Tất cả ghi chú đều bằng tiếng Việt.
"""

from typing import List


class TextSplitter:
    """Chia văn bản thành nhiều đoạn (chunk) dựa trên số lượng từ."""

    def __init__(self, min_words_threshold: int = 50, num_chunks: int = 10) -> None:
        """Khởi tạo splitter.

        Args:
            min_words_threshold: Nếu tổng số từ ≤ ngưỡng này thì trả về 1 chunk duy nhất.
            num_chunks: Số chunk tối đa sẽ tạo.
        """
        self.min_words_threshold = min_words_threshold
        self.num_chunks = num_chunks

    def split(self, text: str) -> List[str]:
        """Chia *text* thành list các chunk.

        Trả về ít nhất 1 chunk, không bao giờ trả về danh sách rỗng.
        """
        words = text.strip().split()
        total_words = len(words)

        # Nếu văn bản quá ngắn, không cần chia
        if total_words <= self.min_words_threshold or self.num_chunks <= 1:
            return [text.strip()]

        base_size = total_words // self.num_chunks
        remainder = total_words % self.num_chunks

        chunks: List[str] = []
        start_idx = 0
        for i in range(self.num_chunks):
            add_one = 1 if i < remainder else 0
            end_idx = start_idx + base_size + add_one
            chunk_words = words[start_idx:end_idx]
            if chunk_words:
                chunks.append(" ".join(chunk_words))
            start_idx = end_idx

        return chunks 