from motor.motor_asyncio import AsyncIOMotorClient
import psycopg2
from src.core.config import settings
from src.utils.logger import logger

def get_mongodb_client():
    """Dependency for obtaining a MongoDB client."""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    try:
        yield client
    finally:
        client.close()

def get_mongodb_db():
    """Dependency for obtaining the MongoDB database."""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    try:
        yield db
    finally:
        client.close()

def get_postgresql_conn():
    """Dependency for obtaining a PostgreSQL connection."""
    conn = psycopg2.connect(
        host=settings.POSTGRES_SERVER,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        port=settings.POSTGRES_PORT,
        dbname=settings.POSTGRES_DB
    )
    try:
        yield conn
    finally:
        conn.close()
