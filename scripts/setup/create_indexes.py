import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

async def create_indexes():
    print(f"Connecting to MongoDB at {settings.database.mongodb_uri}...")
    client = AsyncIOMotorClient(settings.database.mongodb_uri)
    db = client[settings.database.mongodb_db]

    # Tasks collection indexes
    print("Creating indexes for 'tasks'...")
    await db.tasks.create_index("user_id")
    await db.tasks.create_index("status")
    await db.tasks.create_index("created_at")

    # State collection indexes
    print("Creating indexes for 'state'...")
    await db.state.create_index("task_id", unique=True)
    await db.state.create_index("version")

    # Trace collection indexes
    print("Creating indexes for 'trace'...")
    await db.trace.create_index("task_id")
    await db.trace.create_index("step_id")
    await db.trace.create_index("timestamp")

    # Artifacts collection indexes
    print("Creating indexes for 'artifacts'...")
    await db.artifacts.create_index("task_id")
    await db.artifacts.create_index("artifact_id", unique=True)

    # User Profiles collection indexes
    print("Creating indexes for 'user_profiles'...")
    await db.user_profiles.create_index("user_id", unique=True)

    # Historical Patterns collection indexes
    print("Creating indexes for 'historical_patterns'...")
    await db.historical_patterns.create_index([("user_id", 1), ("metadata.created_at", -1)])
    await db.historical_patterns.create_index([
        ("goal_request", "text"),
        ("approach", "text"),
        ("tags", "text")
    ], name="historical_patterns_text_index")

    print("Indexes creation complete.")

if __name__ == "__main__":
    asyncio.run(create_indexes())
