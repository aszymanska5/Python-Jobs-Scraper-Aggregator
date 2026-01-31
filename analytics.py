import sqlite3
import collections
import re
import os
from config import DB_PATH

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_stats_data():
    if not os.path.exists(DB_PATH): return {}, [], 0
    conn = get_db_connection()
    
    rows = conn.execute("SELECT source_site, COUNT(*) as count FROM offers WHERE source_site != '' GROUP BY source_site").fetchall()
    sources_dict = {row['source_site']: row['count'] for row in rows}
    
    titles = conn.execute("SELECT title FROM offers").fetchall()
    conn.close()
    
    all_text = " ".join([t['title'].lower() for t in titles])
    tech_list = ['python', 'java', 'sql', 'javascript', 'tester', 'driver', 'magazynier', 'sprzedawca', 'junior', 'senior']
    
    top_keywords = []
    for tech in tech_list:
        c = len(re.findall(rf'\b{re.escape(tech)}\b', all_text))
        if c > 0:
            top_keywords.append((tech.capitalize(), c))
    
    top_keywords.sort(key=lambda x: x[1], reverse=True)
    max_val = max([x[1] for x in top_keywords]) if top_keywords else 1
    
    return sources_dict, top_keywords, max_val

def get_quick_filters():
    if not os.path.exists(DB_PATH): return []
    conn = get_db_connection()
    titles = conn.execute("SELECT title FROM offers").fetchall()
    conn.close()
    
    words = []
    stop_words = {'w', 'na', 'dla', 'z', 'do', 'o', 'and', 'the', 'of', 'pracy', 'oferta', 'poznan'}
    for t in titles:
        found = re.findall(r'\b\w+\b', t['title'].lower())
        words.extend([w for w in found if len(w) > 3 and w not in stop_words])
    
    most_common = collections.Counter(words).most_common(6)
    return [x[0].capitalize() for x in most_common]