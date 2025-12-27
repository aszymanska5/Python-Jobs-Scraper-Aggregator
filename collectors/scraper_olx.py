import requests
import time
from bs4 import BeautifulSoup

def scrape_olx():
    base_url = "https://www.olx.pl/praca/poznan/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    all_data = []
    seen_urls = set()
    page_num = 1
    max_pages = 25

    print(f"Starting OLX scraping (limit: {max_pages} pages)...")

    while page_num <= max_pages:
        url = f"{base_url}?page={page_num}"
        print(f"  Processing page {page_num}...")

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                break

            soup = BeautifulSoup(resp.text, 'html.parser')
            links = soup.find_all('a', href=True)
            current_page_offers = 0

            for link in links:
                href = link['href']
                
                if '/oferta/praca/' in href:
                    full_link = href
                    if not full_link.startswith('http'):
                        full_link = f"https://www.olx.pl{href}"

                    if full_link in seen_urls:
                        continue
                    
                    seen_urls.add(full_link)

                    title_tag = link.find('h6')
                    if title_tag:
                        title = title_tag.text.strip()
                    else:
                        title = "OLX Offer"

                    offer_obj = {
                        "title": title,
                        "company": "OLX User",
                        "city": "Poznań",
                        "salary": "Undisclosed",
                        "link": full_link,
                        "source_site": "olx.pl"
                    }
                    
                    all_data.append(offer_obj)
                    current_page_offers += 1

            if current_page_offers == 0:
                print("  No offers found on this page. Stopping.")
                break

            page_num += 1
            time.sleep(1)

        except Exception:
            break

    return all_data

if __name__ == "__main__":
    offers = scrape_olx()
    print(f"Total found: {len(offers)}")