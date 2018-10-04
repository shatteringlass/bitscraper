import logging
from product_listings import BITListing
import json

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def main():
    p = BITListing(category="Derivati",
                        subcategory="Futuressuenergiaelettrica").details
    print(json.dumps(p, sort_keys=False, indent=4))


if __name__ == '__main__':
    main()
