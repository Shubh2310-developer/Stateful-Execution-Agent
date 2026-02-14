import zlib
import base64
from typing import Any, Dict, Optional, Union
from src.utils.logger import logger

class Compression:
    """Utility for compressing and decompressing large state payloads."""

    @staticmethod
    def compress(data: str) -> bytes:
        """Compresses a string using zlib."""
        try:
            return zlib.compress(data.encode("utf-8"))
        except Exception as e:
            logger.error(f"Compression failed: {str(e)}")
            return data.encode("utf-8")

    @staticmethod
    def decompress(compressed_data: bytes) -> str:
        """Decompresses zlib-compressed bytes back to a string."""
        try:
            return zlib.decompress(compressed_data).decode("utf-8")
        except Exception as e:
            logger.error(f"Decompression failed: {str(e)}")
            # Fallback if it wasn't actually compressed
            try:
                return compressed_data.decode("utf-8")
            except:
                raise e

    @staticmethod
    def to_base64(data: bytes) -> str:
        """Encodes bytes to a base64 string for JSON storage if needed."""
        return base64.b64encode(data).decode("utf-8")

    @staticmethod
    def from_base64(b64_str: str) -> bytes:
        """Decodes a base64 string back to bytes."""
        return base64.b64decode(b64_str)
