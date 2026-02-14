from typing import Any, Dict, Optional
from src.utils.logger import logger

class Compression:
    """Utility for compressing and decompressing large state payloads."""

    @staticmethod
    def compress(data: str) -> bytes:
        # Simulated compression (e.g., using zlib or gzip)
        return data.encode("utf-8")

    @staticmethod
    def decompress(compressed_data: bytes) -> str:
        # Simulated decompression
        return compressed_data.decode("utf-8")
