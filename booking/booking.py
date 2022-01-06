from selenium import webdriver
import os
from booking.constants import BASE_URL
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support.ui import Select
from booking.filtration import BookingFiltration
from prettytable import PrettyTable


class Booking(webdriver.Chrome):
    def __init__(self,driver_path='/usr/lib/chromium-browser/chromedriver'):
        self.driver_path = driver_path
        os.environ['PATH'] += driver_path
        super(Booking,self).__init__()
        self.implicitly_wait(15)
    def open_page(self):
        self.get(BASE_URL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting tab...")
        self.quit()

    def change_currency(self,currency):
        currencybutton = self.find_element(By.CSS_SELECTOR,
            'button[data-modal-aria-label="Select your currency"]'
        )
        currencybutton.click()
        req_currency = self.find_element(By.CSS_SELECTOR,
            'a[data-modal-header-async-url-param*="selected_currency=' + currency + '"]'
        )
        req_currency.click()

    def input_values(self,place,checkin,checkout,children,adults,rooms=1):
        place_field = self.find_element(By.CSS_SELECTOR,
            'input[id="ss"]')
        place_field.clear()
        place_field.send_keys(place)
        self.implicitly_wait(10)
        place_first_suggession = self.find_element(By.CSS_SELECTOR,
            'li[data-i="0"]')
        place_first_suggession.click()
        date_in_element = self.find_element(By.CSS_SELECTOR,f'td[data-date="{checkin}"]')
        date_out_element = self.find_element(By.CSS_SELECTOR,
            f'td[data-date="{checkout}"]')
        date_in_element.click()
        date_out_element.click()
        count_selector = self.find_element(By.CSS_SELECTOR,'label[id="xp__guests__toggle"]')
        count_selector.click()
        rooms_field_plus = self.find_element(By.CSS_SELECTOR,'button[aria-label="Increase number of Rooms"]')
        for i in range(rooms - 1):
            rooms_field_plus.click()
        adults_field_plus = self.find_element(By.CSS_SELECTOR,'button[aria-label="Increase number of Adults"]')
        adults_field_minus = self.find_element(By.CSS_SELECTOR,'button[aria-label="Decrease number of Adults"]')
        adults_field_minus.click()
        for i in range(adults - 1):
            adults_field_plus.click()
        children_field_plus = self.find_element(By.CSS_SELECTOR,'button[aria-label="Increase number of Children"]')
        for i in range(children):
            children_field_plus.click()
            age_field = self.find_element(By.CSS_SELECTOR,f'select[data-group-child-age="{i}"]')
            ageselect = Select(age_field)
            ageselect.select_by_index(5)
            # age_field.click()
            # age_option = self.find_element(By.CSS_SELECTOR,f'option[value="5"]')
            # age_option.click()

    def search(self):
        search_button = self.find_element(By.CSS_SELECTOR,'button[class*="sb-searchbox__button"]')
        search_button.click() 
    
    def low_to_high(self):
        self.find_element(By.XPATH,"//a[text()='Price (lowest first)']").click(); 


    def apply_filtration(self,rating):
        filtration = BookingFiltration(driver=self)
        filtration.star_rating(rating)

    def report_list(self):
        hotel_divs = self.find_element(By.CSS_SELECTOR,'div[id*="ajaxsrwrap"]').find_elements(By.CSS_SELECTOR,'div[class*="fc21746a73"]')
        table = PrettyTable(
            field_names=['Hotel Name','Price','About']        
        )
        for hotel in hotel_divs:
            try:
                name = str(hotel.find_element(By.CSS_SELECTOR,'div[data-testid="title"]').get_attribute('innerHTML')).strip()
                price = str(hotel.find_element(By.CSS_SELECTOR,'span[class="fde444d7ef _e885fdc12"]').get_attribute('innerHTML')).strip()
                about = str(hotel.find_element(By.CSS_SELECTOR,'div[class="_9c5f726ff _192b3a196 f1cbb919ef"]').get_attribute('innerHTML')).strip()
            except:
                continue
            table.add_row([name,price.replace('&nbsp;',' '),about])
        print(table)
           