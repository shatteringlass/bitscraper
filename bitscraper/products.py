from .scrapers import DetailScraper


class BITProduct:

    FIELDS = []
    pass


class EnergyFuture(BITProduct):

    def __init__(self, product):
        self._details = DetailScraper(category=3, subcategory=7, prodcode=product).get_details()

    @property
    def details(self):
        return self._details
    

class Stock(BITProduct):
    pass
