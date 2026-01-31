import requests
import time
import random
from bs4 import BeautifulSoup
from config import USER_AGENT

def scrape_pracapl():
    headers = {"User-Agent": USER_AGENT}
    
    urls = [
        "https://www.praca.pl/oferty-pracy_wielkopolskie.html",
        "https://www.praca.pl/praca-zdalna.html"
    ]

    all_data = []
    seen_urls = set()
    MAX_PAGES = 5

    print("[Praca.pl] Starting scraper (BROAD SEARCH - Region Only)...")

    for base_url in urls:
        for page_num in range(1, MAX_PAGES + 1):
            url = f"{base_url}?p={page_num}" if page_num > 1 else base_url

            try:
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code != 200:
                    break

                soup = BeautifulSoup(resp.text, 'html.parser')
                items = soup.find_all('li', class_="listing__item")
                
                if not items:
                    items = soup.find_all('div', class_="listing__item") 

                for item in items:
                    link_tag = item.find('a', class_="listing__offer-title")
                    if not link_tag:
                        link_tag = item.find('a', href=True)

                    if not link_tag:
                        continue

                    href = link_tag.get('href')
                    if not href or 'javascript' in href:
                        continue
                        
                    full_link = href if href.startswith('http') else f"https://www.praca.pl{href}"

                    if full_link in seen_urls:
                        continue
                    seen_urls.add(full_link)
                    
                    title = link_tag.text.strip()
                    if not title:
                        title_tag = item.find('h3') 
                        if title_tag:
                            title = title_tag.text.strip()
                        else:
                            title = "Oferta Pracy"

                    all_data.append({
                        "title": title,
                        "link": full_link,
                        "source_site": "Praca.pl"
                    })

                time.sleep(random.uniform(0.5, 1.0))
            except Exception:
                continue

    print(f"[Praca.pl] Finished. Found {len(all_data)} offers.")
    return all_data