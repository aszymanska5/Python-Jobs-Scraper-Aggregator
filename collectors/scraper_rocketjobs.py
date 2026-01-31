import requests
import time
import random
from bs4 import BeautifulSoup
from config import ROCKET_URL, USER_AGENT

def scrape_rocket():
    headers = {
        "User-Agent": USER_AGENT
    }
    
    all_offers = []
    MAX_PAGES_ROCKET = 5 

    print("[RocketJobs] Starting scraper...")

    for page_num in range(1, MAX_PAGES_ROCKET + 1):
        sep = '&' if '?' in ROCKET_URL else '?'
        url = f"{ROCKET_URL}{sep}page={page_num}"
        
        print(f"[RocketJobs] Processing page {page_num}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            offer_cards = soup.find_all('div', attrs={"class": lambda x: x and 'MuiBox-root' in x})
            
            for card in offer_cards:
                link_tag = card.find('a', href=True)
                if not link_tag:
                    continue
                
                href = link_tag['href']
                if '/oferta-pracy/' not in href:
                    continue

                full_link = f"https://rocketjobs.pl{href}"
                
                title_tag = card.find('h2') or card.find('h3')
                if title_tag:
                    title = title_tag.text.strip()
                else:
                    clean_slug = href.split('/')[-1].replace('-', ' ').title()
                    if "Poznan" in clean_slug:
                        clean_slug = clean_slug.split("Poznan")[0]
                    title = clean_slug.strip()

                if title.lower().endswith("nowa"):
                    title = title[:-4].strip()

                all_offers.append({
                    "title": title,
                    "link": full_link,
                    "source_site": "RocketJobs"
                })

            time.sleep(random.uniform(1, 2))
        except Exception:
            continue

    print(f"[RocketJobs] Finished. Total offers: {len(all_offers)}")
    return all_offers