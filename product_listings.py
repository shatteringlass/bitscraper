import financial_products as fp


class ProductListing(object):

    def __init__(self, listing=None):
        self.listing = listing


class BITListing(ProductListing):

    def __init__(self, category=None, subcategory=None):
        super(BITListing, self).__init__()
        self.category = category
        self.subcategory = subcategory

class IDEMListing(BITListing):
    pass
