import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

async def create_indexes():
    print(f"Connecting to MongoDB at {settings.MONGODB_URL}...")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]

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

    # Memory collection indexes
    print("Creating indexes for 'memory'...")
    await db.memory.create_index("user_id", unique=True)

    print("Indexes creation complete.")

if __name__ == "__main__":
    asyncio.run(create_indexes())
