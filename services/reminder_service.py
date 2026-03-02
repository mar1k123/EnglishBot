import asyncio
import sqlite3
import time

from aiogram import Bot

from services.paths import DB_PATH

REMINDER_CHECK_SECONDS = 10


def ensure_reminders_table() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reminders (
            user_id INTEGER PRIMARY KEY,
            interval_minutes INTEGER NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1,
            next_remind_at INTEGER
        )
        """
    )

    cursor.execute("PRAGMA table_info(reminders)")
    columns = {row[1] for row in cursor.fetchall()}
    if "next_remind_at" not in columns:
        cursor.execute("ALTER TABLE reminders ADD COLUMN next_remind_at INTEGER")

    conn.commit()
    conn.close()


async def reminders_worker(bot: Bot) -> None:
    ensure_reminders_table()
    while True:
        now_ts = int(time.time())
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT user_id, interval_minutes
            FROM reminders
            WHERE enabled = 1
              AND COALESCE(next_remind_at, 0) <= ?
            """,
            (now_ts,),
        )
        due_rows = cursor.fetchall()

        for user_id, interval_minutes in due_rows:
            try:
                await bot.send_message(
                    user_id,
                    "⏰ Пора повторить слова и улучшить прогресс! Используй /check или /check_reverse.",
                )
            except Exception:
                pass

            next_ts = int(time.time()) + interval_minutes * 60
            cursor.execute(
                """
                UPDATE reminders
                SET next_remind_at = ?
                WHERE user_id = ?
                """,
                (next_ts, user_id),
            )

        conn.commit()
        conn.close()
        await asyncio.sleep(REMINDER_CHECK_SECONDS)


def reminder_disable(user_id: int) -> None:
    ensure_reminders_table()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE reminders SET enabled = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def reminder_enable(user_id: int, minutes: int) -> None:
    ensure_reminders_table()
    next_ts = int(time.time()) + minutes * 60
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO reminders (user_id, interval_minutes, enabled, next_remind_at)
        VALUES (?, ?, 1, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET interval_minutes = ?, enabled = 1, next_remind_at = ?
        """,
        (user_id, minutes, next_ts, minutes, next_ts),
    )
    conn.commit()
    conn.close()
