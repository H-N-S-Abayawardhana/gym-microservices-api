import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv(Path(__file__).resolve().parent / ".env")

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_2EgomUnWVuR6@ep-muddy-frost-amee30pa-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require").strip()


def _require_database_url() -> str:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set for member-service.")
    return DATABASE_URL


def get_conn():
    return psycopg.connect(_require_database_url(), row_factory=dict_row)


def init_db() -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS members (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT NOT NULL,
                    membership_type TEXT NOT NULL,
                    age INTEGER
                );
                """
            )
        conn.commit()
