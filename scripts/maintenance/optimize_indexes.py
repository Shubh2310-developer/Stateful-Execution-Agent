import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.utils.logger import logger

async def optimize():
    """Runs database optimization commands like index rebuilding."""
    logger.info("Starting database optimization...")

    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]

    # Example: Re-index collections
    for coll_name in ["tasks", "state", "trace", "memory"]:
        logger.info(f"Optimizing collection: {coll_name}")
        # await db.command("compact", coll_name)

    print("Database optimization complete.")

if __name__ == "__main__":
    asyncio.run(optimize())
