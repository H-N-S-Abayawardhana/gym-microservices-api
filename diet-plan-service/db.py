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


def _rebuild_diet_plans_integer_schema(cur) -> None:
    cur.execute(
        """
        SELECT data_type FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'diet_plans'
          AND column_name = 'diet_plan_id';
        """
    )
    row = cur.fetchone()
    if not row or row["data_type"] not in ("text", "character varying"):
        return
    cur.execute("DROP TABLE IF EXISTS diet_plans_new CASCADE;")
    cur.execute(
        """
        CREATE TABLE diet_plans_new (
            diet_plan_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            member_id INTEGER NOT NULL,
            trainer_id INTEGER NOT NULL,
            goal TEXT NOT NULL,
            meal_plan TEXT NOT NULL,
            duration_weeks INTEGER NOT NULL
        );
        """
    )
    cur.execute(
        """
        INSERT INTO diet_plans_new (member_id, trainer_id, goal, meal_plan, duration_weeks)
        SELECT
            CASE
                WHEN trim(member_id::text) ~ '^[0-9]+$' THEN trim(member_id::text)::integer
                ELSE 0
            END,
            CASE
                WHEN trim(trainer_id::text) ~ '^[0-9]+$' THEN trim(trainer_id::text)::integer
                ELSE 0
            END,
            goal,
            meal_plan,
            duration_weeks
        FROM diet_plans;
        """
    )
    cur.execute("DROP TABLE diet_plans CASCADE;")
    cur.execute("ALTER TABLE diet_plans_new RENAME TO diet_plans;")


def init_db() -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            _rebuild_diet_plans_integer_schema(cur)
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS diet_plans (
                    diet_plan_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                    member_id INTEGER NOT NULL,
                    trainer_id INTEGER NOT NULL,
                    goal TEXT NOT NULL,
                    meal_plan TEXT NOT NULL,
                    duration_weeks INTEGER NOT NULL
                );
                """
            )
        conn.commit()
