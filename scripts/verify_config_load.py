import sys
import os
from pathlib import Path

# Add project root to python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.config import settings

def verify_config():
    print("Verifying Configuration Loading...")
    print(f"Environment: {settings.app.env}")
    
    # Check MongoDB
    mongo_uri = settings.database.mongodb_uri
    print(f"MongoDB URI: {mongo_uri}")
    if "mongodb+srv" in mongo_uri and "engunity" in mongo_uri:
        print("✅ MongoDB URI loaded correctly from .env")
    else:
        print("❌ MongoDB URI mismatch (using default?)")

    # Check Postgres
    pg_uri = settings.database.postgres_uri
    print(f"Postgres URI: {pg_uri}")
    if "supabase.com" in pg_uri:
        print("✅ Postgres URI loaded correctly from .env")
    else:
        print("❌ Postgres URI mismatch (using default?)")
        
    # Check Redis
    redis_uri = settings.cache.redis_uri
    print(f"Redis URI: {redis_uri}")
    
    print("\nVerification Complete.")

if __name__ == "__main__":
    verify_config()
