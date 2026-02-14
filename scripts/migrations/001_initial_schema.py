"""
Initial database schema migration.
This script sets up the baseline PostgreSQL tables.
"""
import psycopg2
from src.core.config import settings

def migrate():
    print("Running migration: 001_initial_schema")
    conn = psycopg2.connect(settings.database.postgres_uri)
    cur = conn.cursor()

    # Create a simple table for relational data example
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(50) UNIQUE NOT NULL,
            full_name VARCHAR(100),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Migration 001 complete.")

if __name__ == "__main__":
    migrate()
