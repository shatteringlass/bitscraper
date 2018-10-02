import logging
import bit_market_scraper as bms

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def main():
    b = bms.BITScraper(url='http://borsaitaliana.it/borsa/listino-ufficiale')
    cat,subc = "Derivati", "Futuressuenergiaelettrica"


if __name__ == '__main__':
    main()
