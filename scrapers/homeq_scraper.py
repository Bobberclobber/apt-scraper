from selenium import webdriver
from scrapers.scraper import Scraper, ROOMS, AREA, RENT, RESERVED, LINK


class HomeqScraper(Scraper):
    def __init__(self):
        super(HomeqScraper, self).__init__()

    def get_apt_info(self, text):
        reserved = False
        splits = [s for s in text.split("\n") if s]
        if splits[0] == "Reserverad":
            reserved = True
            splits = splits[1:]
        address = splits[0].strip().split()
        street_name = " ".join(address[:-1]).capitalize()
        street_nr = address[-1].upper()
        city = splits[1].strip().capitalize()
        apt_spec_list = splits[2].strip().split()
        apt_spec = {RESERVED: reserved}
        apt_spec[ROOMS] = float(apt_spec_list[0])
        apt_spec[AREA] = float(apt_spec_list[2])
        apt_spec[RENT] = float(apt_spec_list[4])
        return city, street_name, street_nr, apt_spec

    def get_scrape_data(self):
        scrape_data = {}
        errors = []
        self.driver.get("https://www.homeq.se/search")
        for elem in self.driver.find_elements_by_tag_name("a"):
            hyper_link = elem.get_attribute("href")
            if not hyper_link or "object" not in hyper_link:
                continue
            try:
                city, street_name, street_nr, apt_spec = self.get_apt_info(elem.text)
                if city not in scrape_data:
                    scrape_data[city] = {}
                if street_name not in scrape_data[city]:
                    scrape_data[city][street_name] = {}
                scrape_data[city][street_name][street_nr] = apt_spec
                scrape_data[city][street_name][street_nr][LINK] = hyper_link
            except:
                if elem.text:
                    errors.append(elem.text)
        return scrape_data, errors
