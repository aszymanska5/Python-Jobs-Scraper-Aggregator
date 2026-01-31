import requests
import time
import random

def scrape_olx():
    base_url = "https://www.olx.pl/api/v1/offers?offset={}&limit=40&category_id=4&region_id=15"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = []
    seen_links = set()
    
    print("[OLX] Scaling up to 400+ offers...")

    for offset in range(0, 440, 40):
        try:
            resp = requests.get(base_url.format(offset), headers=headers, timeout=10)
            if resp.status_code != 200: break
            offers = resp.json().get('data', [])
            if not offers: break
            for offer in offers:
                link = offer.get('url')
                if link not in seen_links:
                    seen_links.add(link)
                    data.append({'title': offer.get('title'), 'link': link, 'source_site': 'OLX'})
            time.sleep(0.3)
        except: continue

    return data