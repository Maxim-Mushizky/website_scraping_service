import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from datetime import datetime
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Yad2SApartmentScraper:

    def __init__(self, base_url: str = "https//yad2.co.il/",
                 option_clicker: str = "//img[starts-with(@alt, 'נדל')]"):
        self._user_agent = UserAgent()
        self._options = webdriver.ChromeOptions()
        self._options.add_argument(f'user-agent={self._user_agent.random}')
        self.driver = webdriver.Chrome()
        self.driver.get(base_url)
        self.wait = WebDriverWait(self.driver, random.random() * random.randint(3, 12))
        sleep(random.random() * random.randint(3, 12))
        self.driver.find_element(By.XPATH, option_clicker).click()
        self.add_random_mouse_movement()

    def get_win_visible_area_size(self):
        return self.driver.execute_script(
            "return [window.innerWidth, window.innerHeight];"
        )

    def add_random_mouse_movement(self, rand_range: tuple[int, int] = (0, 12)):
        """
        Purpose of this method is to add random behavior to the page, so it will less likely will
        be caught by Captcha algorithms
        :return:
        """
        visible_area_size = self.get_win_visible_area_size()
        max_x = visible_area_size[0]
        max_y = visible_area_size[1]

        # Create an instance of ActionChains
        actions = ActionChains(self.driver)

        # Move the mouse cursor around randomly
        for _ in range(random.randint(*rand_range)):  # Perform 10 random movements
            # Generate random coordinates within the browser window
            x = random.randint(0, max_x // 10)
            y = random.randint(0, max_y // 10)

            # Perform the mouse movement
            actions.move_by_offset(x, y).perform()

    def _compose_apartment_listing_url(self,
                                       city_code: int,
                                       min_price: int,
                                       max_price: int,
                                       min_rooms: int,
                                       max_rooms: int) -> str:

        url = f"https://www.yad2.co.il/realestate/forsale?topArea=25&area=53&city={city_code}&propertyGroup=apartments" \
              f"&rooms={min_rooms}-{max_rooms}&price={min_price}-{max_price}"

    def search_apartment_listings(self,
                                  city_code: int,
                                  min_price: int,
                                  max_price: int,
                                  min_rooms: int,
                                  max_rooms: int) -> list[dict]:
        results = []
        self.driver.get(self._compose_apartment_listing_url(city_code, min_price, max_price, min_rooms, max_rooms))
        while True:
            # Wait for the dynamic content to load
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'feeditem')))

            # Extract the page HTML source
            html = self.driver.page_source

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Find the apartment listings on the page
            apartment_listings = soup.find_all('div', class_='feeditem')

            for listing in apartment_listings:
                result_map = {}
                title = listing.find('span', class_='title').text.strip()
                price_element = listing.find('div', class_='price').text.strip()
                description = listing.find('span', class_='subtitle').text.strip()
                rooms = listing.find('div', class_='rooms-item').text.strip()
                area = listing.find("div", class_="data SquareMeter-item").text.strip()
                merchant = listing.find("div", class_="merchant").text.strip()

                result_map['title'] = title
                result_map['description'] = description
                result_map['price_element'] = price_element
                result_map['rooms'] = rooms
                result_map['area'] = area
                result_map['merchant'] = merchant

                results.append(result_map)
            # Scroll to the bottom of the page
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

            # Wait for a short interval before scrolling again
            time.sleep(random.random() * random.randint(1, 12))
            break
        return results
