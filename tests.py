#!/usr/bin/env python3

import bitscraper as bs
import json

def test_categorie():
    cs = bs.CategoryScraper()
    print(cs.categories)

def test_data():
    ds = bs.DataScraper(category=3, subcategory=1)
    print(ds.extras)

def test_results():
    results = dict()
    for l in list(chr(x) for x in range(65, 90+1)):
        results = {**results, **bs.ResultsScraper(category=1, subcategory=1, letter=l).extras}
    print(json.dumps(results, indent=4))

def test_azione(extra=180595):
    p = bs.StocksScraper(product=extra).product
    print(json.dumps(p, indent=4))

def test_stock(extra='ENEL'):
    s = bs.Stock(extra)
    print(s)

def test_dividends_calendar():
    c = bs.Calendar(type='dividends')
    print(c.result)

def test_events_calendar():
    c = bs.Calendar(type='events')
    print(c.result)


def test_derivati():
    pass


def test_all_stocks():
    pass


def test_all():
    # test_categorie() #OK
    # test_data() #OK
    # test_results() #OK
    # test_prodotti()
    # test_derivati()
    # test_azioni()
    # test_all_stocks()
    # test_azione()
    # test_stock()
    test_dividends_calendar()
    test_events_calendar()


if __name__ == '__main__':
    test_all()
