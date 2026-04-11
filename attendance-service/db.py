import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv(Path(__file__).resolve().parent / ".env")

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_uHperkBa69YP@ep-lucky-grass-a4fsyq58-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require").strip()


def _require_database_url() -> str:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set for attendance-service.")
    return DATABASE_URL


def get_conn():
    return psycopg.connect(_require_database_url(), row_factory=dict_row)


def _table_columns(cur, table: str) -> set[str]:
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s;
        """,
        (table,),
    )
    return {row["column_name"] for row in cur.fetchall()}


def _migrate_legacy_attendance(cur) -> None:
    cols = _table_columns(cur, "attendance")
    if "checked_in_at" not in cols:
        return

    cur.execute(
        "ALTER TABLE attendance ADD COLUMN IF NOT EXISTS trainer_id INTEGER DEFAULT 0;"
    )
    cur.execute(
        "ALTER TABLE attendance ADD COLUMN IF NOT EXISTS session_type TEXT DEFAULT 'gym';"
    )
    cur.execute(
        "ALTER TABLE attendance ADD COLUMN IF NOT EXISTS date_col TEXT DEFAULT '1970-01-01';"
    )
    cur.execute(
        "ALTER TABLE attendance ADD COLUMN IF NOT EXISTS check_in_time TEXT DEFAULT '00:00';"
    )
    cur.execute(
        "ALTER TABLE attendance ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'present';"
    )

    cur.execute(
        """
        UPDATE attendance
        SET date_col = left(checked_in_at, 10)
        WHERE checked_in_at IS NOT NULL AND length(trim(checked_in_at)) >= 10;
        """
    )
    cur.execute(
        """
        UPDATE attendance
        SET check_in_time = substring(checked_in_at from 12 for 5)
        WHERE checked_in_at LIKE '%T%' AND length(checked_in_at) >= 16;
        """
    )

    cur.execute(
        """
        ALTER TABLE attendance
        ALTER COLUMN member_id TYPE INTEGER
        USING (
            CASE
                WHEN trim(member_id) ~ '^[0-9]+$' THEN trim(member_id)::integer
                WHEN nullif(regexp_replace(trim(member_id), '[^0-9]', '', 'g'), '') IS NOT NULL
                THEN regexp_replace(trim(member_id), '[^0-9]', '', 'g')::integer
                ELSE 0
            END
        );
        """
    )

    cur.execute("ALTER TABLE attendance DROP COLUMN IF EXISTS checked_in_at;")
    cur.execute('ALTER TABLE attendance RENAME COLUMN date_col TO "date";')

    cur.execute("ALTER TABLE attendance ALTER COLUMN trainer_id DROP DEFAULT;")
    cur.execute("ALTER TABLE attendance ALTER COLUMN session_type DROP DEFAULT;")
    cur.execute("ALTER TABLE attendance ALTER COLUMN date DROP DEFAULT;")
    cur.execute("ALTER TABLE attendance ALTER COLUMN check_in_time DROP DEFAULT;")
    cur.execute("ALTER TABLE attendance ALTER COLUMN status DROP DEFAULT;")

    cur.execute("ALTER TABLE attendance ALTER COLUMN trainer_id SET NOT NULL;")
    cur.execute("ALTER TABLE attendance ALTER COLUMN session_type SET NOT NULL;")
    cur.execute("ALTER TABLE attendance ALTER COLUMN date SET NOT NULL;")
    cur.execute("ALTER TABLE attendance ALTER COLUMN check_in_time SET NOT NULL;")
    cur.execute("ALTER TABLE attendance ALTER COLUMN status SET NOT NULL;")


def _rebuild_attendance_integer_pk(cur) -> None:
    cur.execute(
        """
        SELECT data_type FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'attendance'
          AND column_name = 'id';
        """
    )
    row = cur.fetchone()
    if not row or row["data_type"] not in ("text", "character varying"):
        return
    _migrate_legacy_attendance(cur)
    cur.execute("DROP TABLE IF EXISTS attendance_new CASCADE;")
    cur.execute(
        """
        CREATE TABLE attendance_new (
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            member_id INTEGER NOT NULL,
            trainer_id INTEGER NOT NULL,
            session_type TEXT NOT NULL,
            "date" TEXT NOT NULL,
            check_in_time TEXT NOT NULL,
            status TEXT NOT NULL
        );
        """
    )
    cur.execute(
        """
        INSERT INTO attendance_new (member_id, trainer_id, session_type, "date", check_in_time, status)
        SELECT member_id, trainer_id, session_type, "date", check_in_time, status
        FROM attendance;
        """
    )
    cur.execute("DROP TABLE attendance CASCADE;")
    cur.execute("ALTER TABLE attendance_new RENAME TO attendance;")


def init_db() -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            _rebuild_attendance_integer_pk(cur)
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                    member_id INTEGER NOT NULL,
                    trainer_id INTEGER NOT NULL,
                    session_type TEXT NOT NULL,
                    "date" TEXT NOT NULL,
                    check_in_time TEXT NOT NULL,
                    status TEXT NOT NULL
                );
                """
            )
            _migrate_legacy_attendance(cur)
        conn.commit()
