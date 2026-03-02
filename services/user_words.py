import random
import sqlite3
from typing import Dict, Optional

from .paths import DB_PATH


_used_user_words: dict[int, set[str]] = {}


def user_exists(user_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def add_user(user_id: int) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()


def add_word(user_id: int, aword: str, rword: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO words (user_id, aword, rword) VALUES (?, ?, ?)",
        (user_id, aword, rword),
    )
    conn.commit()
    conn.close()


def get_user_words(user_id: int) -> Dict[str, str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT aword, rword FROM words WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return {aword: rword for aword, rword in rows} if rows else {}


def get_random_aword(user_id: int) -> Optional[str]:
    if user_id not in _used_user_words:
        _used_user_words[user_id] = set()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    used = _used_user_words[user_id]

    if used:
        placeholders = ",".join(["?"] * len(used))
        cursor.execute(
            f"""
            SELECT aword FROM words
            WHERE user_id = ? AND aword NOT IN ({placeholders})
            """,
            (user_id, *used),
        )
    else:
        cursor.execute(
            "SELECT aword FROM words WHERE user_id = ?",
            (user_id,),
        )

    available_words = cursor.fetchall()

    if not available_words:
        _used_user_words[user_id] = set()
        conn.close()
        return None

    chosen_word = random.choice(available_words)[0]
    _used_user_words[user_id].add(chosen_word)
    conn.close()
    return chosen_word


def get_rword_by_aword(user_id: int, aword: str) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT rword FROM words WHERE user_id = ? AND aword = ?",
        (user_id, aword),
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

