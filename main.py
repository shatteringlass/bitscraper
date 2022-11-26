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


def test_bitscraper():
    p = bs.BITScraper()
    cat = p.avail_categories
    scat = p.avail_subcategories
    return cat, scat


def test_bitlisting(category, subcategory):
    p = bs.BITListing(category=category,
                        subcategory=subcategory).details
    with open(f"./tests/BIT_{category}_{subcategory}.json", 'w') as fp:
        json.dump(obj=p, fp=fp, sort_keys=False, indent=4)

def main():
    # cat, scat=test_bitscraper()
    # for i,c in enumerate(cat):
    #     for sc in scat[i]:
    #         print(c,sc)
    #         test_bitlisting(c, sc)
    test_bitlisting(category="Derivati", subcategory="Futuressuenergiaelettrica")

if __name__ == '__main__':
    main()
