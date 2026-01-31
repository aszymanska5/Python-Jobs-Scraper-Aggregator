import pandas as pd
from datetime import datetime
from setup_db import run_setup
from collectors.scraper_rocketjobs import scrape_rocket
from collectors.scraper_pracapl import scrape_pracapl
from collectors.scraper_olx import scrape_olx
from collectors.scraper_nofluff import scrape_nofluff
from db_manager import add_offers

def main():
    run_setup()
    
    print(f"Starting Data Collection Process...")
    
    all_collected_offers = []
    
    rocket_offers = scrape_rocket()
    all_collected_offers.extend(rocket_offers)
    
    praca_offers = scrape_pracapl()
    all_collected_offers.extend(praca_offers)
    
    olx_offers = scrape_olx()
    all_collected_offers.extend(olx_offers)

    nofluff_offers = scrape_nofluff()
    all_collected_offers.extend(nofluff_offers)
    
    if not all_collected_offers:
        print("No offers collected.")
        return

    df = pd.DataFrame(all_collected_offers)
    
    added = add_offers(df)
    
    print(f"Process finished. New unique offers added: {added}")

if __name__ == "__main__":
    main()