"""
Migration to add versioning support to certain tables.
"""
import psycopg2
from src.core.config import settings

def migrate():
    print("Running migration: 002_add_versioning")
    conn = psycopg2.connect(settings.database.postgres_uri)
    cur = conn.cursor()

    # Add a version column to user_profiles
    cur.execute("""
        ALTER TABLE user_profiles
        ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Migration 002 complete.")

if __name__ == "__main__":
    migrate()
