import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join("data", "oferty.db")

def inspect_db():
    if not os.path.exists(DB_PATH):
        print("Database file not found!")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        
        df = pd.read_sql_query("SELECT * FROM offers", conn)
        
        print(f"--- DATABASE INSPECTION ---")
        print(f"Database Path: {DB_PATH}")
        print(f"Total rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print("-" * 30)
        
        if not df.empty:
            print("Counts by Source Site:")
            print(df['source_site'].value_counts())
            
            print("\n--- SAMPLE DATA (First 5 rows) ---")
            print(df[['id', 'title', 'source_site', 'link']].head(5))
            
            print("\n--- DATA INTEGRITY CHECK ---")
            duplicates = df.duplicated(subset=['link']).sum()
            print(f"Duplicate links found: {duplicates}")
            
        else:
            print("Table 'offers' is empty.")

        conn.close()

    except Exception as e:
        print(f"Error reading database: {e}")

if __name__ == "__main__":
    inspect_db()