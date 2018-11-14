from selenium import webdriver
from scrapers.scraper import Scraper


class WillhemScraper(Scraper):
    def __init__(self):
        super(WillhemScraper, self).__init__()

    def get_apt_info(self, row_elem):
        for elem in row_elem.find_elements_by_tag_name("td"):
            data_title = elem.get_attribute("data-title")
            city = ""
            street_name = ""
            street_nr = ""
            apt_spec = {"reserved": False}
            hyper_link = ""
            if data_title == "Adress":
                city, street_name, street_nr = self.get_address(elem.text)
                hyper_link = self.get_hyper_link(elem)
            elif data_title == "Hyra":
                apt_spec["rent"] = 0
            elif data_title == "Yta, antal rum":
                apt_spec["area"] = 0
                apt_spec["rooms"] = 0
            return city, street_name, street_nr, apt_spec, hyper_link

    def get_scrape_data(self):
        scrape_data = {}
        errors = []
        self.driver.get("https://willhem.se/sok-bostad/")
        city_urls = {}
        for elem in self.driver.find_elements_by_tag_name("a"):
            city_href = elem.get_attribute("href")
            if not city_href or "link/" not in city_href or elem.text == "Startsida":
                continue
            city = elem.text.strip()
            city_url = "https://willhem.se/sok-bostad/%s" % city
            city_url = city_url.replace('å', 'a').replace('ä', 'a').replace('ö', 'o')
            city_urls[city] = city_url
        for city, city_url in city_urls.items():
            self.driver.get(city_url)
            for elem in self.driver.find_elements_by_tag_name("tr")[:5]:
                self.get_apt_info(elem)
                print(elem.text)
                print('---')
        return scrape_data, errors
