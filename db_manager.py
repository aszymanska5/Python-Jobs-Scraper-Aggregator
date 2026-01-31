import sqlite3
import os
import pandas as pd
from config import DB_PATH

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            source_site TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print(f"[DB] Baza danych gotowa: {DB_PATH}")

def add_offer(offer):
    conn = get_connection()
    cursor = conn.cursor()
    
    clean_link = offer['link'].split('#')[0]
    clean_link = clean_link.split('?')[0]

    try:
        cursor.execute('''
            INSERT OR IGNORE INTO offers (title, link, source_site)
            VALUES (?, ?, ?)
        ''', (offer['title'], clean_link, offer['source_site']))
        conn.commit()
        added = cursor.rowcount > 0
        return added
    except Exception as e:
        print(f"[DB] Błąd zapisu: {e}")
        return False
    finally:
        conn.close()

def get_all_offers_as_df():
    conn = get_connection()
    query = "SELECT * FROM offers ORDER BY created_at DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df