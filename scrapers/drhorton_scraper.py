# scrapers/drhorton_scraper.py
import time
import html
from bs4 import BeautifulSoup
from core.base_scraper import BaseScraper
from utils.helpers import clean_text, timeit
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, as_completed
from config.constants import DRHORTON_BASE_URL, DRHORTON_COMMUNITY_ABOUT_CLASS, DRHORTON_COMMUNITY_AMENITIES_CLASS, DRHORTON_COMMUNITY_AREA_CLASS, DRHORTON_COMMUNITY_AREA_INFO_ID, DRHORTON_COMMUNITY_AVAILABLE_HOMES_ID, DRHORTON_COMMUNITY_FLOORPLANS_ID, DRHORTON_COMMUNITY_NEARBY_COMMUNITIES_ID, DRHORTON_COMMUNITY_PAGINATION_BUTTON_CLASS, DRHORTON_COMMUNITY_CARD_CLASS, DRHORTON_COMMUNITY_PRICE_CLASS, DRHORTON_COMMUNITY_TYPE_CLASS, DRHORTON_COMMUNITY_ADDRESS_CLASS, DRHORTON_COMMUNITY_AVAILABLE_HOMES_CLASS, DRHORTON_SEARCH_BOX_ID, DRHORTON_SEARCH_RESULT_TARGET_ID
from config.settings import config
from utils.logger import Logger

logger = Logger(config.LOG_TO_FILE, config.LOG_FILE_NAME).get_logger()
class DRHortonScraper(BaseScraper):
    def get_search_url(self, search_term: str) -> str:
        self.load_page_with_wait(DRHORTON_BASE_URL, 10)
        self.remove_privacy_banner()
        try:
            search_box = self.driver.find_element(By.ID, DRHORTON_SEARCH_BOX_ID)
            search_box.clear()
            search_box.send_keys(search_term)
            # wait for autocomplete widget to load
            time.sleep(2)
            try:
                search_result_link = self.driver.find_element(By.ID, DRHORTON_SEARCH_RESULT_TARGET_ID)
                search_result_link.click()
                time.sleep(2)
            except Exception as e:
                # print("unable to locate search result", repr(e))
                logger.exception("unable to locate search result", repr(e))
        except Exception as e:
            logger.exception("unable to locate search box", repr(e))
        # get the page url
        return self.driver.current_url
     
    def extract_community_data(self, url: str) -> list[dict]:
        self.driver.get(url)
        time.sleep(10)
        page_html = self.driver.page_source
        soup = BeautifulSoup(page_html, 'lxml')
        communities = []
        print("scraping the communities list")
        for community in soup.find_all('a', class_=DRHORTON_COMMUNITY_CARD_CLASS):
            try:
                title = clean_text(community.find('h2').text.strip())
                address = clean_text(community.find('div', class_=DRHORTON_COMMUNITY_ADDRESS_CLASS).text.strip())
                start_price = clean_text(community.find('div', class_=DRHORTON_COMMUNITY_PRICE_CLASS).text.strip())
                property_type = clean_text(community.find('div', class_=DRHORTON_COMMUNITY_TYPE_CLASS).text.strip())
                property_area = clean_text(community.find('div', class_=DRHORTON_COMMUNITY_AREA_CLASS).text.strip())
                available_homes_div = community.find('div', class_=DRHORTON_COMMUNITY_AVAILABLE_HOMES_CLASS)
                available_homes = clean_text(available_homes_div.text.strip()) if available_homes_div else 'N/A'
                details_link = DRHORTON_BASE_URL + community['href']

                communities.append({
                    'community_name': title,
                    'address': address,
                    'start_price': start_price,
                    'property_type': property_type,
                    'property_area': property_area,
                    'available_homes': available_homes,
                    'details_link': details_link
                })
            except AttributeError:
                continue  # Skip if data is missing
            # self.driver.quit()
        return communities

    @timeit
    def scrape_community_list(self, soup):
        communities = []
        logger.info("scraping the communities list")
        for community in soup.find_all('a', class_=DRHORTON_COMMUNITY_CARD_CLASS):
            try:
                title = clean_text(community.find('h2').text.strip())
                address = clean_text(community.find('div', class_=DRHORTON_COMMUNITY_ADDRESS_CLASS).text.strip())
                start_price = clean_text(community.find('div', class_=DRHORTON_COMMUNITY_PRICE_CLASS).text.strip())
                property_type = clean_text(community.find('div', class_=DRHORTON_COMMUNITY_TYPE_CLASS).text.strip())
                property_area = clean_text(community.find('div', class_=DRHORTON_COMMUNITY_AREA_CLASS).text.strip())
                available_homes_div = community.find('div', class_=DRHORTON_COMMUNITY_AVAILABLE_HOMES_CLASS)
                available_homes = clean_text(available_homes_div.text.strip()) if available_homes_div else 'N/A'
                details_link = DRHORTON_BASE_URL + community['href']

                communities.append({
                    'community_name': title,
                    'address': address,
                    'start_price': start_price,
                    'property_type': property_type,
                    'property_area': property_area,
                    'available_homes': available_homes,
                    'details_link': details_link
                })
            except AttributeError:
                continue  # Skip if data is missing
        return communities
    
    @timeit
    def extract_details_page_data(self, details_url: str) -> dict:
        logger.info(f"scraping community details from {details_url}")
        try:
            scraper = DRHortonScraper()
            scraper.load_page_with_wait(details_url)
            scraper.remove_privacy_banner()
            soup = scraper.get_beautiful_soup(scraper.driver.page_source)

            about_community = scraper.extract_about_community(soup)
            amenities = scraper.extract_community_amenities(soup)
            schools = scraper.extract_schools(soup)
            floor_plans = scraper.extract_floorplans(soup)
            return {
                'about_community': about_community,
                'amenities': amenities,
                'schools': schools,
                'floorplans': floor_plans,
                'area_information': scraper.extract_area_info(soup),
                'available_homes': scraper.extract_available_homes(soup),
                'nearby_communities': scraper.extract_nearby_communities(soup)
            }
        except Exception as e:
            logger.exception("unable to extract community details" , repr(e))
        return {}

    @timeit
    def extract_about_community(self,soup):
        try:
            about_section = soup.find('div', class_=DRHORTON_COMMUNITY_ABOUT_CLASS).find('p').text.strip()
            more = soup.find('div', class_='slide-content').text.strip()
            about_section += '. ' + more
            about_section = html.escape(about_section)  # Remove HTML entities
            return clean_text(about_section)
        except AttributeError:
            return None

    # Function to extract "Community amenities" from the details page
    @timeit
    def extract_community_amenities(self,soup):
        try:
            amenities_list = [html.escape(li.text.strip()) for li in soup.find('ul', class_=DRHORTON_COMMUNITY_AMENITIES_CLASS).find_all('li')]
            return ', '.join(amenities_list)
        except AttributeError:
            return []

    # Function to extract "Schools" from the details page
    @timeit
    def extract_schools(self, soup):
        try:
            school_info = []
            school_section = soup.find_all('h3', string='Schools')[0].find_next_siblings('p')
            for school in school_section:
                school_name = school.find('a').text.strip()
                grades = school.contents[2].strip()
                distance = school.find('span', class_='distance').text.strip()
                school_info.append(f"{school_name}: {grades}, {distance}")
            return ', '.join(school_info)
        except (AttributeError, IndexError):
            return []

    # Function to extract "Available homes in this community" (floorplans) from the details page
    @timeit
    def extract_floorplans(self, soup):
        try:
            floorplans = []
            floorplan_items = soup.find('div', id=DRHORTON_COMMUNITY_FLOORPLANS_ID).find_all('div', class_='toggle-item')
            for item in floorplan_items:
                plan_name = item.find('h2', class_='pr-case').text.strip()
                price = item.find('h3').text.strip()
                details = item.find('p').text.strip().replace('\n', ' ').replace('  ', ' ')
                floorplans.append(f"{plan_name}: {price}, {details}")
            return ', '.join(floorplans)
        except AttributeError:
            return []

    # Function to extract "Area information" from the details page
    @timeit
    def extract_area_info(self, soup):
        try:
            area_info_section = soup.find('section', id=DRHORTON_COMMUNITY_AREA_INFO_ID).find('div', class_='area-blurb').text.strip()
            area_info_section = html.escape(area_info_section)
            return clean_text(area_info_section)
        except AttributeError:
            return None

    # Function to extract "Available homes in this community"
    @timeit
    def extract_available_homes(self, soup):
        """
        Extracts a list of dictionaries describing the available homes in a community.

        Given a BeautifulSoup object representing a community details page, extracts
        the available homes section and creates a list of dictionaries containing the
        following keys:
            - 'price': The price of the home
            - 'address': The address of the home
            - 'floorplan': The floorplan name of the home
            - 'specs': A string describing the home's specifications
            - 'estimate': An estimated monthly payment for the home (or 'N/A' if not available)

        Returns an empty list if no available homes are found on the page.
        """

        available_homes = []
        try:
            home_cards = soup.find('div', id=DRHORTON_COMMUNITY_AVAILABLE_HOMES_ID).find_all('div', class_='toggle-item')
            for home in home_cards:
                price = clean_text(home.find('h2').contents[0].text.strip())
                address = clean_text(home.find('h3').text.strip())
                floorplan = clean_text(home.find('span', class_='pr-case').text.strip())

                # Extract the home specs (beds, baths, garage, stories, square footage)
                specs_paragraph = home.find_all('p')[1].text.strip()
                specs = clean_text(specs_paragraph)

                # Extract estimated monthly payment
                estimate = home.find('span', class_='estimate').text.strip() if home.find('span', class_='estimate') else 'N/A'
                estimate = clean_text(estimate)
                available_homes.append({
                    'price': price,
                    'address': address,
                    'floorplan': floorplan,
                    'specs': specs,
                    'estimate': estimate
                })
        except AttributeError:
            pass  # Return empty if no homes available

        return available_homes

    # Function to extract "Nearby communities"
    @timeit
    def extract_nearby_communities(self, soup):
        """
        Extracts a list of dictionaries containing the name and address of nearby communities
        from a given soup object.

        Returns:
            list[dict]: A list of dictionaries where each dictionary has the keys
                'community_name' and 'address' describing a nearby community.
        """
        nearby_communities = []
        try:
            nearby_cards = soup.find('div', id=DRHORTON_COMMUNITY_NEARBY_COMMUNITIES_ID).find_all('div', class_='toggle-item')
            for community in nearby_cards:
                name = clean_text(community.find('h2').text.strip())
                address = clean_text(community.find('div', class_='home-info__address').text.strip())

                nearby_communities.append({
                    'community_name': name,
                    'address': address
                })
        except AttributeError:
            pass  # Return empty if no nearby communities

        return nearby_communities
    
    @timeit
    def scrape(self, search_term: str="raleigh") -> list[dict]:
        """
        Scrapes community pages and extracts all the required data.

        Returns:
            list[dict]: A list of dictionaries containing the scraped data for each community.
        """
        try:
            self.driver.maximize_window()
            # Scrape all community pages
            search_result_url = self.get_search_url(search_term)
            logger.info(f"scraping: {search_result_url}")

            communities: list[dict] = self.scrape_community_pages(search_result_url)
            logger.info(f"Total Communities: {len(communities)}")

            # Scrape details for each community
            # enriched_communities: list[dict] = self.scrape_details_parallel(communities, 3)
            # Save to file
            # if len(enriched_communities) > 0:
            #     self.save_to_file(enriched_communities, 'data/dr_horton_scraped_communities.json')

        except Exception as e:
            logger.exception(f"Error scraping: {e}")
        return communities

    def remove_privacy_banner(self):
        try:
            element = self.driver.find_element(By.ID, 'onetrust-banner-sdk')
            self.driver.execute_script("""
                var element = arguments[0];
                element.parentNode.removeChild(element);
            """, element)
        except Exception as e:
            pass    
    @timeit
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
    
    @timeit
    def scrape_community_pages(
        self,
        url: str,  # The URL of the first page to scrape
        max_pages: int = 10  # The maximum number of pages to scrape
    ) -> list[dict]:  # A list of dictionaries with community information
        """
        Scrapes multiple community pages in sequence.

        Args:
            url (str): The URL of the first page to scrape.
            max_pages (int, optional): The maximum number of pages to scrape. Defaults to 10.

        Returns:
            list[dict]: A list of dictionaries with community information.
        """
        all_communities = []
        current_page = 1
        self.load_page_with_wait(url, 10)
        page_buttons = self.driver.find_elements(By.CLASS_NAME, DRHORTON_COMMUNITY_PAGINATION_BUTTON_CLASS)
        page_count = len(page_buttons) - 1  # remove the next page button
        logger.info(f"page_count: {page_count}")
        self.remove_privacy_banner()

        while current_page <= max_pages and current_page <= page_count:
            logger.info(f"scraping page {current_page}...")
            soup = self.get_beautiful_soup(self.driver.page_source)
            # Extract communities data from the current page
            communities = self.scrape_community_list(soup)
            all_communities.extend(communities)
            # Try to find the "Next" button and click it (if applicable)
            try:
                if current_page < page_count:
                    next_button = self.driver.find_element(By.ID, 'btn-' + str(current_page+1))  # Adjust if the button is different
                    logger.debug('clicking next page btn-' + str(current_page+1))
                    self.driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(5)  # Give the page some time to load
            except Exception as e:
                logger.debug("No more pages to scrape or 'Next' button not found.")
                break
            current_page += 1
        
        self.close_driver()  # Close the driver once done with all pages
        return all_communities

    # Function to scrape multiple details pages in parallel
    @timeit
    def scrape_details_parallel(
        self,
        communities: list[dict],  # List of dictionaries with community info
        max_workers: int = 5  # Number of threads to use
    ) -> list[dict]:  # List of dictionaries with enriched community info

        """
        Scrapes multiple details pages in parallel.

        Args:
        - communities (list[dict]): List of dictionaries with community info
        - max_workers (int): Number of threads to use (default: 5)

        Returns:
        - list[dict]: List of dictionaries with enriched community info
        """
        enriched_communities = []
        communities = communities[:6]
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_community = {
                executor.submit(self.extract_details_page_data, community['details_link']): community
                for community in communities
            }

            # Iterate through the futures as they complete
            for future in as_completed(future_to_community):
                community_info = future_to_community[future]
                try:
                    details_data = future.result()  # Get details page data
                    # Merge the details with the main community info
                    community_info.update(details_data)
                    enriched_communities.append(community_info)
                    logger.info(f"scraped details for {community_info['community_name']}")
                except Exception as e:
                    logger.exception(f"error scraping details for {community_info['community_name']}: {e}")
        
        return enriched_communities
