import requests
import time
from bs4 import BeautifulSoup

def scrape_rocket():
    base_url = "https://rocketjobs.pl/oferty-pracy/poznan"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    all_offers = []
    max_pages = 10

    print(f"Starting scraping RocketJobs (Pages 1 to {max_pages})...")

    for page_num in range(1, max_pages + 1):
        url = f"{base_url}?page={page_num}"
        
        try:
            print(f"  Fetching page {page_num}...")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            
            page_links = soup.find_all('a', href=True)
            unique_hrefs = set()

            for a in page_links:
                href = a['href']
                if '/oferta-pracy/' in href:
                    unique_hrefs.add(href)

            if not unique_hrefs:
                break

            for href in unique_hrefs:
                full_link = f"https://rocketjobs.pl{href}"
                
                try:
                    slug = href.split('/')[-1]
                    title = slug.replace('-', ' ').title()
                except Exception:
                    title = "RocketJobs Offer"

                all_offers.append({
                    "title": title,
                    "company": "Unknown",
                    "city": "Poznań",
                    "salary": "Undisclosed",
                    "link": full_link,
                    "source_site": "rocketjobs.pl"
                })
            
            time.sleep(1)

        except Exception:
            continue

    return all_offers

if __name__ == "__main__":
    offers = scrape_rocket()
    print(f"Total offers found: {len(offers)}")