import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path

# Define paths
DATA_DIR = Path("../../DATA")
DB_PATH = DATA_DIR/"intelligence_platform.db"

# Create DATA folder if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

conn=sqlite3.connect('../../DATA/intelligence_platform.db')
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user')""")

conn.commit()

print(" Imports successful!")
print(f" DATA folder: {DATA_DIR.resolve()}")
print(f" This will destroy the pc. Database will be created at: {DB_PATH.resolve()}")