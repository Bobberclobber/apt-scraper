from abc import ABC


class Scraper(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_scrape_data(self):
        pass
