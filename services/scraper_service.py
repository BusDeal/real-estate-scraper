from scrapers.lennar_scraper import LennarScraper
from scrapers.drhorton_scraper import DRHortonScraper

def start_scraping(vendor, search_term):
    if vendor == 'lennar':
        scraper = LennarScraper()
    elif vendor == 'drhorton':
        scraper = DRHortonScraper()
    else:
        raise ValueError(f"Unknown scraper type: {vendor}")
    
    scraper.scrape(search=search_term)
