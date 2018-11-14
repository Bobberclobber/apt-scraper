from selenium import webdriver
from abc import ABC, abstractmethod


class Scraper(ABC):
    def __init__(self):
        # Run Chrome silently
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        # TODO: Make sure that creating the driver object here works when the program is running for a long time
        self.driver = webdriver.Chrome(chrome_options=options)

    @abstractmethod
    def get_scrape_data(self):
        pass

    @abstractmethod
    def close(self):
        pass
