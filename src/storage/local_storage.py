from typing import Any, Dict, Optional
import os
from src.utils.logger import logger

class LocalStorage:
    """Simple local filesystem storage implementation."""

    def __init__(self, base_dir: str = "data/artifacts"):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def put(self, key: str, data: Any):
        file_path = os.path.join(self.base_dir, key)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        mode = "wb" if isinstance(data, bytes) else "w"
        with open(file_path, mode) as f:
            f.write(data)
        return f"file://{os.path.abspath(file_path)}"

    def get(self, key: str) -> Any:
        file_path = os.path.join(self.base_dir, key)
        if not os.path.exists(file_path):
            return None

        with open(file_path, "rb") as f:
            return f.read()
