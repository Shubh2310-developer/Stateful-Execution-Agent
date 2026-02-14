from motor.motor_asyncio import AsyncIOMotorClient
import psycopg2
from src.core.config import settings
from src.utils.logger import logger

def get_mongodb_client():
    """Dependency for obtaining a MongoDB client."""
    client = AsyncIOMotorClient(settings.database.mongodb_uri)
    try:
        yield client
    finally:
        client.close()

def get_mongodb_db():
    """Dependency for obtaining the MongoDB database."""
    client = AsyncIOMotorClient(settings.database.mongodb_uri)
    db = client[settings.database.mongodb_db]
    try:
        yield db
    finally:
        client.close()

def get_postgresql_conn():
    """Dependency for obtaining a PostgreSQL connection."""
    conn = psycopg2.connect(settings.database.postgres_uri)
    try:
        yield conn
    finally:
        conn.close()
