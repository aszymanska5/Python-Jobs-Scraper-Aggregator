import sqlite3
import os

DB_FOLDER = 'data'
DB_FILE = 'oferty.db'
DB_PATH = os.path.join(DB_FOLDER, DB_FILE)

def create_database():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
        print(f"Created folder: {DB_FOLDER}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS offers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT,
        city TEXT,
        salary TEXT,
        link TEXT UNIQUE,
        source_site TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    conn.close()
    print(f"Database ready at: {DB_PATH}")

if __name__ == '__main__':
    create_database()