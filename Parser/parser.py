from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from bs4 import BeautifulSoup
from functools import wraps
import logging


def my_logger(orig_funk):
    logging.basicConfig(filename='./logger/logger.log', level=logging.INFO)

    @wraps(orig_funk)
    def wrapper(*args, **kwargs):
        try:
            func = orig_funk(*args, **kwargs)
            logging.info(f'Function: {orig_funk.__name__}, Description: {orig_funk.__doc__}')
            return func
        except Exception as ex:
            logging.error(f"Function: {orig_funk.__name__}, Catched error: {ex}!")
    return wrapper


class Parser:

    def __init__(self):
        self.url = 'https://laboral.pjud.cl/'
        self.css_selector = '.TESTcpBorder > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > center:nth-child(1)' \
                            ' > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(5)'
        self.data = []
        self.driver = webdriver.Firefox()
        """When starting Chrome"""
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # self.driver = webdriver.Chrome(chrome_options=chrome_options)

    @property
    @my_logger
    def selenium_flow(self):
        """Launch browser with the help of selenium and get html with data"""
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        frame = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/frameset/frameset/frame[2]")))
        self.driver.switch_to.frame(frame)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'tdDos'))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="IMG_FEC_Desde"]'))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.css_selector))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/form/table[6]/tbody/tr/td[2]/img'))).click()
        return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/table[8]')))

    @my_logger
    def soup_flow(self)->list:
        """Select data from html and save them in list"""
        soup = BeautifulSoup(self.selenium_flow.get_attribute('innerHTML'), features="html.parser")
        table = soup.find_all('tr', attrs={'class': ['filadostabla', 'filaunotabla']})
        for one in table:
            cols = one.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            self.data.append([ele for ele in cols if ele])
        return self.data

    @staticmethod
    @my_logger
    def save_csv(data):
        """Save data in csv"""
        with open('./data/data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter='\n',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(data)


if __name__ == '__main__':
    try:
        instance = Parser()
        our_data = instance.soup_flow()
        instance.save_csv(our_data)
        if instance.data:
            print('Parsing has been Success!')
        else:
            print('Check the logger!')
    except Exception as ex:
        print(ex)
    finally:
        instance.driver.quit()
