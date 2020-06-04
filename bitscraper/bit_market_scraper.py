import re
import string
import logging
import requests
from bs4 import BeautifulSoup as bs
import urllib.parse as urlparse
from urllib.parse import parse_qs

logger = logging.getLogger()

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
                                               'main_list': c, 'sub_list': s}).find('table', attrs={'bordercolordark': '#ffffff'}).find_all('tr')[1:]
            items = []
            for tr in table:
                items.append(tr.find_all('td')[0].find('a'))
            return tuple(map(lambda x: x.get('href').split('=')[-1], items))
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
                                               'main_list': c, 'sub_list': s, 'extra': prodcode}).find('table', attrs={'bordercolordark': '#ffffff'})
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


class StockScraper(ProductScraper):

    # TODO: refactoring

    def __init__(self):
        url = 'https://borsaitaliana.it/borsa/listino-ufficiale'
        super(StockScraper, self).__init__(url)
        letters = list(chr(x) for x in range(65,90+1))
        self._stocks = dict()
        for l in letters:
            pg = self.get_stocks_page(letter=l)
            self._stocks = {**self._stocks, **pg}

    @property
    def stocks(self):
        return self._stocks
    

    @staticmethod
    def get_extra(link):
        return parse_qs(urlparse.urlparse(link).query)['extra'][0]

    def get_stocks_page(self, letter):
        stocks = dict()
        html = self.get_page_html(params={
            'target': 'null',
            'service': 'Results',
            'lang': 'it',
            'main_list': 1,
            'sub_list': 1,
            'search': 'al',
            'letter': letter
        })
        try:
            links = html.find('table', attrs={'bordercolordark': '#ffffff'}).find_all('a')
            for l in links:
                stocks[l.text] = StockScraper.get_extra(l.get('href'))
        finally:
            return stocks
        
    def get_stocks_list(self):
        return list(self.stocks.keys())

    def get_stock_info(self, name):
        letter = name[0].upper()
        extra = self.stocks.get(name)
        html = self.get_page_html(params={
            'target':'null',
            'lang':'it',
            'service':'Detail',
            'from':'search',
            'main_list':1,
            'sub_list':1,
            'letter':letter,
            'search':'al',
            'extra':extra,
            'emittenti':'',
            })
        table = html.find('table', attrs={'bordercolordark': '#ffffff'}).find_all('tr')[2:]
        product = dict()
        for row in table:#.find_all('tr')[2:]:
            k, v = tuple(map(lambda x: x.text, row.find_all('td')))
            product[k.translate(
                {ord(c): '_' for c in string.whitespace}).lower()] = v
        return product