import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from datetime import datetime

async def seed_data():
    print(f"Connecting to MongoDB at {settings.database.mongodb_uri}...")
    client = AsyncIOMotorClient(settings.database.mongodb_uri)
    db = client[settings.database.mongodb_db]

    # Seed a sample user profile/memory
    user_id = "usr_demo_123"
    print(f"Seeding sample memory for user: {user_id}...")

    sample_memory = {
        "user_id": user_id,
        "profile": {
            "role": "Software Engineer",
            "preferences": {
                "tone": "concise",
                "language": "Python"
            }
        },
        "historical_patterns": [],
        "created_at": datetime.utcnow()
    }

    await db.memory.update_one(
        {"user_id": user_id},
        {"$set": sample_memory},
        upsert=True
    )

    print("Seed data insertion complete.")

if __name__ == "__main__":
    asyncio.run(seed_data())
