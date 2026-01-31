import sqlite3
import os
from config import DB_PATH, DB_FOLDER_PATH

def run_setup():
    if not os.path.exists(DB_FOLDER_PATH):
        os.makedirs(DB_FOLDER_PATH)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                link TEXT UNIQUE,
                source_site TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            print(f"[Database] Initialized at: {DB_PATH}")
            
    except sqlite3.Error as e:
        print(f"[Database] Error: {e}")

if __name__ == '__main__':
    run_setup()