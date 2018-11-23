from selenium import webdriver
from scrapers.scraper import Scraper, ROOMS, AREA, RENT, RESERVED, LINK


class WillhemScraper(Scraper):
    def __init__(self):
        super(WillhemScraper, self).__init__()

    def get_hyper_link(self, row_elem):
        for elem in row_elem.find_elements_by_tag_name("td"):
            if elem.get_attribute("data-title") == "Adress":
                return elem.find_element_by_tag_name("a").get_attribute("href")
        return ""

    def get_apt_info(self, text):
        splits = [s for s in text.split("\n") if s]
        address = splits[0].strip().split()
        try:
            street_nr = "%d%s" % (int(address[-2]), address[-1].upper())
            street_name = " ".join(address[:-2]).capitalize()
        except ValueError:
            street_nr = address[-1]
            street_name = " ".join(address[:-1]).capitalize()
        city = " ".join(splits[1].split()[2:]).capitalize()
        apt_spec = {RESERVED: False}
        apt_spec[RENT] = float(splits[3].split()[0])
        size_splits = splits[4].split()
        apt_spec[AREA] = float(size_splits[0].replace(',', '.'))
        apt_spec[ROOMS] = float(size_splits[3].replace(',', '.'))
        return city, street_name, street_nr, apt_spec

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
            for elem in self.driver.find_elements_by_tag_name("tr"):
                try:
                    hyper_link = self.get_hyper_link(elem)
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
