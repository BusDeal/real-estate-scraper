from scrapers.lennar_scraper import LennarScraper
from scrapers.drhorton_scraper import DRHortonScraper

def start_scraping(vendor):
    if vendor == 'lennar':
        scraper = LennarScraper()
    elif vendor == 'drhorton':
        scraper = DRHortonScraper()
    else:
        raise ValueError(f"Unknown scraper type: {vendor}")
    
    result = scraper.scrape()  # Assuming each scraper has a `scrape` method
    return result
