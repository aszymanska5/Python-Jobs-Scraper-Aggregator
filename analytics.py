import re
import pandas as pd
from collections import Counter
from db_manager import get_db_connection

def get_dynamic_quick_filters() -> list:
    try:
        conn = get_db_connection()
        rows = conn.execute("SELECT title FROM offers").fetchall()
        conn.close()
        
        if not rows:
            return []
        
        text = " ".join([r[0] for r in rows]).lower()
        words = re.sub(r'[^\w\s]', '', text).split()
        
        stop_words = {
            'w', 'z', 'i', 'na', 'do', 'o', 'dla', 'oraz', 'od', 'po', 'ze', 'za', 
            'poznan', 'poznań', 'praca', 'oferta', 'pl', 'oferty', 'szukamy', 'new', 
            'remote', 'hybrydowa', 'stacjonarna', 'senior', 'junior', 'mid'
        }
        
        filtered = [w for w in words if w not in stop_words and len(w) > 3]
        return [w.capitalize() for w in [item[0] for item in Counter(filtered).most_common(5)]]
    except Exception:
        return []

def get_stats_data():
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT title, source_site FROM offers", conn)
        conn.close()
        
        if df.empty:
            return None, None
        
        counts = df['source_site'].value_counts().to_dict()
        
        text = " ".join(df['title'].astype(str).str.lower())
        words = re.sub(r'[^\w\s]', '', text).split()
        
        stop_words = {
            'w', 'z', 'i', 'na', 'do', 'o', 'dla', 'oraz', 'od', 'po', 'ze', 'za', 
            'poznan', 'poznań', 'praca', 'oferta', 'pl', 'oferty', 'szukamy', 'new'
        }
        
        top_keywords = Counter([w for w in words if w not in stop_words and len(w) > 3]).most_common(10)
        
        return counts, top_keywords
    except Exception:
        return None, None