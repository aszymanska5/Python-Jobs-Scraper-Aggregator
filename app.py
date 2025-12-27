from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import os
import math
from collections import Counter
import re

app = Flask(__name__)

DB_PATH = os.path.join("data", "oferty.db")
ITEMS_PER_PAGE = 30

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    query = request.args.get('query', '').lower()
    source_filter = request.args.get('source', '')
    page = request.args.get('page', 1, type=int)

    try:
        conn = get_db_connection()
        
        sql_query = "SELECT * FROM offers WHERE 1=1"
        params = []

        if query:
            sql_query += " AND lower(title) LIKE ?"
            params.append(f"%{query}%")
        
        if source_filter:
            sql_query += " AND source_site = ?"
            params.append(source_filter)

        count_query = f"SELECT COUNT(*) FROM ({sql_query})"
        total_items = conn.execute(count_query, params).fetchone()[0]
        total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

        sql_query += " ORDER BY created_at DESC"

        offset = (page - 1) * ITEMS_PER_PAGE
        sql_query += " LIMIT ? OFFSET ?"
        params.extend([ITEMS_PER_PAGE, offset])
        
        df = pd.read_sql_query(sql_query, conn, params=params)
        
        sources_df = pd.read_sql_query("SELECT DISTINCT source_site FROM offers", conn)
        sources_list = sources_df['source_site'].tolist()

        conn.close()

        window = 2
        start_page = max(1, page - window)
        end_page = min(total_pages, page + window)
        page_range = range(start_page, end_page + 1)

        offers_data = df.to_dict('records')

        return render_template('index.html', 
                               offers=offers_data, 
                               page=page,
                               total_pages=total_pages,
                               page_range=page_range,
                               total_items=total_items,
                               current_query=query,
                               current_source=source_filter,
                               sources=sources_list)

    except Exception as e:
        return f"Błąd aplikacji: {e}"

@app.route('/stats')
def stats():
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM offers", conn)
        conn.close()
        
        if df.empty: return "Brak danych."

        source_counts = df['source_site'].value_counts().to_dict()
        city_counts = df['city'].value_counts().head(5).to_dict()

        all_titles = df['title'].dropna().astype(str).str.lower().tolist()
        text = " ".join(all_titles)
        
        text = re.sub(r'[^\w\s]', '', text)
        words = text.split()

        stop_words = {
            'w', 'z', 'i', 'na', 'do', 'o', 'dla', 'oraz', 'od', 
            'sp', 'zoo', 'sa', 'gmbh', 'polska', 'poland', 
            'poznan', 'poznań', 'praca', 'oferta', 'undisclosed',
            'unknown', 'pl', 'ul', 'ds', 'specjalista', 'młodszy', 'starszy',
            'manager', 'kierownik', 'pracownik', 'ekspert', 'consultant',
            'senior', 'junior', 'mid', 'regular', 'master', 'st', 'zoo'
        }
        
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        top_keywords = Counter(filtered_words).most_common(10)

        return render_template('stats.html', 
                               sources=source_counts, 
                               cities=city_counts,
                               top_keywords=top_keywords)
    
    except Exception as e:
        return f"Błąd: {e}"

if __name__ == '__main__':
    app.run(debug=True)