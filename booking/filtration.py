from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class BookingFiltration:

    def __init__(self,driver:WebDriver) -> None:
        self.driver = driver

    def star_rating(self,rating):
        try:
            star_div = self.driver.find_element(By.CSS_SELECTOR,'div[class="_962ef834c cbe47aa30e"]')
        finally:
            if ((rating<6) and (rating >1)):
                child = self.driver.find_element(By.CSS_SELECTOR,f'input[id="__bui-{rating + 15}"]')
                self.driver.implicitly_wait(10)
                ActionChains(self.driver).move_to_element(child).click(child).perform()