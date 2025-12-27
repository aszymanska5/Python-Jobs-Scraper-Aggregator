from collectors.scraper_rocketjobs import scrape_rocket
from db_manager import add_offers

def run_aggregator():
    print("--- STARTING JOB AGGREGATOR ---")
    
    total_new_offers = 0
    
    print("Running RocketJobs scraper...")
    try:
        rocket_data = scrape_rocket()
        print(f"    Fetched: {len(rocket_data)} offers")
        
        new_count = add_offers(rocket_data)
        print(f"    Saved to DB: {new_count} new offers")
        
        total_new_offers += new_count
        
    except Exception as e:
        print(f"    Error: {e}")

    print("-" * 30)
    print(f"SUMMARY: Added {total_new_offers} new offers in total.")
    print("--- FINISHED ---")

if __name__ == "__main__":
    run_aggregator()