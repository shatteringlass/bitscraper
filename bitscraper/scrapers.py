from .base_scrapers import CategoryScraper
from .base_scrapers import DetailScraper
from .base_scrapers import ListingScraper
from .base_scrapers import ResultsScraper

class StocksScraper:

	def __init__(self, product):
		self._product = DetailScraper(category=1, subcategory=1, prodcode=product).get_detail_page()

	@property
	def product(self):
		return self._product
	