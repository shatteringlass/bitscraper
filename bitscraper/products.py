from .scrapers import DetailScraper
from .base_scrapers import DividendsScraper
from .base_scrapers import CalendarScraper
from .base_scrapers import RatingScraper
import json
from datetime import date


class BITProduct:

    FIELDS = []
    pass


class EnergyFuture(BITProduct):

    def __init__(self, product):
        self._details = DetailScraper(
            category=3, subcategory=7, prodcode=product).get_details()

    @property
    def details(self):
        return self._details


class Stock:
    def __init__(self, ticker):

        with open('bitscraper/mappings/tickers.json', 'r') as f:  # fix path
            tickers_dict = json.load(f)

        self._product = DetailScraper(
            category=1, subcategory=1, prodcode=tickers_dict[ticker]).get_detail_page()

    @property
    def product(self):
        return self._product

    @property
    def name(self):
        return self._product['denominazione']

    @property
    def isin(self):
        return self._product['codice_isin']

    @property
    def min_price(self):
        return float(self._product['prezzo_minimo'])

    @property
    def min_price_amount(self):
        return float(self._product['quantità_prezzo_minimo'].replace(" ", ""))

    @property
    def max_price(self):
        return float(self._product['prezzo_massimo'])

    @property
    def max_price_amount(self):
        return float(self._product['quantità_prezzo_massimo'])

    @property
    def price(self):
        return float(self._product['prezzo_ufficiale'])

    @property
    def last_change(self):
        return float(self._product['var._%'])

    @property
    def shares(self):
        return float(self._product['numero_di_azioni'].replace(" ", ""))

    @property
    def market_cap(self):
        return self.shares * self.price

    @property
    def dividends(self):
        return DividendsScraper(isin=self.isin).get_dividends()

    @property
    def rating(self):
        return RatingScraper(isin=self.isin).get_ratings()

    def __str__(self):
        attrs = ["name",
                 "min_price",
                 "min_price_amount",
                 "max_price",
                 "max_price_amount",
                 "price",
                 "last_change",
                 "shares",
                 "market_cap",
                 "dividends",
                 "rating"]
        return "\n".join([f"{a}: {self.__getattribute__(a)}" for a in attrs])


class Calendar:
    def __init__(self, type='dividends', date_from=date.today(), date_to=''):

        if date_to == '':
            split_date = str(date_from).split('-')
            next_year = int(str(date.today()).split('-')[0]) + 1
            date_to = str(next_year) + '-' + split_date[1] + '-' + split_date[2]

        self._result = CalendarScraper(
            type=type, date_from=date_from, date_to=date_to).get_list()

    @property
    def result(self):
        return self._result
