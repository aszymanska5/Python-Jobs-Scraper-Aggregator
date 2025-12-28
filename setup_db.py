import sqlite3
import os

DB_FOLDER = 'data'
DB_FILE = 'oferty.db'
DB_PATH = os.path.join(DB_FOLDER, DB_FILE)

def create_database():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)

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
    create_database()