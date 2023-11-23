import time
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from utils import form_section_result, form_section_data, write_dic

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

AIRCRAFTS = {
    'Al420': 0,
    'Al440': 1,
    'Br837': 2,
    'Br857': 3,
    'Al420LessSeats': 4,
    'Al420MoreSeats': 5,
    'Al440LessSeats': 6,
    'Al440MoreSeats': 7,
    'Br837LessSeats': 8,
    'Br837MoreSeats': 9,
    'Br857LessSeats': 10,
    'Br857MoreSeats': 11
}
ROUTES = ['A1/B1', 'A1/C1', 'A1/D1']
SELECTIONS = [1, 2, 3]  # section for each round


class Coseplayer():

    def __init__(self):
        self.browser = webdriver.Chrome(options=options)
        self.start_playing()

    def start_playing(self):
        self.browser.get('https://private.lud.io/launch/20demoair')
        self.browser.find_element(By.ID, "read-slide-link").click()
        time.sleep(1)
        self.browser.find_element(By.ID, "read-slide-link").click()
        time.sleep(1)

    def do_fleet_choice(self, data):
        for i, route in enumerate(ROUTES):
            peak = int(data[route + ' Peak'])
            offpeak = int(data[route + ' OffPeak'])
            aircraft = AIRCRAFTS[data[route + ' Aircraft']]

            self.browser.find_element(By.NAME, "highPeriodFrequencyList[" + str(i) + "]").clear()
            self.browser.find_element(By.NAME, "highPeriodFrequencyList[" + str(i) + "]").send_keys(peak)
            self.browser.find_element(By.NAME, "lowPeriodFrequencyList[" + str(i) + "]").clear()
            self.browser.find_element(By.NAME, "lowPeriodFrequencyList[" + str(i) + "]").send_keys(offpeak)
            Select(self.browser.find_element(By.ID, "planeTypeIdList" + str(i))).select_by_index(aircraft)

        self.browser.find_element(By.ID, "validate-fleet-choice-link").click()
        time.sleep(1)
        self.browser.find_element(By.ID, "read-fleet-choice-results-link").click()
        time.sleep(1)

    def do_section(self, prices):
        for i, price in enumerate(prices):
            if self.browser.find_element(By.NAME, "priceList[" + str(i) + "]").get_attribute('type') != 'hidden':
                self.browser.find_element(By.NAME, "priceList[" + str(i) + "]").clear()
                self.browser.find_element(By.NAME, "priceList[" + str(i) + "]").send_keys(int(price))

        self.browser.find_element(By.ID, "validate-price-choice-link").click()
        time.sleep(1)

    def do_round(self, rd, data):
        for section in SELECTIONS:
            prices = form_section_data(data, ROUTES, rd, section, 'Price')
            self.do_section(prices)

            self.browser.find_element(By.ID, "read-price-choice-results-link").click()
            time.sleep(1)

        round_result = {}
        round_result[rd + ' Profit'] = self.browser.find_element(By.XPATH,
                                                                 "//span[contains(@title,'Alpha')]/../../td[3]").text.replace(
            '€', '')
        round_result[rd + ' AveragePrice'] = self.browser.find_element(By.XPATH,
                                                                       "//span[contains(@title,'Alpha')]/../../td[4]").text.replace(
            '€', '')
        round_result[rd + ' Sales'] = self.browser.find_element(By.XPATH,
                                                                "//span[contains(@title,'Alpha')]/../../td[5]").text
        round_result[rd + ' LoadFactor'] = self.browser.find_element(By.XPATH,
                                                                     "//span[contains(@title,'Alpha')]/../../td[7]").text
        print(round_result)
        return round_result

    def save_year_result(self, data, round_result1, round_result2, csv_path):
        year_result = {}
        year_result.update(data.to_dict())
        year_result.update(round_result1)
        year_result.update(round_result2)
        year_result['Year Profit'] = self.browser.find_element(By.XPATH,
                                                               "//span[contains(@title,'Alpha')]/../../td[3]").text.replace(
            '€', '')
        print(year_result)
        write_dic(year_result, csv_path)

    def do_year(self, year, data):
        self.do_fleet_choice(data)
        round_result1 = self.do_round('Round1', data)
        self.browser.find_element(By.ID, "read-round-results-link").click()
        time.sleep(1)
        round_result2 = self.do_round('Round2', data)
        self.browser.find_element(By.ID, "read-round-results-link").click()
        time.sleep(1)
        self.save_year_result(data, round_result1, round_result2, 'result_year' + str(year) + '.csv')

    def run(self, end_year):
        for year in range(1, end_year + 1):
            data = pd.read_csv('data/year' + str(year) + '.csv').iloc[-1]
            self.do_year(year, data)

            if year == end_year:
                return
            self.browser.find_element(By.ID, "read-year-results-link").click()
            time.sleep(1)
            self.browser.find_element(By.ID, "read-slide-link").click()
            time.sleep(1)

    def repeat(self, repeat_year):
        if repeat_year > 1:
            self.run(repeat_year-1)
        self.browser.find_element(By.ID, "read-year-results-link").click()
        time.sleep(1)
        self.browser.find_element(By.ID, "read-slide-link").click()
        time.sleep(1)

        data = pd.read_csv('data/year' + str(repeat_year) + '.csv')
        for _, d in data.iterrows():
            self.do_year(repeat_year, d)

            for i in range(0, 7):
                self.browser.find_element(By.ID, "player-go-back-button").click()
                time.sleep(1)


if __name__ == '__main__':
    coseplayer = Coseplayer()

    # coseplayer.run(4)  # run until the end year
    coseplayer.repeat(2)  # repeat the year

