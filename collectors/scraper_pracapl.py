import requests
import time
from bs4 import BeautifulSoup

def scrape_pracapl():
    base_url = "https://www.praca.pl/poznan.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    all_data = []
    seen_urls = set()
    page_num = 1
    max_pages = 15

    print(f"Starting Praca.pl scraping (limit: {max_pages} pages)...")

    while page_num <= max_pages:
        if page_num == 1:
            url = base_url
        else:
            url = f"{base_url}?p={page_num}"
            
        print(f"  Processing page {page_num}...")

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                break

            soup = BeautifulSoup(resp.text, 'html.parser')
            
            listing_items = soup.find_all('li', class_="listing__item")
            
            current_page_offers = 0

            for item in listing_items:
                link_tag = item.find('a', class_="listing__title")
                
                if not link_tag:
                    link_tag = item.find('a', href=True)

                if not link_tag:
                    continue

                href = link_tag['href']
                full_link = href
                if not full_link.startswith('http'):
                    full_link = f"https://www.praca.pl{href}"

                if full_link in seen_urls:
                    continue
                
                if 'oferta' not in full_link and '.html' not in full_link:
                    continue

                seen_urls.add(full_link)

                title = link_tag.text.strip()
                if not title:
                    title = "Praca.pl Offer"

                offer_obj = {
                    "title": title,
                    "company": "Unknown",
                    "city": "Poznań",
                    "salary": "Undisclosed",
                    "link": full_link,
                    "source_site": "praca.pl"
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
    offers = scrape_pracapl()
    print(f"Total found: {len(offers)}")