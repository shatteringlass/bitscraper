class Category:

    def __init__(self, number, name, subcategories=None):
        self.number = number
        self.name = name
        self.subcategories = subcategories

    def __str__(self):
        return "Category(number={},name=\"{}\",subcategories={})".format(self.number, self.name, self.subcategories)

    def __repr__(self):
        return self.__str__()

class Subcategory(Category):
    pass
    
    def __str__(self):
        return "Subcategory(number={},name=\"{}\")".format(self.number, self.name)