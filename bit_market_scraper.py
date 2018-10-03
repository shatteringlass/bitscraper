import logging
import re
from bs4 import BeautifulSoup as bs
import requests
import string
import product_listings as fp

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class SiteScraper(object):
    def __init__(self, url):
        self.baseurl = url
        self.page = None

    def get_page_html(self, params):
        response = requests.get(self.baseurl, params)
        self.page = bs(response.text, 'html.parser')
        return self.page


class BITScraper(SiteScraper):

    def __init__(self):
        super(SiteScraper, self).__init__(
            url='http://borsaitaliana.it/borsa/listino-ufficiale')
        self.mainpage = self.get_list_page()
        self.avail_categories = self.get_categories()
        self.avail_subcategories = self.get_categories()

    @property
    def category(self):
        return self._category

    @property
    def subcategory(self):
        return self._subcategory

    @category.setter
    def category(self, category):
        pass

    @subcategory.setter
    def subcategory(self, subcategory):
        pass

    def get_list_page(self):
        return self.get_page_html(params={'target': 'null', 'service': 'Listino', 'lang': 'it'})

    def get_data_page():
        if category and subcategory:
            return self.get_page_html(params={'target': 'null', 'service': 'Data', 'lang': 'it', 'main_list': category, 'sub_list': subcategory})
        else:
            logger.error("Not enough parameters provided.")
            raise ValueError

    def get_detail_page():
        if category and subcategory and prodcode:
            return self.get_page_html(params={'target': 'null', 'service': 'Detail', 'lang': 'it', 'main_list': category, 'sub_list': subcategory, 'extra': prodcode})
        else:
            logger.error("Not enough parameters provided.")
            raise ValueError

    def get_categories(self):

        return [
            v.text for v in
            self.mainpage.select("select[name=main_list] option")
        ]

    def get_subcategories(self, category=None):

        if category:
            try:
                idx = self.avail_categories.index(category) + 1
            except ValueError:
                logger.error("Category {} does not exist.".format(category))
                raise

        sc = self.mainpage.find_all('script')[1].text.translate(
            {ord(c): None
             for c in string.whitespace}).split(';')
        if idx:
            sc = sc[idx]

        rgx = 'level\d.*Array\((.+)\)'

        return tuple(
            map(lambda x: x.replace('\'', ''),
                re.findall(rgx, sc)[0].split(',')))
