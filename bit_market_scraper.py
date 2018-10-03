import logging
import re
from bs4 import Comment, BeautifulSoup as bs
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

    def __init__(self, url='http://borsaitaliana.it/borsa/listino-ufficiale'):
        super(BITScraper, self).__init__(url)
        self.mainpage = self.get_list_page()
        self.avail_categories = self.get_categories()
        self.avail_subcategories = self.get_subcategories()
        self._category = None
        self._subcategory = None

    @property
    def category(self):
        return self._category

    @property
    def subcategory(self):
        return self._subcategory

    @category.setter
    def category(self, category):
        try:
            self._category = self.avail_categories.index(category)
        except ValueError:
            logger.error("Invalid category provided!")
            raise

    @subcategory.setter
    def subcategory(self, subcategory):
        try:
            self._subcategory = self.avail_subcategories[self.category].index(subcategory)+1
        except ValueError:
            logger.error("Invalid subcategory provided!")
            raise

    def get_list_page(self):
        return self.get_page_html(params={'target': 'null', 'service': 'Listino', 'lang': 'it'})

    def get_data_page(self):
        if self.category and self.subcategory:
            html = self.get_page_html(params={'target': 'null', 'service': 'Data', 'lang': 'it', 'main_list': self.category, 'sub_list': self.subcategory})
            return html.find(string=lambda txt: isinstance(txt, Comment) and 'vtable' in txt).next_element
        else:
            logger.error("Not enough parameters provided.")
            raise ValueError

    def get_detail_page(self):
        if self.category and self.subcategory and self.prodcode:
            html = self.get_page_html(params={'target': 'null', 'service': 'Detail', 'lang': 'it', 'main_list': self.category, 'sub_list': self.subcategory, 'extra': self.prodcode})
        else:
            logger.error("Not enough parameters provided.")
            raise ValueError

    def get_categories(self):

        return [
            v.text for v in
            self.mainpage.select("select[name=main_list] option")
        ]

    def get_subcategories(self, category=None):

        idx = None
        if category:
            try:
                idx = self.avail_categories.index(category) + 1
            except ValueError:
                logger.error("Category {} does not exist.".format(category))
                raise

        sc = self.mainpage.find_all('script')[1].text.translate(
            {ord(c): None
             for c in string.whitespace}).split(';')[1:9]
        if idx:
            sc = sc[idx]

        rgx = 'level\d.*Array\((.+)\)'
        r = []

        for x in sc:
            r.append(tuple(map(lambda x: x.replace('\'', ''),
                               re.findall(rgx, x)[0].split(','))))

        return r
