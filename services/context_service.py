import html
import random
import re
import time

import requests

CONTEXT_CACHE_TTL_SECONDS = 1800
_context_sentence_cache: dict[str, tuple[float, str]] = {}


def _cleanup_context_sentence(sentence: str, word: str) -> str:
    cleaned = re.sub(r"\s+", " ", (sentence or "").strip())
    if not cleaned:
        return ""
    if len(cleaned) > 220:
        return ""
    word_re = rf"\b{re.escape(word.lower())}(?:'s|s)?\b"
    if not re.search(word_re, cleaned.lower()):
        return ""
    return cleaned


def _fetch_context_sentence_from_dictionary(word: str) -> str | None:
    response = requests.get(
        f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
        timeout=5,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list):
        return None

    candidates: list[str] = []
    for entry in payload:
        for meaning in (entry.get("meanings") or []):
            for definition in (meaning.get("definitions") or []):
                example = definition.get("example")
                if isinstance(example, str):
                    cleaned = _cleanup_context_sentence(example, word)
                    if cleaned:
                        candidates.append(cleaned)
    if not candidates:
        return None
    candidates.sort(key=len)
    return candidates[0]


def _build_context_sentence_fallback(word: str) -> str:
    templates = [
        "I use this {word} every day.",
        "I saw a {word} near my home yesterday.",
        "This {word} is very important for my work.",
        "Can you show me your {word}?",
        "We talked about this {word} in class.",
    ]
    return random.choice(templates).format(word=word)


def highlight_target_word(sentence: str, word: str) -> str:
    escaped_sentence = html.escape(sentence or "")
    escaped_word = html.escape((word or "").strip())
    if not escaped_word:
        return escaped_sentence

    pattern = re.compile(rf"(?i)\b({re.escape(escaped_word)}(?:'s|s)?)\b")
    return pattern.sub(r"<b>\1</b>", escaped_sentence)


def get_context_sentence(word: str) -> str:
    normalized_word = (word or "").strip().lower()
    if not normalized_word:
        return ""

    now_ts = time.time()
    cached = _context_sentence_cache.get(normalized_word)
    if cached and (now_ts - cached[0] <= CONTEXT_CACHE_TTL_SECONDS):
        return cached[1]

    sentence = ""
    try:
        sentence = _fetch_context_sentence_from_dictionary(normalized_word) or ""
    except Exception:
        sentence = ""
    if not sentence:
        sentence = _build_context_sentence_fallback(normalized_word)

    _context_sentence_cache[normalized_word] = (now_ts, sentence)
    return sentence
