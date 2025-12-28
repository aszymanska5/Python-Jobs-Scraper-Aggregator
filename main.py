import pandas as pd
from collectors.scraper_rocketjobs import scrape_rocket
from collectors.scraper_pracapl import scrape_pracapl
from collectors.scraper_olx import scrape_olx
from db_manager import add_offers

def run_aggregator():
    print("--- STARTING JOB AGGREGATOR ---")
    
    all_offers_list = []
    
    try:
        rocket_data = scrape_rocket()
        all_offers_list.extend(rocket_data)
    except Exception as e:
        print(f"[Main] Error RocketJobs: {e}")

    try:
        pracapl_data = scrape_pracapl()
        all_offers_list.extend(pracapl_data)
    except Exception as e:
        print(f"[Main] Error Praca.pl: {e}")

    try:
        olx_data = scrape_olx()
        all_offers_list.extend(olx_data)
    except Exception as e:
        print(f"[Main] Error OLX: {e}")

    print(f"[Main] Aggregating {len(all_offers_list)} offers...")
    
    if all_offers_list:
        df = pd.DataFrame(all_offers_list)
        new_count = add_offers(df)
        print(f"[Main] Success! Added {new_count} new unique offers.")
    else:
        print("[Main] No offers fetched today.")

    print("--- FINISHED ---")

if __name__ == "__main__":
    run_aggregator()