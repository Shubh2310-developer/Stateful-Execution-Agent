from typing import Any, Dict, Optional
import os
from src.utils.logger import logger

class LocalStorage:
    """Simple local filesystem storage implementation."""

    def __init__(self, base_dir: str = "data/artifacts"):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def put(self, key: str, data: Any) -> str:
        file_path = os.path.join(self.base_dir, key)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        mode = "wb" if isinstance(data, (bytes, bytearray)) else "w"
        encoding = None if "b" in mode else "utf-8"

        with open(file_path, mode, encoding=encoding) as f:
            f.write(data)
        return f"file://{os.path.abspath(file_path)}"

    def get(self, key: str) -> Optional[bytes]:
        file_path = os.path.join(self.base_dir, key)
        if not os.path.exists(file_path):
            return None

        with open(file_path, "rb") as f:
            return f.read()

    def delete(self, key: str) -> bool:
        """Deletes a file from local storage."""
        file_path = os.path.join(self.base_dir, key)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                # Try to remove empty parent directories
                parent = os.path.dirname(file_path)
                while parent != self.base_dir and not os.listdir(parent):
                    os.rmdir(parent)
                    parent = os.path.dirname(parent)
                return True
            except Exception as e:
                logger.error(f"Error deleting {file_path}: {e}")
                return False
        return False

    def exists(self, key: str) -> bool:
        """Checks if a key exists in storage."""
        file_path = os.path.join(self.base_dir, key)
        return os.path.exists(file_path)
