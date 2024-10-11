# config/settings.py
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    """Base configuration class."""
    FLASK_ENV: str = os.getenv('FLASK_ENV', 'production')
    FLASK_APP: str = os.getenv('FLASK_APP')
    FLASK_DEBUG: bool = os.getenv('FLASK_DEBUG', "False").lower() == 'true'
    APP_DEBUG: bool = os.getenv('APP_DEBUG', "False").lower() == 'true'
    APP_ENV: str = os.getenv('APP_ENV', 'development')

    # Logger settings
    LOG_TO_FILE: bool = os.getenv("LOG_TO_FILE", "False").lower() == "true"
    LOG_FILE_NAME: str = os.getenv("LOG_FILE_NAME", "app.log")

    # Scraper settings
    SCRAPER_TIMEOUT: int = int(os.getenv('SCRAPER_TIMEOUT', 30))
    SCRAPER_DEFAULT_CONCURRENCY: int = int(os.getenv('SCRAPER_DEFAULT_CONCURRENCY'))
    SCRAPER_OUTPUT_DIR: str = os.getenv('SCRAPER_OUTPUT_DIR')
    SCRAPER_USER_AGENT: str = os.getenv('SCRAPER_USER_AGENT', 'Mozilla/5.0')

    # Web driver settings
    WEB_DRIVER_PATH: str = os.getenv('WEB_DRIVER_PATH')
    WEB_DRIVER_HEADLESS: bool = os.getenv('WEB_DRIVER_HEADLESS', 'True').lower() == 'true'


class DevelopmentConfig(Config):
    """Development configuration."""
    APP_DEBUG: bool = True
    APP_ENV: str = 'development'
    FLASK_ENV: str = 'development'
    LOG_TO_FILE: bool = False
    WEB_DRIVER_HEADLESS: bool = os.getenv('WEB_DRIVER_HEADLESS', 'False').lower() == 'true'

class ProductionConfig(Config):
    """Production configuration."""
    FLASK_DEBUG: bool = False
    FLASK_ENV: str = 'production'
    APP_ENV: str = 'production'


class TestingConfig(Config):
    """Testing configuration."""
    FLASK_DEBUG: bool = False
    FLASK_ENV: str = 'testing'
    APP_ENV: str = 'testing'


# Select configuration based on the FLASK_ENV variable
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}[os.getenv('APP_ENV', 'development')]  # type: Config
