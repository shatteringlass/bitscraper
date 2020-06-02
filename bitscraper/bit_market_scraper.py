import re
import string
import logging
import requests
from bs4 import BeautifulSoup as bs

logger = logging.getLogger()
"""
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
"""


class SiteScraper(object):
    def __init__(self, url):
        self.baseurl = url
        self.page = None

    def get_page_html(self, params):
        response = requests.get(self.baseurl, params)
        self.page = bs(response.text, 'html.parser')
        return self.page


class ProductScraper(SiteScraper):

    def get_products(self, *args, **kwargs):
        pass

    def get_details(self, *args, **kwargs):
        pass


class BITScraper(ProductScraper):

    def __init__(self, url='https://borsaitaliana.it/borsa/listino-ufficiale'):
        super(BITScraper, self).__init__(url)
        self.mainpage = self.get_list_page()
        self.date = self.mainpage.font.text[-10:].strip()
        self._avail_categories = self.get_categories()
        self._avail_subcategories = self.get_subcategories()

    @property
    def avail_categories(self):
        return self._avail_categories

    @property
    def avail_subcategories(self):
        return self._avail_subcategories

    def get_list_page(self):
        return self.get_page_html(params={'target': 'null', 'service': 'Listino', 'lang': 'it'})

    def get_data_page(self, category, subcategory):
        if category and subcategory:
            c = self.avail_categories.index(category)
            s = self.avail_subcategories[c].index(subcategory) + 1
            logger.debug(
                "Now retrieving products for category: {} - subcategory {}".format(category, subcategory))
            table = self.get_page_html(params={'target': 'null', 'service': 'Data', 'lang': 'it',
                                               'main_list': c, 'sub_list': s}).select('center table:nth-of-type(2) tr a')
            return tuple(map(lambda x: x.get('href').split('=')[-1], table))
        else:
            logger.error("Not enough parameters provided.")
            raise ValueError

    def get_detail_page(self, category, subcategory, prodcode):
        if category and subcategory and prodcode:
            c = self.avail_categories.index(category)
            s = self.avail_subcategories[c].index(subcategory) + 1
            logger.debug(
                "Now retrieving info for product {} in category: {} - subcategory {}".format(prodcode, category, subcategory))
            table = self.get_page_html(params={'target': 'null', 'service': 'Detail', 'lang': 'it',
                                               'main_list': c, 'sub_list': s, 'extra': prodcode}).select('table:nth-of-type(6)')[0]
            product = {'data_listino': self.date}
            for row in table.find_all('tr')[2:]:
                k, v = tuple(map(lambda x: x.text, row.find_all('td')))
                product[k.translate(
                    {ord(c): '_' for c in string.whitespace}).lower()] = v
            return product
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
                idx = self.avail_categories.index(category)
            except ValueError:
                logger.error("Category {} does not exist.".format(category))
                raise

        sc = self.mainpage.find_all('script')[1].text.translate(
            {ord(c): None
             for c in string.whitespace}).split(';')[1:9]
        if idx:
            sc = [sc[idx]]

        rgx = 'level\d.*Array\((.+)\)'
        r = []

        for x in sc:
            r.append(tuple(map(lambda x: x.replace('\'', ''),
                               re.findall(rgx, x)[0].split(','))))

        return r

    def get_products(self, *args, **kwargs):
        category = kwargs.get('category')
        subcategory = kwargs.get('subcategory')
        return self.get_data_page(category=category, subcategory=subcategory)

    def get_details(self, *args, **kwargs):
        category = kwargs.get('category')
        subcategory = kwargs.get('subcategory')
        products = kwargs.get('products')
        return tuple(map(lambda prod: self.get_detail_page(category=category, subcategory=subcategory, prodcode=prod), products))
