import requests
import time
import random
from config import USER_AGENT

def scrape_nofluff():
    url = "https://nofluffjobs.com/api/search/posting"
    
    headers = {
        "Content-Type": "application/infiniteSearch+json",
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://nofluffjobs.com",
        "Referer": "https://nofluffjobs.com/pl/poznan"
    }

    payload = {
        "rawSearch": "city=poznan",
        "pageSize": 50,
        "withSalaryMatch": True
    }

    all_data = []
    seen_ids = set()
    
    print("[NoFluffJobs] Starting scraper (Clean Title Strategy)...")

    for page in range(1, 4):
        params = {
            "pageFrom": page,
            "pageTo": page,
            "salaryCurrency": "PLN",
            "salaryPeriod": "month",
            "region": "pl",
            "language": "pl-PL"
        }
        
        try:
            response = requests.post(url, params=params, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                postings = data.get('postings', [])
                
                if not postings:
                    break

                for post in postings:
                    p_id = post.get('id') or post.get('url')
                    if not p_id or p_id in seen_ids:
                        continue
                    seen_ids.add(p_id)

                    raw_title = post.get('title', 'Oferta IT')
                    clean_title = raw_title.replace('Nowa', '').replace('NOWA', '').replace('nowa', '').strip()
                    
                    link = f"https://nofluffjobs.com/job/{post.get('url')}"
                    
                    all_data.append({
                        "title": clean_title,
                        "link": link,
                        "source_site": "NoFluffJobs"
                    })
            else:
                print(f"[NoFluffJobs] Błąd API: {response.status_code}")
                break
            
            time.sleep(random.uniform(1.0, 2.0))
        except Exception as e:
            print(f"[NoFluffJobs] Błąd: {e}")
            continue

    print(f"[NoFluffJobs] Finished. Found {len(all_data)} clean offers.")
    return all_data