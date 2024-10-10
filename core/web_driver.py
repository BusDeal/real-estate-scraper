from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager

class WebDriverHandler:
    def __init__(self, browser_type="firefox"):
        """Initialize with browser type (default is 'firefox')."""
        self.browser_type = browser_type.lower()  # Normalize to lowercase
        self.driver = None

    def start_driver(self):
        """Start either Chrome or Firefox WebDriver based on the browser_type."""
        if self.browser_type == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run Chrome in headless mode
            self.driver = webdriver.Chrome(options=options)
            # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        else:  # Default to Firefox
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')  # Run Firefox in headless mode
            self.driver = webdriver.Firefox(options=options)
            # self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    def get_page(self, url):
        """Fetch the page source for the given URL."""
        if not self.driver:
            raise Exception("Driver not initialized. Call start_driver() first.")
        self.driver.get(url)
        return self.driver.page_source

    def close_driver(self):
        """Close the WebDriver instance."""
        if self.driver:
            self.driver.quit()
