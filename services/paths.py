from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = str(BASE_DIR / "vocabulary_bot.db")
COMMON_WORDS_CSV = str(BASE_DIR / "common_words.csv")

