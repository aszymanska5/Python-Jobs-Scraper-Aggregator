import pandas as pd
from collectors.scraper_rocketjobs import scrape_rocket
from collectors.scraper_pracapl import scrape_pracapl
from collectors.scraper_olx import scrape_olx
from db_manager import add_offers

def run_aggregator():
    print("--- STARTING JOB AGGREGATOR ---")
    
    all_offers_list = []
    
    print("\n >> 1/3 Running RocketJobs scraper...")
    try:
        rocket_data = scrape_rocket()
        print(f"    Fetched: {len(rocket_data)} offers")
        all_offers_list.extend(rocket_data)
    except Exception as e:
        print(f"    Error RocketJobs: {e}")

    print("\n >> 2/3 Running Praca.pl scraper...")
    try:
        pracapl_data = scrape_pracapl()
        print(f"    Fetched: {len(pracapl_data)} offers")
        all_offers_list.extend(pracapl_data)
    except Exception as e:
        print(f"    Error Praca.pl: {e}")

    print("\n >> 3/3 Running OLX scraper...")
    try:
        olx_data = scrape_olx()
        print(f"    Fetched: {len(olx_data)} offers")
        all_offers_list.extend(olx_data)
    except Exception as e:
        print(f"    Error OLX: {e}")

    print(f"\n >> Aggregating {len(all_offers_list)} offers into DataFrame...")
    
    if all_offers_list:
        df = pd.DataFrame(all_offers_list)
        
        print(f"    DataFrame shape: {df.shape}")
        
        added_count = add_offers(df)
        print(f"    Successfully saved to DB: {added_count} new offers")
    else:
        print("    No offers collected from any source.")

    print("-" * 30)
    print("--- FINISHED ---")

if __name__ == "__main__":
    run_aggregator()