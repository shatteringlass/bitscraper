import logging
import bitscraper as bs
import json

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def test_derivati():
    p = bs.BITListing(category="Derivati",
                        subcategory="Futuressuenergiaelettrica").details
    print(json.dumps(p, sort_keys=False, indent=4))

def test_azioni():
    p = bs.StockScraper().get_stock_info('TRIPADVISOR')
    print(json.dumps(p, sort_keys=False, indent=4))

def main():
	test_azioni()

if __name__ == '__main__':
    main()
