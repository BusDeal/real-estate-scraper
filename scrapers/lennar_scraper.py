import requests
from core.base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from concurrent.futures import ThreadPoolExecutor, as_completed
from config.constants import LENNAR_AMENITIES_CONTAINER_CLASS, LENNAR_AMENITIES_NAME_LABEL_CLASS, LENNAR_AMENITIES_ROOT_DIV_CLASS, LENNAR_BASE_URL, LENNAR_COMMUNITY_AMENITIES_LINK_CLASS, LENNAR_COMMUNITY_CARD_BADGE_CLASS, LENNAR_COMMUNITY_CARD_CLASS, LENNAR_COMMUNITY_CARD_LINK_CLASS, LENNAR_COMMUNITY_CARD_OVERVIEW_CLASS, LENNAR_COMMUNITY_CARD_PRICE_ADDRESS_CLASS, LENNAR_COMMUNITY_CARD_STATUS_CLASS, LENNAR_COMMUNITY_CARD_TITLE_CLASS, LENNAR_COMMUNITY_NEARBY_PLACES_LINK_CLASS, LENNAR_CONTACT_LINK_SELECTOR, LENNAR_GRAPHQL_API_URL, LENNAR_HOME_DETAILS_WRAPPER_CLASS, LENNAR_HOME_ITEM_CLASS, LENNAR_HOME_LISTING_CONTAINER_CLASS, LENNAR_HOME_NEARBY_SCHOOLS_CLASS, LENNAR_HOME_PRICE_SIDEBAR_ID, LENNAR_HOME_SITE_ID, LENNAR_HOMESITE_ID_CLASS, LENNAR_LINK_ELEMENT_SELECTOR, LENNAR_POIS_CONTAINER_CLASS, LENNAR_SEARCH_BOX_ID, LENNAR_SEARCH_RESULT_TARGET_LINK_SELECTOR, LENNAR_SEARCH_URL
from config.settings import config
from utils.helpers import timeit
from utils.logger import Logger
import time

logger = Logger(config.LOG_TO_FILE, config.LOG_FILE_NAME).get_logger()

class LennarScraper(BaseScraper):
    def extract_community_data(self) -> list:
        return self.scrape()

    def _get_search_payload(self, search_term: str) -> dict:
        return {
            "operationName": "SearchQueryNew",
            "variables": {
                "input": search_term,
                "first": 3,
                "marketCode": "AUS"
            },
            "query": """query SearchQueryNew($input: String, $first: Int, $type: String, $marketCode: String) {
                search(input: $input, first: $first, marketCode: $marketCode, type: $type) {
                    type
                    results {
                        name
                        subtext
                        url
                    }
                    totalResults
                }
            }"""
        }
    
    def get_search_url(self, search_term: str) -> str:
        headers = get_request_headers()
        payload = self._get_search_payload(search_term)
        try:
           response = requests.post(LENNAR_GRAPHQL_API_URL, headers=headers, json=payload)
           response.raise_for_status()
           data = response.json().get('data').get('search')
           if len(data) == 0:
               raise Exception("unable to find any results for search")
           results = list(filter(lambda x: x['type'] == 'CITY', data))
           if len(results) == 0:
               raise Exception("unable to find any results for search")
           cities = results[0]
           return LENNAR_BASE_URL + cities["results"][0]["url"]

        except Exception as e:
            print("error in getting the search results", repr(e))
        return ""
    
    def remove_privacy_notice_popup(self, driver = None):
        try:
            driver = driver if driver else self.driver
            element = driver.find_element(By.ID, 'onetrust-consent-sdk')
            driver.execute_script(""" 
                var element = arguments[0];
                if (element) {element.remove();} 
            """, element)
        except Exception as e:
            pass
        try:
            driver.execute_script(""" 
                var element = document.getElementById('onetrust-consent-sdk');
                if (element) { element.remove();} 
            """)
        except:
            pass

    def remove_ads_banner(self, driver=None):
        driver = driver if driver else self.driver
        driver.execute_script("""
            document.querySelectorAll('.MessageBarV2_backgroundAnimatedContainer__n4Xt4').forEach(e => e.remove());
            document.querySelectorAll('.Panel_overlay__M2jRh').forEach(e => e.remove()); 
        """)

    def page_clean_up(self, driver=None):
        self.remove_ads_banner(driver)
        self.remove_privacy_notice_popup(driver)

    def scrape(self, search:str = "raleigh"):
        communities = []
        self.driver.maximize_window()
        try:
            search_url = self.get_search_url(search)
            # print("search url: ", search_url)
            if len(search_url) == 0:
                logger.error("unable to find any results for search")
                return communities
            self.load_page_with_wait(search_url)
        except Exception as e:
            logger.exception("error in getting the search results", repr(e))
            return communities
        
        # remove popup
        self.remove_privacy_notice_popup()
        # Step 2: Click the "Communities" button
        self._click_communities_button()
        while self._load_more_communities():
            print("loading more communities...")
            time.sleep(1)
        else:
            print("no more communities to load")

        # Step 3: Scrape the community list
        soup = self.get_beautiful_soup(self.driver.page_source)
        communities = self.scrape_community_list(soup)
        logger.info(f"communities found: {len(communities)}")
        # print(json.dumps(communities, indent=4))
        self.close_driver()
        if len(communities) == 0:
            logger.error("unable to find any communities")
            return communities
        # Step 4: Scrape the details for each community
        communities = communities[:4]
        enriched_communities = self.scrape_details_parallel(communities, config.SCRAPER_DEFAULT_CONCURRENCY)
        self.save_to_file(enriched_communities, config.SCRAPER_OUTPUT_DIR +'lennar_scraped_communities.json')
        return communities
    def _click_communities_button(self):
        # Locate the Communities button by text or other attributes and click it 
        # search-results-tab-count-index-available 
        try:
            self.driver.execute_script("""document.getElementsByClassName("SearchResultsTabs_tab__ZjaY_")[1].click()""")
            time.sleep(1)  # Allow time for the community list to load
        except Exception as e:
            print("unable to locate community button", repr(e))

    def _load_more_communities(self):
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, '.ListSection_loadMore__e9_jP > .Button_root__8nq_L')
            if btn:
                self.driver.execute_script("""document.querySelector('.ListSection_loadMore__e9_jP > .Button_root__8nq_L').click()""")
                time.sleep(1)  # Allow time for the community list to load
                return True
            return False
        except Exception as e:
            # print("unable to locate community button", repr(e))
            return False
    
    @timeit
    def scrape_community_list(self, soup):
        communities = []
        
        print("started scraping community list")
        community_cards = soup.find_all('div', class_=LENNAR_COMMUNITY_CARD_CLASS)

        for card in community_cards:
            community = {}
            # Extract community name, badge, link, InfoCard_info, status, title, meta details, address, and overview
            title = card.find('h3', class_=LENNAR_COMMUNITY_CARD_TITLE_CLASS)
            community['community_name'] = title.text.strip() if title else None

            link_tag = card.find('a', class_=LENNAR_COMMUNITY_CARD_LINK_CLASS)
            if link_tag:
                community['details_link'] = LENNAR_BASE_URL + link_tag.get('href')

            badge = card.find('span', class_=LENNAR_COMMUNITY_CARD_BADGE_CLASS)
            community['badge'] = badge.text.strip() if badge else None

            status = card.find('span', class_=LENNAR_COMMUNITY_CARD_STATUS_CLASS)
            community['status'] = status.text.strip() if status else None

            meta_details = card.find_all('p', class_=LENNAR_COMMUNITY_CARD_PRICE_ADDRESS_CLASS)
            community['price'] = meta_details[0].text.strip() if len(meta_details) > 0 else ""
            community['address'] = meta_details[1].text.strip() if len(meta_details) > 1 else ""

            overview = card.find('p', class_=LENNAR_COMMUNITY_CARD_OVERVIEW_CLASS)
            community['overview'] = overview.text.strip() if overview else None
            communities.append(community)

        return communities

    def extract_details_page_data(self, details_url: str) -> dict:
        return self.scrape_home_details(details_url)
    @timeit
    def available_homes(self, soup):
        try:
            print("extracting available homes from listing")
            homes_container = soup.find('div', class_=LENNAR_HOME_LISTING_CONTAINER_CLASS)
            homes = homes_container.find_all('a', class_=LENNAR_HOME_ITEM_CLASS)
        except Exception as e:
            print("unable to locate homes container ", repr(e))
            return []
       
        # Initialize list to store extracted data
        homes_data = []
        print(f"found {len(homes)} homes in listing")
        # Iterate over each home and extract details
        for home in homes:
            home_data = {}
            # Extract homesite_id (inside <p> with class 'bodycopySmallNew Typography_bodycopySmallNew__4lltu')
            homesite_id = home.find('p', class_=LENNAR_HOMESITE_ID_CLASS).text.strip()
            home_data['site_id'] = homesite_id
            try:
                details = home.find_all('p')
                if(len(details) == 0):
                    print("unable to extract home details due to less information, length: ", len(details))
                    continue
                home_data['site_id'] = details[0].text.strip()
                home_data['price'] = details[1].text.strip()
                home_data['plan'] = details[3].text.strip()
                home_data['home_details'] = details[2].text.strip()
                home_data['address'] = details[4].text.strip()

            except Exception as e:
                print("unable to extract home details", repr(e))
                continue
            
            # Extract details page link (href attribute of the <a> tag)
            details_link = home['href']
            home_data['details_link'] = f"{LENNAR_BASE_URL}{details_link}"  # Add base URL as needed
            # Add the extracted home data to the list
            homes_data.append(home_data)
            # print("extracted home data: ", home_data)
        return homes_data

    @timeit
    def scrape_community_page_data(self, url: str) -> dict:
        print("scraping community page data from ", url)
        scraper = LennarScraper()
        scraper.load_page_with_wait(url)
        # self.wait_for_element(By.CSS_SELECTOR, 'a.HomesitesTableNew_rowButton__EDamq')
        # self.wait_for_element(By.CLASS_NAME, 'MessageBarV2_backgroundAnimatedContainer__n4Xt4')
        # self.wait_for_element(By.CLASS_NAME, 'AmenitiesModalContent_root__AUXpm')
        scraper.driver.execute_script("""
            document.querySelectorAll('.MessageBarV2_backgroundAnimatedContainer__n4Xt4').forEach(e => e.remove());
            document.querySelectorAll('.Panel_overlay__M2jRh').forEach(e => e.remove()); 
        """)
        time.sleep(1)
        scraper.remove_privacy_notice_popup()
        soup = scraper.get_beautiful_soup(scraper.driver.page_source)

        amenities_link_element = soup.select_one(LENNAR_COMMUNITY_AMENITIES_LINK_CLASS)
        nearby_places_element = soup.select_one(LENNAR_COMMUNITY_NEARBY_PLACES_LINK_CLASS)
        amenities_link = LENNAR_BASE_URL+ amenities_link_element.attrs.get('href') if amenities_link_element else ""
        print("amenities link: ", amenities_link)
        nearby_places_link = LENNAR_BASE_URL+ nearby_places_element.attrs.get('href') if nearby_places_element else ""
    
        print("nearby places link: ", nearby_places_link)
        print("extracting amenities and nearby places")
        amenities = scraper.extract_amenities(amenities_link) if amenities_link else []
        nearby_places = scraper.extract_places_nearby(nearby_places_link) if nearby_places_link else []
        print(f"amenities: {len(amenities)}, nearby places found: {len(nearby_places)}")
        # Find all homes in the list
        homes = scraper.available_homes(soup)
        scraper.driver.quit()
        homes = self.add_home_site_info(homes)
        return {'homes': homes, 'amenities': amenities, 'nearby_places': nearby_places}
    
    @timeit
    def add_home_site_info(self, homes: dict) -> dict:
        for home in homes:
            details_link = home['details_link']
            home['site_info'] = self.scrape_home_details(details_link)
            # print(home['site_info'])

        # with ThreadPoolExecutor(max_workers=4) as executor:
        #     futures = {executor.submit(self.scrape_home_details, link): link for link in links}
        #     for future in as_completed(futures):
        #         link = futures[future]
        #         try:
        #             data = future.result()
        #         except Exception as exc:
        #             print('%r generated an exception: %s' % (link, exc))
        #         else:
        #             for home in homes:
        #                 if home['details_link'] == link:
        #                     home['site_info'] = data
        #                     break
        return homes
    
    @timeit
    def scrape_home_details(self, details_url: str) -> dict:
        print("scraping home details from ", details_url)
        scraper = LennarScraper()
        scraper.load_page_with_wait(details_url)
        scraper.page_clean_up()
        # Initialize BeautifulSoup object
        soup = scraper.get_beautiful_soup(scraper.driver.page_source)
        try:
            # Extract homesite status
            homesite_status = soup.find('p', id=LENNAR_HOME_SITE_ID).text.strip()
            # Extract price
            price = soup.find('h2', id=LENNAR_HOME_PRICE_SIDEBAR_ID).text.strip()

            # Select the div containing the home details and address
            details_wrapper = soup.find('div', class_=LENNAR_HOME_DETAILS_WRAPPER_CLASS)
            # Extract homesite details (first <p> tag)
            if details_wrapper:
                para = details_wrapper.find_all('p')
                homesite_details = para[0].text.strip() if para is not None else None
                # Extract address (second <p> tag)
                address = para[1].text.strip() if len(para) >= 2 else None

            # Extract contact number (without the text)
            try:
                contact_number = soup.select(LENNAR_CONTACT_LINK_SELECTOR)[0]['href'].replace('tel:', '')
            except Exception as e:
                contact_number = 'NA'
                print("unable to extract contact number ", repr(e))

            links_elements = soup.select(LENNAR_LINK_ELEMENT_SELECTOR)
            links = [LENNAR_BASE_URL + link_element['href']  for link_element in links_elements]
            # filter links and exclude link that ends with faq
            links = [link for link in links if not link.endswith('faq')]
            print("links: ", links)

        except Exception as e:
                print("failed to scrape home details", repr(e))
                return {}
        # Store the data in a dictionary
        homesite_info = {
            'homesite_status': homesite_status,
            'price': price,
            'homesite_details': homesite_details,
            'address': address,
            'contact_number': contact_number,
            'links': links
        }

        # Extract nearby schools and places
        print("extracting homesite nearby schools and places")
        try:
            for link in links:
                if link.endswith('nearby-schools'):
                    schools = scraper.extract_schools_nearby_home(link)
                    homesite_info['schools'] = schools
                elif link.endswith('nearby-places'):
                    places = scraper.extract_places_nearby(link)
                    homesite_info['nearby_places'] = places
        except Exception as e:
            print("failed to extract nearby schools and places", repr(e))
        finally:
            scraper.driver.quit()

        return homesite_info

    @timeit
    def extract_schools_nearby_home(self, url: str) -> list:
        schools_info = []
        try:
            page_html = self.load_page_with_wait(url)
            soup = self.get_beautiful_soup(page_html)
            # Find all divs containing school information
            school_items = soup.find_all('div', class_=LENNAR_HOME_NEARBY_SCHOOLS_CLASS)

            # Loop through each school item and extract details
            for item in school_items:
                school_name = item.find('p', class_='headline3').text.strip()
                school_type_grade = item.find_all('p', class_='bodycopySmall')[0].text.strip()
                school_district = item.find_all('p', class_='bodycopySmall')[1].text.strip()
                school_rating = item.find('span', class_='subheadlineSmall').text.strip()
                niche_link = item.find('a', class_='SchoolListItem_link__rZVjX')['href']
                
                # Store school details in a dictionary
                school_info = {
                    'school_name': school_name,
                    'school_grade': school_type_grade,
                    'school_district': school_district,
                    'school_rating': school_rating,
                    'niche_link': niche_link
                }    
                # Append the school info to the list
                schools_info.append(school_info)
            print(f"found {len(schools_info)} schools")
        except Exception as e:
            print("error extracting schools: ", repr(e))
  
        return schools_info
    @timeit
    def extract_places_nearby(self, url: str) -> list:
        try:
            html_content = self.load_page_with_wait(url)
            soup = self.get_beautiful_soup(html_content)
            # self.wait_for_element(By.CLASS_NAME, 'PointsOfInterestListItem_listItem__cJ17m')
            # Extract POIs information
            poi_list = []
            pois = soup.find_all('div', class_=LENNAR_POIS_CONTAINER_CLASS)
            for poi in pois:
                name = poi.find('p', class_='headline3').get_text(strip=True)
                details = poi.find('p', class_='bodycopySmall').get_text(strip=True)
                rating_info = poi.find('div', class_='Rating_root__i2oym')['aria-label']
                
                # Extract rating and number of reviews
                rating = rating_info.split(' out of ')[0].strip()
                reviews = rating_info.split('based on ')[-1].split(' reviews')[0].strip()

                # Append the extracted data
                poi_list.append({
                    'name': name,
                    'details': details,
                    'rating': rating,
                    'reviews': reviews
                })
        except Exception as e:
            print(f"Error occurred while extracting POIs: {e}")

        return poi_list
    @timeit
    def extract_amenities(self, url):
        '''
        Extracts the amenities from the Lennar community page
        '''
        try:
            # scraper = LennarScraper()
            self.load_page_with_wait(url,3)
            # self.wait_for_element(By.CLASS_NAME, 'AmenitiesModalContent_root__AUXpm')
            soup = self.get_beautiful_soup(self.driver.page_source)
            amenities = soup.find('div', class_=LENNAR_AMENITIES_ROOT_DIV_CLASS)
            # print(len(amenities))
            amenities_list = []
            if amenities:
                amenity_items = amenities.find_all('div', class_=LENNAR_AMENITIES_CONTAINER_CLASS)
                for item in amenity_items:
                    amenity_name = item.find('p', class_=LENNAR_AMENITIES_NAME_LABEL_CLASS).text.strip()
                    amenity_details = item.find('p', class_='bodycopySmall').text.strip()
                    amenities_list.append({
                        'name': amenity_name,
                        'details': amenity_details
                    })

            # print(f"found {len(amenities_list)} amenities")
            return amenities_list
        except Exception as e:
            print(f"Error occurred while scraping amenities: {e}")
            return []

    @timeit    
    def scrape_details_parallel(self, communities, max_workers=4):
        enriched_communities = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_community = {
                executor.submit(self.scrape_community_page_data, community['details_link']): community
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
                    print(f"Scraped details for {community_info['community_name']}")
                    # print(community_info)
                except Exception as e:
                    print(f"Error scraping details for {community_info['community_name']}: {e}")
        
        return enriched_communities

def get_request_headers():
    return {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'authorization': '',
        'content-type': 'application/json',
        'origin': LENNAR_BASE_URL,
        'priority': 'u=1, i',
        'referer': LENNAR_BASE_URL,
        'sec-ch-ua': '"Google Chrome";v="129", "Chromium";v="129"',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }