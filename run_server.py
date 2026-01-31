from flask import Flask, render_template, request, url_for
import db_manager
import analytics
import math
from config import ITEMS_PER_PAGE

app = Flask(__name__)

@app.route('/')
def index():
    query = request.args.get('query', '')
    source = request.args.get('source', '')
    sort = request.args.get('sort', 'newest')
    page = int(request.args.get('page', 1))

    df = db_manager.get_all_offers_as_df()
    if df.empty:
        return render_template('index.html', offers=[], total_items=0, page=1, total_pages=1, page_range=[1])

    if query:
        df = df[df['title'].str.lower().str.contains(query.lower())]
    if source:
        df = df[df['source_site'] == source]

    if sort == 'az':
        df = df.sort_values('title', ascending=True)
    else:
        df = df.sort_values('created_at', ascending=False)

    total_items = len(df)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    offers_list = df.iloc[start:end].to_dict(orient='records')

    range_size = 5
    start_p = max(1, page - 2)
    end_p = min(total_pages, start_p + range_size - 1)
    page_range = range(start_p, end_p + 1)

    return render_template('index.html',
                           offers=offers_list, total_items=total_items,
                           page=page, total_pages=total_pages, page_range=page_range,
                           current_query=query, current_source=source, current_sort=sort,
                           sources=df['source_site'].unique().tolist(),
                           quick_filters=analytics.get_quick_filters())

@app.route('/stats')
def stats():
    sources, top_keywords, max_val = analytics.get_stats_data()
    return render_template('stats.html', sources=sources, top_keywords=top_keywords, max_val=max_val)

if __name__ == '__main__':
    app.run(debug=True)