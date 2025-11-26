import sqlite3
from pathlib import Path

# Get project root → 'courseworkattempt'
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "DATA"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "intelligence_platform.db"

def connect_database():
    """Connect to SQLite database."""
    return sqlite3.connect(str(DB_PATH))

