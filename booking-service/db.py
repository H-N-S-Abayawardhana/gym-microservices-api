import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row


load_dotenv(Path(__file__).resolve().parent / ".env")

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_nHXgF5mRI9Cj@ep-polished-moon-a4qwkac1-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require").strip()


def _require_database_url() -> str:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set for booking-service.")
    return DATABASE_URL


def get_conn():
    return psycopg.connect(_require_database_url(), row_factory=dict_row)


def init_db() -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id SERIAL PRIMARY KEY,
                    member_id INTEGER NOT NULL,
                    trainer_id INTEGER NOT NULL,
                    session_date TEXT NOT NULL,
                    session_time TEXT NOT NULL,
                    booking_status TEXT NOT NULL
                        CHECK (booking_status IN ('Confirmed', 'Cancelled'))
                );
                """
            )
        conn.commit()
