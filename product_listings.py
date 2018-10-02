import financial_products as fp

class ProductListing(object):
    pass

class BITListing(ProductListing):
    pass

class IDEMListing(BITListing):

    def __init__(self):
        pass


    @property
    def category(self):
        return self._category

    @property
    def subcategory(self):
        return self._subcategory

    @category.setter
    def category(self, category):
        self._category = (self.get_categories().index(category), category)

    @subcategory.setter
    def subcategory(self, subcategory):
        self._subcategory = (self.get_subcategories(
            self.category[0]).index(subcategory), subcategory)


    def get_products(self):
        """Return the table of the products available on the specific segment"""
        self.params['service'] = 'Data'
        self.params['main_list'] = self.category
        self.params['sub_list'] = self.subcategory + 1

        pass

    def get_dettagli_prodotto(self):
        """Return the details relative to a specific product"""
        pass

    def get_listino_completo(baseurl):
        """Return the details relative to all products in a specific segment"""
        pass
