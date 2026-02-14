from datetime import datetime, timezone
from typing import Optional

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

def format_datetime(dt: datetime) -> str:
    return dt.isoformat()

def parse_datetime(dt_str: str) -> datetime:
    return datetime.fromisoformat(dt_str)

def get_timestamp() -> int:
    return int(datetime.now(timezone.utc).timestamp())
