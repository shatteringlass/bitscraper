import financial_products as fp


class ProductListing(object):

    def __init__(self, listing=None):
        self.listing = listing


class BITListing(ProductListing):

    def __init__(self, *args, **kwargs, category=None, subcategory=None):
        super(ProductListing, self).__init__(*args, **kwargs)
        self.category = category
        self.subcategory = subcategory

class IDEMListing(BITListing):
    pass
