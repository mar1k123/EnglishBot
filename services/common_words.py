import csv
import random
from typing import Dict, List, Optional, Tuple

from database import init_common_words

from .paths import COMMON_WORDS_CSV


_used_common_words: dict[str, set[Tuple[str, str]]] = {}


def get_common_words(level: str) -> Dict[str, str]:
    words: Dict[str, str] = {}
    with open(COMMON_WORDS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["level"] == level:
                words[row["english"]] = row["russian"]
    return words


def get_random_common_word(level: str) -> Optional[Tuple[str, str]]:
    if level not in _used_common_words:
        _used_common_words[level] = set()

    try:
        with open(COMMON_WORDS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            all_words = [
                (row["english"], row["russian"])
                for row in reader
                if row["level"] == level
            ]
    except FileNotFoundError:
        init_common_words()
        with open(COMMON_WORDS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            all_words = [
                (row["english"], row["russian"])
                for row in reader
                if row["level"] == level
            ]

    if not all_words:
        return None

    available_words = [w for w in all_words if w not in _used_common_words[level]]

    if not available_words:
        _used_common_words[level] = set()
        available_words = all_words

    chosen_word = random.choice(available_words)
    _used_common_words[level].add(chosen_word)
    return chosen_word


def get_available_levels() -> List[str]:
    levels = set()
    try:
        with open(COMMON_WORDS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "level" in row:
                    levels.add(row["level"])
    except FileNotFoundError:
        init_common_words()
        return get_available_levels()
    except Exception:
        return []

    return sorted(levels, key=lambda x: (x[0], int(x[1])))

