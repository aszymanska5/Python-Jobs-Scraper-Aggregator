import sqlite3
import pandas as pd
from config import DB_PATH

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_offers(df: pd.DataFrame) -> int:
    if df.empty:
        return 0

    offers_list = df.to_dict('records')

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            added_count = 0
            
            for offer in offers_list:
                cursor.execute("SELECT id FROM offers WHERE link = ?", (offer['link'],))
                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO offers (title, link, source_site)
                    VALUES (?, ?, ?)
                """, (
                    offer['title'],
                    offer['link'],
                    offer['source_site']
                ))
                added_count += 1
                
            return added_count

    except sqlite3.Error as e:
        print(f"[DB Manager] Error: {e}")
        return 0