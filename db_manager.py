import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join("data", "oferty.db")

def add_offers(df):
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
                    INSERT INTO offers (title, company, city, salary, link, source_site)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    offer['title'],
                    offer['company'],
                    offer['city'],
                    offer['salary'],
                    offer['link'],
                    offer['source_site']
                ))
                added_count += 1
                
            return added_count

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 0