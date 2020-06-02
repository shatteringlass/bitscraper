from .bit_market_scraper import BITScraper


class ProductListing(object):

    def __init__(self, *args, scraper=None, **kwargs):
        self._scraper = scraper
        self._products = scraper.get_products(*args, **kwargs)
        self._details = scraper.get_details(*args, products=self.products, **kwargs)

    @property
    def scraper(self):
        return self._scraper

    @property
    def products(self):
        return self._products

    @property
    def details(self):
        return self._details


class BITListing(ProductListing):

    def __init__(self, scraper=BITScraper(), category=None, subcategory=None):
        super(BITListing, self).__init__(scraper=BITScraper(),
                                         category=category, subcategory=subcategory)
        self._category = category
        self._subcategory = subcategory

    @property
    def category(self):
        return self._category

    @property
    def subcategory(self):
        return self._subcategory

    @property
    def available_categories(self):
        return self.scraper.avail_categories

    @property
    def available_subcategories(self):
        return self.scraper.avail_subcategories


class IDEMListing(BITListing):
    pass
