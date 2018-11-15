#!./venv/bin/python

import sys
import inspect
import importlib

from os import listdir
from os.path import isfile, join


from scrapers.willhem_scraper import WillhemScraper
from scrapers.homeq_scraper import HomeqScraper


SCRAPERS_DIR = "scrapers"


if __name__ == "__main__":
    # Automatically import and instantiate all scrapers
    #scraper_files = [f for f in listdir(SCRAPERS_DIR) if isfile(join(SCRAPERS_DIR, f)) and f.endswith('_scraper.py')]
    #scrapers = []
    #for sf in scraper_files:
    #    module_path = "%s.%s" % (SCRAPERS_DIR, sf[:-3])
    #    importlib.import_module(module_path)
    #    cls = [c for c in inspect.getmembers(sys.modules[module_path], inspect.isclass) if c[0] != 'Scraper'][0]
    #    scrapers.append(cls[1]())
    #for s in scrapers:
    #    s.get_scrape_data()
    #    s.close()
    s = WillhemScraper()
    s.get_scrape_data()
    s.close()
