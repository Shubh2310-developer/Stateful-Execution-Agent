from typing import Any, Dict, Optional
import os
from src.utils.logger import logger

class LocalStorage:
    """Simple local filesystem storage implementation."""

    def __init__(self, base_dir: str = "data/artifacts"):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def _safe_path(self, key: str) -> str:
        """Ensures the resolved path is within the base directory."""
        # Remove leading slashes and handle '..'
        clean_key = os.path.normpath(key).lstrip(os.sep)
        if clean_key.startswith(".."):
            raise ValueError(f"Invalid storage key: {key}")

        full_path = os.path.join(os.path.abspath(self.base_dir), clean_key)
        if not full_path.startswith(os.path.abspath(self.base_dir)):
            raise ValueError(f"Access denied: {key} is outside base directory")
        return full_path

    def put(self, key: str, data: Any) -> str:
        file_path = self._safe_path(key)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        mode = "wb" if isinstance(data, (bytes, bytearray)) else "w"
        encoding = None if "b" in mode else "utf-8"

        with open(file_path, mode, encoding=encoding) as f:
            f.write(data)
        return f"file://{os.path.abspath(file_path)}"

    def get(self, key: str) -> Optional[bytes]:
        try:
            file_path = self._safe_path(key)
        except ValueError:
            return None

        if not os.path.exists(file_path):
            return None

        with open(file_path, "rb") as f:
            return f.read()

    def delete(self, key: str) -> bool:
        """Deletes a file from local storage."""
        try:
            file_path = self._safe_path(key)
        except ValueError:
            return False

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                # Try to remove empty parent directories
                parent = os.path.dirname(file_path)
                abs_base = os.path.abspath(self.base_dir)
                while os.path.abspath(parent) != abs_base and not os.listdir(parent):
                    os.rmdir(parent)
                    parent = os.path.dirname(parent)
                return True
            except Exception as e:
                logger.error(f"Error deleting {file_path}: {e}")
                return False
        return False

    def exists(self, key: str) -> bool:
        """Checks if a key exists in storage."""
        try:
            file_path = self._safe_path(key)
            return os.path.exists(file_path)
        except ValueError:
            return False
