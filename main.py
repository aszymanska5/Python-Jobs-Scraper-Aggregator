from db_manager import init_db, add_offer
from collectors.scraper_nofluff import scrape_nofluff
from collectors.scraper_olx import scrape_olx
from collectors.scraper_pracapl import scrape_pracapl
from collectors.scraper_rocketjobs import scrape_rocket

def run_aggregator():
    print("--- STARTING JOB AGGREGATOR (STABLE TRIPLE-SOURCE MODE) ---")
    
    init_db()
    
    scrapers = {
        "NoFluffJobs": scrape_nofluff,
        "OLX": scrape_olx,
        "Praca.pl": scrape_pracapl,
        "Rocket Jobs": scrape_rocket,
    }
    
    total_new = 0
    
    for name, scraper_func in scrapers.items():
        print(f"\n[Main] Running {name} scraper...")
        try:
            offers = scraper_func()
            new_from_source = 0
            for offer in offers:
                if add_offer(offer):
                    new_from_source += 1
            
            total_new += new_from_source
            print(f"[Main] {name} returned {len(offers)} offers. Added {new_from_source} NEW.")
        except Exception as e:
            print(f"[Main] Error in {name}: {e}")

    print("\n--- AGGREGATION FINISHED ---")
    print(f"Total new unique offers added this run: {total_new}")

if __name__ == "__main__":
    run_aggregator()