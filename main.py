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
    b = bms.BITScraper()
    cat,subc = "Derivati", "Futuressuenergiaelettrica"
    b.category, b.subcategory = cat, subc
    print(b.get_data_page() )


if __name__ == '__main__':
    main()
