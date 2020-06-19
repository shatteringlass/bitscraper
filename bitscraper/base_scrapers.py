import logging
import re
import requests
import string
import urllib.parse as urlparse

from bs4 import BeautifulSoup as bs
from urllib.parse import parse_qs

from .misc import Category, Subcategory

logger = logging.getLogger()


class SiteScraper(object):
    def __init__(self, url, params):
        self.baseurl = url
        self.params = params
        self._html = self.get_page_html()

    @property
    def html(self):
        return self._html

    def get_page_html(self):
        response = requests.get(self.baseurl, self.params)
        response.encoding = 'utf8'
        return bs(response.text, 'html.parser')


class BITScraper(SiteScraper):

    def __init__(self, params):
        super(BITScraper, self).__init__(
            url='https://borsaitaliana.it/borsa/listino-ufficiale', params=params)


class CategoryScraper(BITScraper):

    def __init__(self):
        params = {'service': 'Listino', }
        super(CategoryScraper, self).__init__(params=params)
        self._categories = self._get_categories()

    @property
    def categories(self):
        return self._categories

    def _get_subcategories(self):

        sc = self.html.find_all('script')[1].get_text()
        rgx = 'level\d.*Array\((.+)\);'
        return [[Subcategory(number=idx+1, name=z) for idx, z in enumerate(
            x.replace("'", "").split(','))] for x in re.findall(rgx, sc)]

    def _get_categories(self):
        c = self.html.select("select[name=main_list] option")
        sc = self._get_subcategories()
        for i in range(len(c)-len(sc)):
            sc.append(None)

        return [
            Category(
                number=idx,
                name=v.text.strip(),
                subcategories=sc[idx]) for idx, v in enumerate(c)
        ]


class ListingScraper(BITScraper):

    def __init__(self, service, category, subcategory, letter):
        params = {
            'service': service,
            'main_list': category,
            'sub_list': subcategory,
            'search': 'al',
            'letter': letter
        }
        super(ListingScraper, self).__init__(params=params)
        self._extras = self.get_extras(letter=letter)

    @property
    def extras(self):
        return self._extras

    def get_extras(self, letter):
        def get_extra(x): return parse_qs(
            urlparse.urlparse(x).query)['extra'][0]
        extras = dict()
        try:
            links = self.html.find(
                'table', attrs={'bordercolordark': '#ffffff'}).find_all('a')
            for l in links:
                extras[l.text] = get_extra(l.get('href'))
        finally:
            return extras


class DataScraper(ListingScraper):

    def __init__(self, category, subcategory):
        super(DataScraper, self).__init__(service='Data',
                                             category=category, 
                                             subcategory=subcategory, 
                                             letter=None)


class ResultsScraper(ListingScraper):

    def __init__(self, category, subcategory, letter):
        super(ResultsScraper, self).__init__(service='Results',
                                             category=category, 
                                             subcategory=subcategory, 
                                             letter=letter)


class DetailScraper(BITScraper):

    def __init__(self, category, subcategory, prodcode):
        params = {
            'service': 'Detail',
            'main_list': category,
            'sub_list': subcategory,
            'extra': prodcode
        }
        super(DetailScraper, self).__init__(params=params)

    def get_detail_page(self):
        table = self.html.find('table', attrs={'bordercolordark': '#ffffff'})
        product = dict()
        for row in table.find_all('tr')[2:]:
            k, v = tuple(map(lambda x: x.text, row.find_all('td')))
            product[k.translate(
                {ord(c): '_' for c in string.whitespace}).lower()] = v.strip().translate(
                {ord(c): None for c in string.whitespace})
        return product
