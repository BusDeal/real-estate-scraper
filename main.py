# main.py
from scrapers import DRHortonScraper, LennarScraper
import json
import pandas as pd
import sys

def scrape_drhorton():
    scraper = DRHortonScraper()
    try:
        # Extract community data
        communities = scraper.scrape()
        print(f"Total Communities: {len(communities)}")
        print("Scraping completed successfully!")
    finally:
        scraper.close_driver()

def scrape_lennar():
    scraper = LennarScraper()
    try:
        data = scraper.scrape()
        print(f"\nfound {len(data)} communities")
        print(json.dumps(data))
        # json.dump(data, open('communities.json', 'w'))
    except Exception as e:
        print(repr(e))

if __name__ == "__main__":
    # take vendor from command line argument 
    vendor = "lennar"
    vendor = sys.argv[1]
    match vendor:
        case "lennar":
            scrape_lennar()
        case "drhorton":
            scrape_drhorton()
        case _:
            raise ValueError(f"Unknown scraper vendor: {vendor}")
