import requests
import time
from bs4 import BeautifulSoup

def scrape_rocket():
    base_url = "https://rocketjobs.pl/oferty-pracy/poznan"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    all_offers = []
    MAX_PAGES_ROCKET = 5 

    print("[RocketJobs] Starting scraper...")

    for page_num in range(1, MAX_PAGES_ROCKET + 1):
        url = f"{base_url}?page={page_num}"
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

                all_offers.append({
                    "title": title,
                    "link": full_link,
                    "source_site": "RocketJobs"
                })

            time.sleep(1)
        except Exception:
            continue

    print(f"[RocketJobs] Finished. Total offers: {len(all_offers)}")
    return all_offers