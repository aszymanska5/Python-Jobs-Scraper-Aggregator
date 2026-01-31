import sqlite3
import os
import pandas as pd
from config import DB_PATH

def get_connection():
    folder = os.path.dirname(DB_PATH)
    if not os.path.exists(folder):
        os.makedirs(folder)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            source_site TEXT NOT NULL,
            date_scraped TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_offers(df):
    if df.empty:
        return 0

    init_db()

    conn = get_connection()
    cursor = conn.cursor()
    
    new_count = 0
    
    offers_list = df.to_dict('records')

    for offer in offers_list:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO job_offers (title, link, source_site)
                VALUES (?, ?, ?)
            ''', (offer['title'], offer['link'], offer['source_site']))

            if cursor.rowcount > 0:
                new_count += 1
        except Exception as e:
            print(f"[DB Error] {e}")

    conn.commit()
    conn.close()
    
    return new_count