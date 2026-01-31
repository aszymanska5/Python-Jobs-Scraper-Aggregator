import requests
import time
import random
from bs4 import BeautifulSoup
from config import NOFLUFF_URL, USER_AGENT

def scrape_nofluff():
    headers = {
        "User-Agent": USER_AGENT
    }
    
    all_data = []
    seen_links = set()
    MAX_PAGES = 5
    
    print("[NoFluffJobs] Starting scraper...")

    for page in range(1, MAX_PAGES + 1):
        sep = '&' if '?' in NOFLUFF_URL else '?'
        url = f"{NOFLUFF_URL}{sep}page={page}"
        
        print(f"[NoFluffJobs] Processing page {page}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)

            for link_tag in links:
                href = link_tag['href']
                if '/job/' not in href:
                    continue

                full_link = f"https://nofluffjobs.com{href}"

                if full_link in seen_links:
                    continue
                seen_links.add(full_link)

                title_tag = link_tag.find('h3')
                if title_tag:
                    title = title_tag.text.strip()
                else:
                    slug = href.split('/job/')[-1]
                    title = slug.replace('-', ' ').title()

                if title.lower().endswith("nowa"):
                    title = title[:-4].strip()

                all_data.append({
                    'title': title,
                    'link': full_link,
                    'source_site': 'NoFluffJobs'
                })

            time.sleep(random.uniform(1, 2))
        except Exception:
            break

    print(f"[NoFluffJobs] Finished. Total offers: {len(all_data)}")
    return all_data