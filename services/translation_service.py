import asyncio
import re
import time

import requests

STOP_BUTTON_TEXT = "Стоп"
STOP_WORDS = {"stop", "стоп"}
ENGLISH_PATTERN = re.compile(r"^[a-zA-Z\s'-]+$")
RUSSIAN_PATTERN = re.compile(r"^[\u0400-\u04FF\s'-]+$")
TRANSLATION_CACHE_TTL_SECONDS = 1800
_translation_variants_cache: dict[tuple[str, str, str], tuple[float, set[str]]] = {}


def is_stop_requested(text: str | None) -> bool:
    return (text or "").strip().lower() in STOP_WORDS


def suggest_translation_en_ru(word: str) -> str | None:
    """Return a suggested RU translation for EN word or None on any failure."""
    try:
        response = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": word, "langpair": "en|ru"},
            timeout=5,
        )
        response.raise_for_status()
        payload = response.json()
        suggested = (payload.get("responseData", {}) or {}).get("translatedText", "")
        suggested = suggested.strip()
        return suggested or None
    except Exception:
        return None


def _normalize_answer(text: str) -> str:
    normalized = (text or "").strip().lower().replace("ё", "е")
    normalized = re.sub(r"[^a-zа-я0-9\s-]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _extract_candidates(text: str) -> set[str]:
    if not text:
        return set()
    chunks = re.split(r"[,;/]|(?:\s+-\s+)|(?:\s+\|\s+)", text)
    return {_normalize_answer(chunk) for chunk in chunks if _normalize_answer(chunk)}


def _fetch_translation_variants(source_word: str, src_lang: str, dst_lang: str) -> set[str]:
    variants: set[str] = set()
    response = requests.get(
        "https://api.mymemory.translated.net/get",
        params={"q": source_word, "langpair": f"{src_lang}|{dst_lang}"},
        timeout=5,
    )
    response.raise_for_status()
    payload = response.json()

    translated = (payload.get("responseData", {}) or {}).get("translatedText", "")
    variants.update(_extract_candidates(translated))

    for match in payload.get("matches", []) or []:
        variants.update(_extract_candidates(match.get("translation", "")))

    return {item for item in variants if item}


def _get_cached_variants(source_word: str, src_lang: str, dst_lang: str) -> set[str]:
    key = (_normalize_answer(source_word), src_lang, dst_lang)
    now_ts = time.time()
    cached = _translation_variants_cache.get(key)
    if cached and (now_ts - cached[0] <= TRANSLATION_CACHE_TTL_SECONDS):
        return set(cached[1])

    try:
        variants = _fetch_translation_variants(source_word, src_lang, dst_lang)
    except Exception:
        variants = set()

    _translation_variants_cache[key] = (now_ts, variants)
    return set(variants)


async def get_accepted_answers(
    source_word: str,
    base_answer: str,
    src_lang: str,
    dst_lang: str,
) -> set[str]:
    accepted = set(_extract_candidates(base_answer))
    api_variants = await asyncio.to_thread(_get_cached_variants, source_word, src_lang, dst_lang)
    accepted.update(api_variants)
    return accepted
