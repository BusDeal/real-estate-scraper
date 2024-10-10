from flask import Flask
from config.settings import config
from blueprints.scraper_api import scraper_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    # Register blueprint
    app.register_blueprint(scraper_blueprint, url_prefix='/api/v1/scraper')

    return app

if __name__ == '__main__':
    app = create_app()
    print(config.FLASK_DEBUG)
    app.run(debug=config.FLASK_DEBUG)
