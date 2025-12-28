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
    MAX_PAGES_PRACAPL = 5

    print("[Praca.pl] Starting scraper...")

    while page_num <= MAX_PAGES_PRACAPL:
        url = base_url if page_num == 1 else f"{base_url}?p={page_num}"
        print(f"[Praca.pl] Processing page {page_num}...")

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                break

            soup = BeautifulSoup(resp.text, 'html.parser')
            listing_items = soup.find_all('li', class_="listing__item")
            
            for item in listing_items:
                link_tag = item.find('a', class_="listing__offer-title", href=True) or item.find('a', href=True)
                if not link_tag:
                    continue

                href = link_tag['href']
                full_link = href if href.startswith('http') else f"https://www.praca.pl{href}"

                if full_link in seen_urls:
                    continue
                
                if 'oferta' not in full_link and '.html' not in full_link:
                    continue

                seen_urls.add(full_link)
                title = link_tag.text.strip() or "Praca.pl Offer"

                all_data.append({
                    "title": title,
                    "link": full_link,
                    "source_site": "Praca.pl"
                })

            page_num += 1
            time.sleep(1)
        except Exception:
            break

    print(f"[Praca.pl] Finished. Total offers: {len(all_data)}")
    return all_data