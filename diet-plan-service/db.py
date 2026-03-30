import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv(Path(__file__).resolve().parent / ".env")

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_2yRfBpirc6KG@ep-summer-recipe-amjuq9yc-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require").strip()


def _require_database_url() -> str:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set for diet-plan-service.")
    return DATABASE_URL


def get_conn():
    return psycopg.connect(_require_database_url(), row_factory=dict_row)


def init_db() -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS diet_plans (
                    diet_plan_id TEXT PRIMARY KEY,
                    member_id TEXT NOT NULL,
                    trainer_id TEXT NOT NULL,
                    goal TEXT NOT NULL,
                    meal_plan TEXT NOT NULL,
                    duration_weeks INTEGER NOT NULL
                );
                """
            )
        conn.commit()
