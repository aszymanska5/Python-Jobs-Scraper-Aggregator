import pandas as pd
from collectors.scraper_rocketjobs import scrape_rocket
from collectors.scraper_pracapl import scrape_pracapl
from collectors.scraper_olx import scrape_olx
from collectors.scraper_nofluff import scrape_nofluff
from db_manager import add_offers

def run_aggregator():
    print("--- STARTING JOB AGGREGATOR ---")
    
    all_offers_list = []
    
    try:
        rocket_data = scrape_rocket()
        print(f"[Main] RocketJobs fetched: {len(rocket_data)}")
        all_offers_list.extend(rocket_data)
    except Exception as e:
        print(f"[Main] Error RocketJobs: {e}")

    try:
        nfj_data = scrape_nofluff()
        print(f"[Main] NoFluffJobs fetched: {len(nfj_data)}")
        all_offers_list.extend(nfj_data)
    except Exception as e:
        print(f"[Main] Error NoFluffJobs: {e}")

    try:
        pracapl_data = scrape_pracapl()
        print(f"[Main] Praca.pl fetched: {len(pracapl_data)}")
        all_offers_list.extend(pracapl_data)
    except Exception as e:
        print(f"[Main] Error Praca.pl: {e}")

    try:
        olx_data = scrape_olx()
        print(f"[Main] OLX fetched: {len(olx_data)}")
        all_offers_list.extend(olx_data)
    except Exception as e:
        print(f"[Main] Error OLX: {e}")

    print(f"[Main] Aggregating {len(all_offers_list)} offers...")
    
    if all_offers_list:
        df = pd.DataFrame(all_offers_list)
        
        if 'link' in df.columns:
            df.drop_duplicates(subset=['link'], keep='first', inplace=True)
        
        new_count = add_offers(df)
        print(f"[Main] Success! Added {new_count} new unique offers.")
    else:
        print("[Main] No offers fetched today.")

    print("--- FINISHED ---")

if __name__ == "__main__":
    run_aggregator()