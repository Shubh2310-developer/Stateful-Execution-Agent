import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import psycopg2
from src.core.config import settings

async def init_mongodb():
    print(f"Connecting to MongoDB at {settings.database.mongodb_uri}...")
    client = AsyncIOMotorClient(settings.database.mongodb_uri)
    db = client[settings.database.mongodb_db]

    # Create collections if they don't exist
    collections = ["tasks", "task_versions", "trace", "artifacts", "memory"]
    for collection in collections:
        if collection not in await db.list_collection_names():
            await db.create_collection(collection)
            print(f"Created collection: {collection}")

    print("MongoDB initialization complete.")

def init_postgresql():
    print(f"Connecting to PostgreSQL...")
    try:
        # We need to parse the postgres_uri to get the DB name for creation check
        # For simplicity, assuming the connection works if the DB exists
        conn = psycopg2.connect(settings.database.postgres_uri)
        conn.close()
        print("PostgreSQL connection verified.")
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")

async def main():
    await init_mongodb()
    init_postgresql()

if __name__ == "__main__":
    asyncio.run(main())
