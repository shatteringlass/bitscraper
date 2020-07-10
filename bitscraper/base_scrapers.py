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


class BITDividendsScraper(SiteScraper):

    def __init__(self, params):
        super(BITDividendsScraper, self).__init__(
            url='https://borsaitaliana.it/borsa/quotazioni/azioni/elenco-completo-dividendi.html', params=params)

class BITCalendarScraper(SiteScraper):

    def __init__(self, params):

        if params['type'] == 'events':
            url = 'https://www.borsaitaliana.it/borsa/documents/events.html'
        if params['type'] == 'dividends':
            url = 'https://www.borsaitaliana.it/borsa/documents/dividends-mini.html'

        super(BITCalendarScraper, self).__init__(
            url=url, params=params)

class BITRatingScraper(SiteScraper):

    def __init__(self, params):
        super(BITRatingScraper, self).__init__(
            url='https://www.borsaitaliana.it/borsa/quotazioni/azioni/rating.html', params=params)

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


class DividendsScraper(BITDividendsScraper):

    def __init__(self, isin):
        params = {
            'isin': isin,
            'lang': 'it',
            'page': 1,
        }
        super(DividendsScraper, self).__init__(params=params)

    def get_dividends(self):
        table = self.html.find('table', {'class': 'm-table -responsive -list -clear-m'})

        thead = self.html.find('tr', {'class': '-xs -list'})

        columns = []
        for row in thead.find_all('th'):
            v = row.text
            columns.append(v.strip().replace(" ", "_").lower())

        dividends = dict()
        for row in table.find_all('tr', {'class' : '-list'})[1:]:
            stock_type, div_board, div_sh_meeting, currency, date, pay_date, sh_meeting_date, avviso = tuple(map(lambda x: x.text, row.find_all('td')))
            year = "20" + date.split("/")[2]

            if year in dividends:
                dividends[year] = dividends[year] + float(div_board.replace(',','.'))
            else:
                dividends[year] = float(div_board.replace(',','.'))
        return dividends

class RatingScraper(BITRatingScraper):

    def __init__(self, isin):
        params = {
            'isin': isin,
            'lang': 'it',
        }
        super(RatingScraper, self).__init__(params=params)

    def get_ratings(self):
        table = self.html.find('table', {'class': 'm-table -responsive -list -clear-m'})

        thead = self.html.find('tr', {'class': '-xs -list'})

        columns = []
        for row in thead.find_all('th'):
            v = row.text
            columns.append(v.strip().replace(" ", "_").lower())

        ratings = []
        for row in table.find_all('tr', {'class' : '-list'})[1:]:
            
            rating = {}
            isin, name, rating_type, rating_value, credit_watch, rating_outlook, rating_agency, rating_date, avviso_date, avviso = tuple(map(lambda x: x.text, row.find_all('td')))

            rating['type'] = rating_type
            rating['value'] = rating_value
            rating['outlook'] = rating_outlook
            rating['agency'] = rating_agency
            rating['date'] = rating_date

            ratings.append(rating)

        return ratings


class CalendarScraper(BITCalendarScraper):

    def __init__(self, type, dateFrom, dateTo):

        self._type = type

        params = {
            'type': type,
            'dateFrom': dateFrom,
            'dateTo': dateTo,
            'page': 1,
            'lang': 'it',
            'size': 500
        }
        super(CalendarScraper, self).__init__(params=params)

    def get_list(self):
        table = self.html.find('table', {'class': 'm-table -firstlevel'})

        stocks = [x.text.strip('\n') for x in table.find_all('div', {'class': 'l-box -pb | l-screen -xs-15'})]
        if self._type == 'dividends':
            dates = [x.text.strip('\n') for x in  table.find_all('div', {'class': 'l-box | l-screen -xs-9'})]
        if self._type == 'events':
            dates = [x.text.strip('\n') for x in  table.find_all('div', {'class': 'l-box | l-screen -xs-11'})]

        return list(zip(dates,stocks))