import logging
import re
import requests
import string
import urllib.parse as urlparse

from bs4 import BeautifulSoup as bs
from urllib.parse import parse_qs

logger = logging.getLogger()


class SiteScraper(object):
    def __init__(self, url, params):
        self.baseurl = url
        self.params = params

    def get_page_html(self):
        response = requests.get(self.baseurl, self.params)
        return bs(response.text, 'html.parser')


class BITScraper(SiteScraper):

    def __init__(self, params):
        super(BITScraper, self).__init__(
            url='https://borsaitaliana.it/borsa/listino-ufficiale', params=params)


class CategoryScraper(BITScraper):

    def __init__(self):
        super(CategoryScraper, self).__init__(params={'service': 'Listino', })
        #self._avail_categories = self.get_categories()
        #self._avail_subcategories = self.get_subcategories()

    @property
    def avail_categories(self):
        return self._avail_categories

    @property
    def avail_subcategories(self):
        return self._avail_subcategories

    def get_list_page(self):
        return self.get_page_html()

    def get_categories(self):

        return [
            v.text for v in
            self.get_list_page().select("select[name=main_list] option")
        ]

    def get_subcategories(self, category):

        sc = self.get_list_page().find_all('script')[1].translate(
            {ord(c): ' ' for c in string.whitespace}).split(';')[category+1]
        print(sc)
        rgx = 'level\d.*Array\((.+)\)'
        scat = dict()
        for icat, cat in enumerate(re.findall(rgx, x)[0].split(',')):
            scat[icat] = cat.replace('\'', '')
        return scat


class ListingScraper(BITScraper):

    def __init__(self, category, subcategory):
        super(ListingScraper, self).__init__(params={
            'service': 'Data',  'main_list': category, 'sub_list': subcategory})
        self._extras = self.get_extra()

    @property
    def extras(self):
        return self._extras

    def get_extra(self):
        try:
            html = self.get_page_html()
            table = html.find('table', attrs={'bordercolordark': '#ffffff'})
            rows = table.find_all('tr')[1:]
            items = [tr.find_all('td')[0].find('a') for tr in rows]
        except AttributeError:
            return tuple()
        else:
            return tuple(map(lambda x: x.get('href').split('=')[-1], items))


class DetailScraper(BITScraper):

    def __init__(self, category, subcategory, prodcode):
        super(ProductScraper, self).__init__()
        self._category = category
        self._subcategory = subcategory
        self._prodcode = prodcode
        params = {
            'target': 'null',
            'service': 'Detail',
            'lang': 'it',
            'main_list': self.category,
            'sub_list': self.subcategory,
            'extra': self.prodcode
        }

    @property
    def category(self):
        return self._category

    @property
    def subcategory(self):
        return self._subcategory

    @property
    def prodcode(self):
        return self._prodcode

    def get_detail_page(self, category, subcategory, prodcode):
        logger.debug(
            "Now retrieving info for product {} in category: {} - subcategory {}".format(self.prodcode, self.category, self.subcategory))
        html = self.get_page_html()
        table = html.find('table', attrs={'bordercolordark': '#ffffff'})
        product = {'data_listino': self.date}
        for row in table.find_all('tr')[2:]:
            k, v = tuple(map(lambda x: x.text, row.find_all('td')))
            product[k.translate(
                {ord(c): '_' for c in string.whitespace}).lower()] = v
        return product


class ResultsScraper(BITScraper):

    def __init__(self):
        super(ResultsScraper, self).__init__(url)
        letters = list(chr(x) for x in range(65, 90+1))
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
            links = html.find(
                'table', attrs={'bordercolordark': '#ffffff'}).find_all('a')
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
            'target': 'null',
            'lang': 'it',
            'service': 'Detail',
            'from': 'search',
            'main_list': 1,
            'sub_list': 1,
            'letter': letter,
            'search': 'al',
            'extra': extra,
            'emittenti': '',
        })
        table = html.find(
            'table', attrs={'bordercolordark': '#ffffff'}).find_all('tr')[2:]
        product = dict()
        for row in table:
            k, v = tuple(map(lambda x: x.text, row.find_all('td')))
            product[k.translate(
                {ord(c): '_' for c in string.whitespace}).lower()] = v
        return product
