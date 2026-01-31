import requests
import time
import random
from bs4 import BeautifulSoup
from config import PRACA_PL_URL, USER_AGENT

def scrape_pracapl():
    headers = {
        "User-Agent": USER_AGENT
    }

    all_data = []
    seen_urls = set()
    page_num = 1
    MAX_PAGES_PRACAPL = 5
    
    forbidden_words = [
        "sprzedawca", "kasjer", "magazynier", "kierowca", "kurier", "kucharz", 
        "kelner", "lekarska", "pielęgniarka", "fizjoterapeuta", "kosmetyczka", 
        "budowlany", "produkcyjny", "fizyczny", "ochrony", "sprzątanie",
        "handlowy", "przedstawiciel", "nieruchomości", "prawnik", "apteka",
        "fryzjer", "mechanik", "ślusarz", "spawacz", "ochroniarz"
    ]

    print("[Praca.pl] Starting scraper...")

    while page_num <= MAX_PAGES_PRACAPL:
        sep = '&' if '?' in PRACA_PL_URL else '?'
        url = PRACA_PL_URL if page_num == 1 else f"{PRACA_PL_URL}{sep}p={page_num}"
        
        print(f"[Praca.pl] Processing page {page_num}...")

        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                print(f"[Praca.pl] Page {page_num} returned status {resp.status_code}")
                break

            soup = BeautifulSoup(resp.text, 'html.parser')
            
            offer_containers = soup.find_all(['li', 'div', 'article'], 
                class_=lambda x: x and any(c in x for c in ["listing__item", "offer-details", "item"]))

            if not offer_containers:
                print(f"[Praca.pl] No more containers found on page {page_num}")
                break

            for container in offer_containers:
                link_tag = container.find('a', href=True)
                if not link_tag:
                    continue

                href = link_tag['href']
                full_link = href if href.startswith('http') else f"https://www.praca.pl{href}"
                full_link = full_link.split('#')[0].split('?')[0]

                if full_link in seen_urls:
                    continue
                
                title_tag = container.find(['h2', 'h3']) or link_tag
                title = title_tag.get_text(" ", strip=True)
                
                if not title or len(title) < 5:
                    continue

                title_lower = title.lower()
                
                is_forbidden = False
                for bad in forbidden_words:
                    if bad in title_lower:
                        is_forbidden = True
                        break
                
                if is_forbidden:
                    continue

                seen_urls.add(full_link)
                
                all_data.append({
                    "title": title,
                    "link": full_link,
                    "source_site": "Praca.pl"
                })

            page_num += 1
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"[Praca.pl] Error: {e}")
            break

    print(f"[Praca.pl] Finished. Total offers: {len(all_data)}")
    return all_data