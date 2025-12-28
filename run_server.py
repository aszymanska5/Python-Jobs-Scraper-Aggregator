import math
from flask import Flask, render_template, request
from config import ITEMS_PER_PAGE
from db_manager import get_db_connection
from analytics import get_dynamic_quick_filters, get_stats_data

app = Flask(__name__)

@app.route('/')
def index():
    query = request.args.get('query', '').strip()
    source_filter = request.args.get('source', '')
    sort_by = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    
    conn = get_db_connection()
    
    sql_query = "SELECT COUNT(*) FROM offers WHERE 1=1"
    params = []

    if query:
        sql_query += " AND title LIKE ?"
        params.append(f"%{query}%")
    
    if source_filter:
        sql_query += " AND source_site = ?"
        params.append(source_filter)

    total_items = conn.execute(sql_query, params).fetchone()[0]
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    page = max(1, min(page, total_pages)) if total_pages > 0 else 1

    sql_query = "SELECT * FROM offers WHERE 1=1"
    
    if query:
        sql_query += " AND title LIKE ?"
    
    if source_filter:
        sql_query += " AND source_site = ?"

    if sort_by == 'az':
        sql_query += " ORDER BY title ASC"
    else:
        sql_query += " ORDER BY id DESC"

    sql_query += " LIMIT ? OFFSET ?"
    params.extend([ITEMS_PER_PAGE, (page - 1) * ITEMS_PER_PAGE])

    offers_paginated = conn.execute(sql_query, params).fetchall()
    
    sources = [row[0] for row in conn.execute("SELECT DISTINCT source_site FROM offers").fetchall()]
    conn.close()

    page_range = range(max(1, page - 2), min(total_pages + 1, page + 3))

    return render_template('index.html', 
                           offers=offers_paginated, 
                           page=page, 
                           total_pages=total_pages, 
                           total_items=total_items, 
                           sources=sources, 
                           current_query=query, 
                           current_source=source_filter, 
                           current_sort=sort_by,
                           quick_filters=get_dynamic_quick_filters(), 
                           page_range=page_range)

@app.route('/stats')
def stats():
    counts, top_keywords = get_stats_data()
    
    if not counts:
        return "Brak danych do wyświetlenia."
        
    max_val = top_keywords[0][1] if top_keywords else 1
    
    return render_template('stats.html', 
                           sources=counts, 
                           top_keywords=top_keywords, 
                           max_val=max_val)

if __name__ == '__main__':
    app.run(debug=True, port=5001)