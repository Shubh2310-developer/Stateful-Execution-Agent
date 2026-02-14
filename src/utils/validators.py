import re
from typing import Any, Dict, List, Optional
from src.core.exceptions import ValidationError

def validate_user_id(user_id: str):
    if not user_id or not isinstance(user_id, str):
        raise ValidationError("Invalid user_id")

def validate_task_id(task_id: str):
    if not task_id or not isinstance(task_id, str):
        raise ValidationError("Invalid task_id")

def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))
