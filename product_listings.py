import bit_market_scraper as bms


class ProductListing(object):

    def __init__(self, listing=None):
        self.listing = listing


class BITListing(ProductListing):

    def __init__(self, category=None, subcategory=None):
        super(BITListing, self).__init__(listing=self.scrape_list())
        self.category = category
        self.subcategory = subcategory

    def scrape_list(self, category="Derivati", subcategory="Futuressuenergiaelettrica"):
    	b = bms.BITScraper()
    	return tuple(map(lambda x: b.get_detail_page(category,subcategory,x), b.get_data_page(category,subcategory)))


class IDEMListing(BITListing):
    pass
