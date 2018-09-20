from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from bs4 import BeautifulSoup
import pickle


class Parser:

    def __init__(self):
        self.url = 'https://laboral.pjud.cl/'
        self.css_selector = '.TESTcpBorder > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > center:nth-child(1)' \
                            ' > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(5)'
        self.data = []
        self.driver = webdriver.Firefox()

    @property
    def selenium_flow(self):
        """Launch browser with the help of selenium and get html with data"""
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
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

    def soup_flow(self)->list:
        """Select data from html and save them in list"""
        soup = BeautifulSoup(self.selenium_flow.get_attribute('innerHTML'), features="html.parser")
        table = soup.find_all('tr', attrs={'class': ['filadostabla', 'filaunotabla']})
        for one in table:
            cols = one.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            self.data.append([ele for ele in cols if ele])
        self.driver.quit()
        return self.data

    @staticmethod
    def save_csv(data):
        """Save data in csv"""
        with open('data.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter='\n',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(data)


if __name__ == '__main__':
    instance = Parser()
    our_data = instance.soup_flow()
    instance.save_csv(our_data)
