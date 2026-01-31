import pandas as pd
import re
import db_manager

def get_stats_data():
    df = db_manager.get_all_offers_as_df()
    
    if df.empty:
        return {}, [], 0

    sources_dict = df['source_site'].value_counts().to_dict()

    tech_list = ['python', 'java', 'sql', 'javascript', 'tester', 'devops', 'data', 'junior', 'senior']
    
    top_keywords = []
    
    for tech in tech_list:
        pattern = rf'\b{re.escape(tech)}\b'
        count = df['title'].str.count(pattern, flags=re.IGNORECASE).sum()
        
        if count > 0:
            top_keywords.append((tech.capitalize(), int(count)))
    
    top_keywords.sort(key=lambda x: x[1], reverse=True)
    max_val = max([x[1] for x in top_keywords]) if top_keywords else 1
    
    return sources_dict, top_keywords, max_val

def get_quick_filters():
    df = db_manager.get_all_offers_as_df()
    
    if df.empty:
        return []

    stop_words = {'w', 'na', 'dla', 'z', 'do', 'o', 'and', 'the', 'with', 'of', 'pracy', 'oferta', 'poznan'}

    all_words = df['title'].str.lower().str.findall(r'\b\w+\b').explode()

    mask = (all_words.str.len() > 3) & (~all_words.isin(stop_words))
    filtered_words = all_words[mask]

    most_common = filtered_words.value_counts().head(6)

    return [word.capitalize() for word in most_common.index.tolist()]