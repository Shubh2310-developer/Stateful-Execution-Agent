import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import psycopg2
from src.core.config import settings

async def init_mongodb():
    print(f"Connecting to MongoDB at {settings.MONGODB_URL}...")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]

    # Create collections if they don't exist
    collections = ["tasks", "state", "trace", "artifacts", "memory"]
    for collection in collections:
        if collection not in await db.list_collection_names():
            await db.create_collection(collection)
            print(f"Created collection: {collection}")

    print("MongoDB initialization complete.")

def init_postgresql():
    print(f"Connecting to PostgreSQL at {settings.POSTGRES_SERVER}...")
    try:
        conn = psycopg2.connect(
            host=settings.POSTGRES_SERVER,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            port=settings.POSTGRES_PORT,
            dbname="postgres" # Connect to default db to create our target db
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Check if DB exists
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{settings.POSTGRES_DB}'")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")
            print(f"Created database: {settings.POSTGRES_DB}")

        cur.close()
        conn.close()
        print("PostgreSQL initialization complete.")
    except Exception as e:
        print(f"Error initializing PostgreSQL: {e}")

async def main():
    await init_mongodb()
    init_postgresql()

if __name__ == "__main__":
    asyncio.run(main())
