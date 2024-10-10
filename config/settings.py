# config/settings.py
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    """Base configuration class."""
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', False)
    APP_DEBUG = os.getenv('APP_DEBUG', False)

    # Logger settings
    LOG_TO_FILE = os.getenv("LOG_TO_FILE", "False").lower() == "true"
    LOG_FILE_NAME = os.getenv("LOG_FILE_NAME", "app.log")

    # Scraper settings
    SCRAPER_TIMEOUT = int(os.getenv('SCRAPER_TIMEOUT', 30))
    SCRAPER_USER_AGENT = os.getenv('SCRAPER_USER_AGENT', 'Mozilla/5.0')

    # Web driver settings
    WEB_DRIVER_PATH = os.getenv('WEB_DRIVER_PATH')
    WEB_DRIVER_HEADLESS = os.getenv('WEB_DRIVER_HEADLESS', 'True').lower() == 'true'


class DevelopmentConfig(Config):
    """Development configuration."""
    APP_DEBUG = True
    FLASK_ENV = 'development'
    LOG_TO_FILE = False
    WEB_DRIVER_HEADLESS = os.getenv('WEB_DRIVER_HEADLESS', 'False').lower() == 'true'

class ProductionConfig(Config):
    """Production configuration."""
    FLASK_DEBUG = False
    FLASK_ENV = 'production'


class TestingConfig(Config):
    """Testing configuration."""
    FLASK_DEBUG = False
    FLASK_ENV = 'testing'


# Select configuration based on the FLASK_ENV variable
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}[os.getenv('FLASK_ENV', 'development')]
