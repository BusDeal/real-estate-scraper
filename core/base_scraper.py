# core/base_scraper.py
from abc import ABC, abstractmethod
import json
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.constants import CHROME_BROWSER, FIREFOX_BROWSER
from config.settings import config
from utils.helpers import timeit

class BaseScraper(ABC):
    def __init__(self):
        self.driver = self.init_driver()

    @staticmethod
    @timeit
    def init_driver(browser=CHROME_BROWSER):
        print("init_driver: launching a browser instance")
        if browser == CHROME_BROWSER:
            return BaseScraper.chrome_driver()
        elif browser == FIREFOX_BROWSER:
            return BaseScraper.firefox_driver()


    @staticmethod
    def chrome_driver():
        """
        Initializes and returns a headless Chrome driver instance.

        The driver instance is configured to run in headless mode and with image
        loading disabled. This is done to reduce the memory and CPU footprint of the
        driver instance.

        Returns:
            A headless Chrome driver instance.
        """
        options = webdriver.ChromeOptions()
        if config.FLASK_ENV == 'development':
            options.add_argument('--headless')
            
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument("start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # this will disable image loading
        # options.add_argument('--blink-settings=imagesEnabled=false')
        # or alternatively we can set direct preference:
        # options.add_experimental_option(
        #     "prefs", {"profile.managed_default_content_settings.images": 2}
        # )
        chrome_service = Service(executable_path=config.WEB_DRIVER_PATH)
        driver = webdriver.Chrome(service=chrome_service, options=options)
        return driver
    @staticmethod
    def firefox_driver():
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        return driver

    @abstractmethod
    def extract_community_data(self, page_html: str) -> list:
        """Extract community data (to be implemented by subclasses)."""
        pass

    @abstractmethod
    def extract_details_page_data(self, details_url: str) -> dict:
        """Extract details from community pages (to be implemented by subclasses)."""
        pass

    # Utility function to wait for element visibility
    def wait_for_element(self, selector_type, selector, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((selector_type, selector))
        )

    def load_page(self, url, timeout=10):
        self.driver.get(url)
        time.sleep(timeout)

    def load_page_with_wait(
        self, url: str, time_in_seconds: int = 5
    ) -> str:
        """
        Load a page and wait for the specified time.

        Args:
            url (str): The URL to load.
            time_in_seconds (int, optional): The time to wait in seconds. Defaults to 5.

        Returns:
            str: The HTML content of the page.
        """
        html = ''
        try:
            self.driver.get(url)
            time.sleep(time_in_seconds)
            html = self.driver.page_source
        except Exception as e:
            print(f"Error occurred while loading page: {e}")
        return html


    def page_clean_up(self):
        # remove pop_ups if any
        # remove ads, banners if any
        # remove privacy policy popup if any
        # remove other unnecessary elements
        pass

    def get_beautiful_soup(
        self, html: str, parser: str = "html.parser"
    ) -> BeautifulSoup:
        """
        Creates a BeautifulSoup object from the given HTML content.

        Args:
            html (str): The HTML content to parse.
            parser (str): The parser to use. Defaults to "html.parser".

        Returns:
            BeautifulSoup: The parsed content as a BeautifulSoup object.
        """
        soup = BeautifulSoup(html, parser)
        return soup

    def close_driver(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"error closing the driver: {e}")

    def save_to_file(self, data: dict, filename: str):
        """
        Save data to a JSON file.

        Args:
            data (dict): The data to save.
            filename (str): The name of the file to save to.
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving the data: {e}")
