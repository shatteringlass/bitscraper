from .scrapers import DetailScraper
from .base_scrapers import DividendsScraper
import json

class BITProduct:

    FIELDS = []
    pass


class EnergyFuture(BITProduct):

    def __init__(self, product):
        self._details = DetailScraper(category=3, subcategory=7, prodcode=product).get_details()

    @property
    def details(self):
        return self._details
    

class Stock:
    def __init__(self, ticker):

        with open('bitscraper/mappings/tickers.json', 'r') as f: #fix path
            tickers_dict = json.load(f)

        self._product = DetailScraper(category=1, subcategory=1, prodcode=tickers_dict[ticker]).get_detail_page()


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