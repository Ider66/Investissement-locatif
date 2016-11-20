import scrapy


class LeBonCoinVente(scrapy.Spider):
    name = "lebon_coin_vente"
    start_urls = ['https://www.leboncoin.fr/ventes_immobilieres/offres/languedoc_roussillon/?th=1&location=Montpellier%2034000&parrot=0&ps=2&pe=6&sqs=1&sqe=6&ros=1&roe=4&ret=2']

    def parse(self, response):
        ITEM_SELECTOR = '.item_infos'
        for item in response.css(ITEM_SELECTOR):

            NAME_SELECTOR = '.item_title'
            PRICE_SELECTOR = '.item_price'
            
            yield {
                'name': item.css(NAME_SELECTOR).extract_first()
                'price': item.css(PRICE_SELECTOR).extract_first()
            }
