
from src.core.config import settings

def verify_rate_limit_config():
    print(f"Rate Limit Enabled: {settings.ratelimit.enabled}")
    print(f"Requests Per Minute: {settings.ratelimit.requests_per_minute}")
    
    expected = 3000
    if settings.ratelimit.requests_per_minute == expected:
        print("SUCCESS: Rate limit Config matches expected default.")
    else:
        print(f"FAILURE: Expected {expected}, got {settings.ratelimit.requests_per_minute}")

if __name__ == "__main__":
    verify_rate_limit_config()
