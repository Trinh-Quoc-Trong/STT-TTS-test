# -*- coding: utf-8 -*-
"""
Module để quản lý trạng thái xử lý của các chunk.
"""
import threading

class StatusManager:
    """
    Quản lý, cập nhật và báo cáo trạng thái của từng chunk trong quá trình xử lý.
    Lớp này đảm bảo an toàn luồng (thread-safe).
    """
    def __init__(self, num_chunks: int):
        """
        Khởi tạo StatusManager.

        Args:
            num_chunks (int): Tổng số chunk sẽ được xử lý.
        """
        self.num_chunks = num_chunks
        self.status_report = []
        self.lock = threading.Lock()
        self._initialize_status_report()

    def _initialize_status_report(self):
        """Tạo danh sách báo cáo trạng thái ban đầu."""
        with self.lock:
            self.status_report = [
                {
                    "id": i,
                    "download_status": "Chờ xử lý",
                    "merge_status": "Chờ xử lý",
                    "error": None
                }
                for i in range(self.num_chunks)
            ]

    def get_download_status(self, index: int) -> str:
        """Lấy trạng thái tải về của một chunk một cách an toàn."""
        with self.lock:
            return self.status_report[index]['download_status']

    def update_download_status(self, index: int, status: str, error_msg: str = None):
        """Cập nhật trạng thái tải về của một chunk một cách an toàn."""
        with self.lock:
            self.status_report[index]["download_status"] = status
            if error_msg:
                self.status_report[index]["error"] = error_msg

    def update_merge_status(self, index: int, status: str, error_msg: str = None):
        """Cập nhật trạng thái ghép file của một chunk một cách an toàn."""
        with self.lock:
            self.status_report[index]["merge_status"] = status
            if error_msg:
                self.status_report[index]["error"] = error_msg
    
    def print_summary_table(self):
        """In ra bảng tóm tắt kết quả xử lý."""
        print("\n\n" + "="*80)
        print("TÓM TẮT".center(80))
        print("="*80)
        print(f"| {'Chunk':<5} | {'Trạng thái Tải về':<25} | {'Trạng thái Ghép':<25} | {'Ghi chú':<13} |")
        print(f"|{'-'*7}|{'-'*27}|{'-'*27}|{'-'*15}|")
        
        with self.lock:
            for report in self.status_report:
                chunk_id = report['id'] + 1
                download_status = report['download_status']
                merge_status = report['merge_status']
                error_msg = "Lỗi" if report['error'] else "OK"
                print(f"| {chunk_id:<5} | {download_status:<25} | {merge_status:<25} | {error_msg:<13} |")
        
        print("="*80 + "\n") 