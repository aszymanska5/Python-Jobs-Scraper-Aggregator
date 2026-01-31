import requests
from bs4 import BeautifulSoup
import time
import random
from config import ROCKET_URL, USER_AGENT

def scrape_rocket():
    headers = {
        "User-Agent": USER_AGENT
    }
    
    all_data = []
    seen_urls = set()
    page = 1
    MAX_PAGES_ROCKET = 5
    
    allowed_keywords = [
        "python", "data", "it", "support", "analyst", "developer", "programista", 
        "engineer", "manager", "cloud", "sap", "devops", "junior", "intern", 
        "staz", "staż", "backend", "fullstack", "frontend", "automation", "test",
        "ai", "ml", "bi", "security", "infrastructure", "system", "admin"
    ]

    print("[RocketJobs] Starting scraper...")

    while page <= MAX_PAGES_ROCKET:
        if "?" in ROCKET_URL:
            url = f"{ROCKET_URL}&page={page}"
        else:
            url = f"{ROCKET_URL}?page={page}"
            
        print(f"[RocketJobs] Processing page {page}...")
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                break
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            offer_divs = soup.find_all('div', class_=lambda x: x and 'MuiBox-root' in x)
            
            for div in offer_divs:
                link_tag = div.find('a', href=True)
                if not link_tag:
                    continue
                
                href = link_tag['href']
                if not href.startswith('/oferta-pracy'):
                    continue
                
                base_href = href.rsplit('-', 1)[0]
                full_link = f"https://rocketjobs.pl{href}"
                
                if full_link in seen_urls:
                    continue
                
                title_tag = div.find('h2') or div.find('h3') or link_tag.find('div')
                if not title_tag:
                    continue
                    
                title = title_tag.get_text(" ", strip=True)
                title_lower = title.lower()
                
                is_relevant = False
                for word in allowed_keywords:
                    if word in title_lower:
                        is_relevant = True
                        break
                
                if not is_relevant:
                    continue
                seen_urls.add(full_link)
                
                all_data.append({
                    "title": title,
                    "link": full_link,
                    "source_site": "RocketJobs"
                })

            page += 1
            time.sleep(random.uniform(1, 3))
            
        except Exception:
            break
            
    print(f"[RocketJobs] Finished. Total offers: {len(all_data)}")
    return all_data