from flask import Flask, render_template, request, send_file
import sqlite3
import pandas as pd
import io
import math
import os
import re
from collections import Counter
from config import DB_NAME, ITEMS_PER_PAGE

app = Flask(__name__)

SEARCH_KEYWORDS = [
    "python", "java", "sql", "javascript", "react", "docker", "aws", "azure", 
    "linux", "c++", "c#", ".net", "php", "angular", "node", "jira", "git",
    "scrum", "devops", "tester", "data", "junior", "senior", "mid", "remote",
    "hybrid", "admin", "support", "helpdesk", "security", "cloud"
]

def regexp(expr, item):
    try:
        if item is None:
            return False
        reg = re.compile(expr, re.IGNORECASE)
        return reg.search(item) is not None
    except Exception:
        return False

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.create_function("REGEXP", 2, regexp)
    return conn

def get_dynamic_filters(limit=5):
    conn = get_db_connection()
    try:
        titles_query = conn.execute("SELECT title FROM job_offers").fetchall()
    except sqlite3.OperationalError:
        conn.close()
        return ["Python", "Data", "Junior", "Remote"]

    conn.close()

    if not titles_query:
        return ["Python", "Data", "Junior", "Remote"]

    all_text = " ".join([row['title'] for row in titles_query]).lower()
    
    keyword_counts = Counter()
    for kw in SEARCH_KEYWORDS:
        pattern = fr'\b{re.escape(kw)}\b'
        matches = re.findall(pattern, all_text)
        count = len(matches)
        if count > 0:
            keyword_counts[kw] = count

    top_keywords = [item[0].capitalize() for item in keyword_counts.most_common(limit)]
    
    if not top_keywords:
        return ["Python", "Data", "Junior", "Remote"]
        
    return top_keywords

@app.route("/")
def index():
    search_query = request.args.get('query', '')
    source_filter = request.args.get('source', '')
    sort_option = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    
    offset = (page - 1) * ITEMS_PER_PAGE

    conn = get_db_connection()
    
    query = "SELECT * FROM job_offers WHERE 1=1"
    params = []

    if search_query:
        keywords = search_query.split()
        for word in keywords:
            query += " AND title REGEXP ?"
            params.append(fr'\b{re.escape(word)}\b')
    
    if source_filter:
        query += " AND source_site = ?"
        params.append(source_filter)

    if sort_option == 'az':
        query += " ORDER BY title ASC"
    else:
        query += " ORDER BY date_scraped DESC"

    query += " LIMIT ? OFFSET ?"
    params.extend([ITEMS_PER_PAGE, offset])

    try:
        offers = conn.execute(query, params).fetchall()
    except sqlite3.OperationalError:
        offers = []

    count_query = "SELECT COUNT(*) FROM job_offers WHERE 1=1"
    count_params = []

    if search_query:
        keywords = search_query.split()
        for word in keywords:
            count_query += " AND title REGEXP ?"
            count_params.append(fr'\b{re.escape(word)}\b')
    
    if source_filter:
        count_query += " AND source_site = ?"
        count_params.append(source_filter)

    try:
        total_items = conn.execute(count_query, count_params).fetchone()[0]
    except (sqlite3.OperationalError, TypeError):
        total_items = 0

    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    
    try:
        sources_data = conn.execute("SELECT DISTINCT source_site FROM job_offers").fetchall()
        sources = [row['source_site'] for row in sources_data]
    except sqlite3.OperationalError:
        sources = []

    conn.close()
    
    page_range = range(max(1, page - 2), min(total_pages + 1, page + 3))
    
    quick_filters = get_dynamic_filters()

    return render_template('index.html', 
                           offers=offers, 
                           search_query=search_query,
                           current_query=search_query,
                           current_source=source_filter,
                           current_sort=sort_option,
                           page=page, 
                           total_pages=total_pages,
                           total_items=total_items,
                           sources=sources,
                           page_range=page_range,
                           quick_filters=quick_filters)

@app.route("/stats")
def stats():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM job_offers", conn)
    except Exception:
        df = pd.DataFrame()
    conn.close()

    if df.empty:
        return render_template('stats.html', 
                               total=0,
                               sources={},
                               seniority=[],
                               keywords=[],
                               max_source=1,
                               max_seniority=1,
                               max_keyword=1)

    source_counts = df['source_site'].value_counts()
    max_source = source_counts.max() if not source_counts.empty else 1

    all_titles_text = " ".join(df['title'].astype(str)).lower()
    
    count_junior = len(re.findall(r'\b(junior|staż|intern|trainee)\b', all_titles_text))
    count_mid = len(re.findall(r'\b(mid|regular)\b', all_titles_text))
    count_senior = len(re.findall(r'\b(senior|lead|head|architect|principal)\b', all_titles_text))
    
    seniority_data = [
        {'label': 'Junior / Staż', 'count': count_junior},
        {'label': 'Mid / Regular', 'count': count_mid},
        {'label': 'Senior / Lead', 'count': count_senior}
    ]
    
    max_seniority = max(s['count'] for s in seniority_data)
    if max_seniority == 0:
        max_seniority = 1

    keyword_stats = []
    for kw in SEARCH_KEYWORDS:
        pattern = fr'\b{re.escape(kw)}\b'
        matches = re.findall(pattern, all_titles_text)
        count = len(matches)
        if count > 0:
            keyword_stats.append({'word': kw.capitalize(), 'count': count})
    
    keyword_stats.sort(key=lambda x: x['count'], reverse=True)
    keyword_stats = keyword_stats[:10]
    max_keyword = keyword_stats[0]['count'] if keyword_stats else 1

    return render_template('stats.html', 
                           total=len(df),
                           sources=source_counts,
                           seniority=seniority_data,
                           keywords=keyword_stats,
                           max_source=max_source,
                           max_seniority=max_seniority,
                           max_keyword=max_keyword)

@app.route("/download_excel")
def download_excel():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT title, link, source_site, date_scraped FROM job_offers ORDER BY date_scraped DESC", conn)
    except Exception:
        df = pd.DataFrame()
    conn.close()

    if df.empty:
        return "Brak danych do pobrania", 404

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Oferty IT')
    
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='oferty_it_poznan.xlsx'
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)