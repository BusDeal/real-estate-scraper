from flask import Blueprint, jsonify, request
from services.scraper_service import start_scraping

scraper_blueprint = Blueprint('scraper', __name__)

@scraper_blueprint.route('/start', methods=['POST'])
def scrape():
    data = request.get_json()
    scraper_vendor = data.get('vendor')  # Example: 'lennar' or 'drhorton'
    search_term = data.get('search')
    if not scraper_vendor:
        return jsonify({'status': 'error', 'message': "provide the scraper_vendor"}), 400
    try:
        # Start scraping ayncronously and don't wait for it to finish
        start_scraping(scraper_vendor, search_term)
        print("scraping started for ", scraper_vendor)
        return jsonify({'status': 'success', 'message': f"scraping started for {scraper_vendor}"}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
