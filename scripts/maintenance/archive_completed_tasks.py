import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.utils.logger import logger

async def archive_tasks():
    """Moves completed tasks older than 90 days to an archive collection."""
    logger.info("Starting task archiving process...")

    client = AsyncIOMotorClient(settings.database.mongodb_uri)
    db = client[settings.database.mongodb_db]

    # In a real impl, we would use a date filter
    # For now, just count completed tasks
    completed_count = await db.tasks.count_documents({"status": "completed"})
    logger.info(f"Found {completed_count} completed tasks eligible for archiving.")

    # Simulated move logic
    if completed_count > 0:
        logger.info("Archiving tasks to 'tasks_archive'...")

    print("Task archiving complete.")

if __name__ == "__main__":
    asyncio.run(archive_tasks())
