import os
import sqlite3
import math
import re
from collections import Counter
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

DB_PATH = os.path.join("data", "oferty.db")
PER_PAGE = 30

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_dynamic_quick_filters():
    try:
        conn = get_db()
        rows = conn.execute("SELECT title FROM offers").fetchall()
        conn.close()
        if not rows: return []
        
        text = " ".join([r[0] for r in rows]).lower()
        words = re.sub(r'[^\w\s]', '', text).split()
        
        stop_words = {
            'w', 'z', 'i', 'na', 'do', 'o', 'dla', 'oraz', 'od', 'po', 'ze', 'za', 
            'poznan', 'poznań', 'praca', 'oferta', 'pl', 'oferty', 'szukamy'
        }
        
        filtered = [w for w in words if w not in stop_words and len(w) > 3]
        return [w.capitalize() for w in [item[0] for item in Counter(filtered).most_common(5)]]
    except:
        return []

@app.route('/')
def index():
    query = request.args.get('query', '').lower()
    source_filter = request.args.get('source', '')
    sort_by = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    
    try:
        conn = get_db()
        sql_base = "FROM offers WHERE 1=1"
        params = []
        
        if query:
            sql_base += " AND lower(title) LIKE ?"
            params.append(f"%{query}%")
        
        if source_filter:
            sql_base += " AND source_site = ?"
            params.append(source_filter)

        total_items = conn.execute(f"SELECT COUNT(*) {sql_base}", params).fetchone()[0]
        total_pages = math.ceil(total_items / PER_PAGE) if total_items > 0 else 1
        
        order_clause = " ORDER BY title ASC" if sort_by == 'alpha' else " ORDER BY id DESC"
        limit_clause = " LIMIT ? OFFSET ?"
        
        final_params = params + [PER_PAGE, (page - 1) * PER_PAGE]
        offers = conn.execute(f"SELECT title, link, source_site {sql_base} {order_clause} {limit_clause}", final_params).fetchall()
        
        sources = [row[0] for row in conn.execute("SELECT DISTINCT source_site FROM offers").fetchall()]
        conn.close()
        
        page_range = range(max(1, page-2), min(total_pages, page+2) + 1)
        
        return render_template('index.html', 
                               offers=offers, 
                               page=page, 
                               total_pages=total_pages, 
                               total_items=total_items, 
                               sources=sources, 
                               current_query=query, 
                               current_source=source_filter, 
                               current_sort=sort_by,
                               quick_filters=get_dynamic_quick_filters(), 
                               page_range=page_range)
    except Exception as e:
        print(f"Server Error: {e}")
        return "Błąd bazy danych."

@app.route('/stats')
def stats():
    try:
        conn = get_db()
        df = pd.read_sql_query("SELECT title, source_site FROM offers", conn)
        conn.close()
        
        if df.empty: return "Brak danych."
        
        counts = df['source_site'].value_counts().to_dict()
        words = re.sub(r'[^\w\s]', '', " ".join(df['title'].astype(str).str.lower())).split()
        stop_words = {'w', 'z', 'i', 'na', 'do', 'o', 'dla', 'oraz', 'od', 'po', 'ze', 'za'}
        
        top = Counter([w for w in words if w not in stop_words and len(w) > 3]).most_common(10)
        
        return render_template('stats.html', sources=counts, top_keywords=top, max_val=top[0][1] if top else 100)
    except:
        return "Błąd statystyk."

if __name__ == '__main__':
    app.run(debug=True, port=5001)