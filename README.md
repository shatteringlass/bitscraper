# Borsa Italiana Official List - python scraper

An object-oriented scraper for the Official List of products traded on Borsa Italiana (Italian Exchange).
Whenever available, the scraper provides full detail for each product.
The products are organized by category first, and then by subcategory.

This is the product hierarchy as of today, October 3rd 2018:

- Indici
    - Indici Generali
    - Indici Settoriali
    - Indici Tah
- Azionario
    - Tutte le azioni
	- Azioni MIB30
	- Azioni Midex
	- Azioni FTSE/MIB
	- Blue Chip
	- Standard 1
	- Standard 2
	- Mercato Expandi
	- Warrant
	- Obbligazioni Convertibili
	- Obbligazioni Convertibili Expandi
	- Diritti
	- Diritti Expandi
	- MTF3
	- MTF4
	- MTA International
	- MIV-InvCompanies
	- MIV-REIC
	- MIV-Unit
	- SIV-Segmento Professionale
	- Segmento STAR
- Securitised Derivatives
    - CW e Certificates
	- Ricerca
- Derivati
    - Futures su indici
	- Futures su azioni
	- Minifutures su indici
	- Opzioni su indici
	- Opzioni su azioni
	- Futures su energia elettrica
	- IDEM-Agrex
	- Futures su dividendi azionari
- Tah
    - Azioni
	- Securitised Derivatives
- Fondi ed ETC-ETN
    - MIV-Fondi Chiusi
	- ETF
	- ETC ed ETN
	- OICR Aperti
- Controvalori Totali
    - Controvalori Diurno
	- Controvalori Serale
- MOT
    - Titoli di Stato italiani
	- Titoli di Debito in euro
	- Euro-obbligazioni
	- ABS

## Usage

Import the library as usual

```import bitscraper as bs```
## Examples
### Initialize scraper
First you need to initialize the scraper
```scraper = bs.BITScraper()```
### Categories
```scraper.get_categories()```
### Sub-categories
If you need all the subcategories:
```scraper.get_subcategories()```
If you need only the subcategories of a specific category
```scraper.get_subcategories(category="Indici")```
### Derivatives
You need to know both the category and the subcategory of the products you need.
```scraper.get_products(category="Derivati", subcategory="Futuressuenergiaelettrica")```
A list of ids will be returned.
To get the product details, just run the following script
```scraper.get_details(category="Derivati", subcategory="Futuressuenergiaelettrica",products=["1152459"])```
### Stocks
Before getting a stock detail, you need to identify the stock name (at the moment is not possibile searching by ticker).
The following script will return a list with all the stock names
```bs.StockScraper().get_stocks_list()```
Once identified the stock of interest, this script will return you the stock details
```bs.StockScraper().get_stock_info('TRIPADVISOR')```