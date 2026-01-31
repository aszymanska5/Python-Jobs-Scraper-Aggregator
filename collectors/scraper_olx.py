import requests
from bs4 import BeautifulSoup
import time
import random
from config import OLX_URL, USER_AGENT

def scrape_olx():
    data = []
    seen_links = set()
    MAX_PAGES_OLX = 5
    
    print("[OLX] Starting scraper...")
    
    headers = {
        'User-Agent': USER_AGENT
    }

    for page in range(1, MAX_PAGES_OLX + 1):
        sep = '&' if '?' in OLX_URL else '?'
        url = OLX_URL if page == 1 else f"{OLX_URL}{sep}page={page}"
        
        print(f"[OLX] Processing page {page}...")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)

            for link_tag in links:
                href = link_tag['href']
                if '/oferta/' not in href:
                    continue
                if '/kategoria/' in href:
                    continue

                full_link = href if href.startswith("http") else "https://www.olx.pl" + href

                if full_link in seen_links:
                    continue
                seen_links.add(full_link)

                title_tag = link_tag.find('h6')
                if title_tag:
                    title = title_tag.text.strip()
                else:
                    slug = href.split('/')[-1].split('-CID')[0]
                    title = slug.replace('-', ' ').title()

                if len(title) < 4:
                    continue

                data.append({
                    'title': title,
                    'link': full_link,
                    'source_site': 'OLX'
                })

            time.sleep(random.uniform(1, 2))
        except Exception:
            break

    print(f"[OLX] Finished. Total offers: {len(data)}")
    return data