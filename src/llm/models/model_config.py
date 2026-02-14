from typing import Dict, Any

MODELS: Dict[str, Dict[str, Any]] = {
    "mixtral-8x7b-32768": {
        "provider": "groq",
        "max_tokens": 32768,
        "context_window": 32768,
    },
    "llama3-70b-8192": {
        "provider": "groq",
        "max_tokens": 8192,
        "context_window": 8192,
    },
    "llama3-8b-8192": {
        "provider": "groq",
        "max_tokens": 8192,
        "context_window": 8192,
    },
    "gemma-7b-it": {
        "provider": "groq",
        "max_tokens": 8192,
        "context_window": 8192,
    },
    "llama-3.3-70b-versatile": {
        "provider": "groq",
        "max_tokens": 32768,
        "context_window": 128000,
    }
}

DEFAULT_MODEL = "llama-3.3-70b-versatile"
