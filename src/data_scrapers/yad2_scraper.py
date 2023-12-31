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

from my_config_reader import MyConfig

USER_AGENT = UserAgent()
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument(f'user-agent={USER_AGENT.random}')


class Yad2SApartmentScrapingAgent:

    def __init__(self, base_url: str = MyConfig.yad2_url,
                 option_clicker: str = "//img[starts-with(@alt, 'נדל')]"):
        self.driver = webdriver.Chrome()
        self.driver.get(base_url)
        self.wait = WebDriverWait(self.driver, random.random() * random.randint(3, 12))
        sleep(random.uniform(3.0, 12.0))
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

        return f"https://www.yad2.co.il/realestate/forsale?topArea=25&area=53&city={city_code}&propertyGroup=apartments" \
               f"&rooms={min_rooms}-{max_rooms}&price={min_price}-{max_price}"

    def _fetch_listing_objects(self, listing) -> dict:
        result_map = {}
        result_map['title'] = listing.find('span', class_='title').text.strip()
        result_map['description'] = listing.find('span', class_='subtitle').text.strip()
        result_map['price_element'] = listing.find('div', class_='price').text.strip()
        result_map['rooms'] = listing.find('div', class_='rooms-item').text.strip()
        result_map['area'] = listing.find("div", class_="data SquareMeter-item").text.strip()
        result_map['merchant'] = listing.find("div", class_="merchant").text.strip()
        return result_map

    def search_apartment_listings(self,
                                  city_code: int,
                                  min_price: int,
                                  max_price: int,
                                  min_rooms: int,
                                  max_rooms: int) -> list[dict]:
        self.driver.get(self._compose_apartment_listing_url(city_code, min_price, max_price, min_rooms, max_rooms))
        while True:
            # Wait for the dynamic content to load
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'feeditem')))
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            apartment_listings = soup.find_all('div', class_='feeditem')
            results = [self._fetch_listing_objects(listing) for listing in apartment_listings]
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

            # Wait for a short interval before scrolling again
            time.sleep(random.uniform(1.0, 12.0))
            break
        return results


if __name__ == '__main__':
    city_code = 1139

    min_price = 1000000  # Minimum price range
    max_price = 1700000  # Maximum price range

    min_rooms = 3
    max_rooms = 5

    agent = Yad2SApartmentScrapingAgent()
    res = agent.search_apartment_listings(city_code, min_price, max_price, min_rooms, max_rooms)
    print(res)
