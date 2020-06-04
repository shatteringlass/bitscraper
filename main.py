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


def test_categorie():
    pass


def test_sottocategorie():
    pass


def test_prodotti():
    pass


def test_derivati():
    p = bs.EnergyFuture().details
    print(json.dumps(p, sort_keys=False, indent=4))


def test_azioni():
    p = bs.StockScraper().get_stock_info('TRIPADVISOR')
    print(json.dumps(p, sort_keys=False, indent=4))


def test_all_stocks():
    p = bs.StockScraper().get_stocks_list()
    print(p)


def main():
    pass


if __name__ == '__main__':
    main()
