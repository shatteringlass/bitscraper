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

    def get_page(self, service, category, subcategory, extra=None):
        params = {'target': 'null', 'service': 'Listino', 'lang': 'it'}
        params['main_list'] = self.get_categories().index(category)
        params['sub_list'] = self.get_subcategories()

        if service == 'Detail':
            params['service'] = service
            params['extra'] = extra

        return self.get_page_html(params)

    def get_categories(self):

        params = {'target': 'null', 'service': 'Listino', 'lang': 'it'}
        return [
            v.text for v in
            self.get_page_html(params).select("select[name=main_list] option")
        ]

    def get_subcategories(self, category=None):

        params = {'target': 'null', 'service': 'Listino', 'lang': 'it'}

        if category:
            try:
                idx = self.get_categories().index(category) + 1
            except ValueError:
                logger.error("Category {} does not exist.".format(category))
                raise

        ctg = self.get_page_html(params).find_all('script')[1].text.translate(
            {ord(c): None
             for c in string.whitespace}).split(';')[idx]
        rgx = 'level\d.*Array\((.+)\)'

        return tuple(
            map(lambda x: x.replace('\'', ''),
                re.findall(rgx, ctg)[0].split(',')))
