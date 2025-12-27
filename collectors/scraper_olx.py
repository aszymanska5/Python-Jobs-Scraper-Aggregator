import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_olx():
    base_url = "https://www.olx.pl/praca/poznan/"
    data = []
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    for page in range(1, 11):
        url = base_url if page == 1 else f"{base_url}?page={page}"

        try:
            response = session.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            offers = soup.find_all('div', attrs={'data-cy': 'l-card'})

            if not offers:
                break

            for offer in offers:
                try:
                    title = ""
                    h2_tag = offer.find('h2')
                    if h2_tag:
                        title = h2_tag.text.strip()
                    else:
                        h6_tag = offer.find('h6')
                        if h6_tag:
                            title = h6_tag.text.strip()
                        else:
                            a_tag = offer.find('a')
                            if a_tag:
                                title = a_tag.text.strip()
                    
                    if not title:
                        continue

                    link_tag = offer.find('a')
                    link = link_tag['href'] if link_tag else ""
                    if link and not link.startswith("http"):
                        link = "https://www.olx.pl" + link

                    price_tag = offer.find('p', attrs={'data-testid': 'ad-price'})
                    price = price_tag.text.strip() if price_tag else "Nie podano"

                    city = "Poznań"
                    loc_tag = offer.find('p', attrs={'data-testid': 'location-date'})
                    if loc_tag:
                        loc_text = loc_tag.text
                        if "-" in loc_text:
                            city = loc_text.split('-')[0].strip()
                        elif "Odświeżono" not in loc_text:
                            city = loc_text.strip()

                    data.append({
                        'title': title,
                        'company': 'OLX User',
                        'city': city,
                        'salary': price,
                        'link': link,
                        'source_site': 'OLX'
                    })

                except Exception:
                    continue

            time.sleep(random.uniform(1, 3))

        except Exception:
            break

    return data

if __name__ == "__main__":
    wyniki = scrape_olx()
    print(len(wyniki))
    if wyniki:
        print(wyniki[0])