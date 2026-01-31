import sqlite3
import os
import pandas as pd
from config import DB_PATH

def get_connection():
    """Tworzy połączenie z bazą danych i dba o folder data."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicjalizuje tabelę ofert. Wywoływane przez main.py."""
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
    """Dodaje nową ofertę. Zwraca True jeśli dodano, False jeśli duplikat."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO offers (title, link, source_site)
            VALUES (?, ?, ?)
        ''', (offer['title'], offer['link'], offer['source_site']))
        conn.commit()
        added = cursor.rowcount > 0
        return added
    except Exception as e:
        print(f"[DB] Błąd zapisu: {e}")
        return False
    finally:
        conn.close()

def get_all_offers_as_df():
    """Pobiera dane dla serwera Flask jako DataFrame."""
    conn = get_connection()
    query = "SELECT * FROM offers ORDER BY created_at DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_all_offers():
    """Zwraca surową listę wierszy (kompatybilność wsteczna)."""
    conn = get_connection()
    offers = conn.execute('SELECT * FROM offers ORDER BY created_at DESC').fetchall()
    conn.close()
    return offers