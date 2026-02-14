import json
from datetime import datetime
from typing import Any

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def to_json(data: Any) -> str:
    return json.dumps(data, cls=DateTimeEncoder)

def from_json(json_str: str) -> Any:
    return json.loads(json_str)
