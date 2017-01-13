import scrapy


class LeBonCoinVente(scrapy.Spider):
    name = "lebon_coin_vente"
    
    start_urls = ['https://www.leboncoin.fr/ventes_immobilieres/offres/languedoc_roussillon/?th=1&location=Montpellier%2034000&parrot=0&ps=2&pe=6&sqs=1&sqe=6&ros=1&roe=4&ret=2']

    def parse(self, response):
        ITEM_SELECTOR = '//*[@id="listingAds"]/section/section/ul/li/a/@href'
        for item in response.xpath(ITEM_SELECTOR).extract():
            yield scrapy.Request(response.urljoin(item), callback=self.parse_page)
        # follow pagination links
        NEXT_PAGE_SELECTOR='/html/body/table/tbody/tr[6434]/td[2]/span[1]/a/@href'
        next_page=response.xpath(NEXT_PAGE_SELECTOR).extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_page(self, response):
        def extractor(query):
            return response.xpath(query).extract_first()
        INTITULE_SELECTOR = '//*[@id="adview"]/section/header/h1/text()'
        PRIX_SELECTOR = '//html/body/table/tbody/tr[553]/td[2]/span/span[6]/text()'
        NBRE_PIECES_SELECTOR = '//html/body/table/tbody/tr[629]/td[2]/text()'
        SURFACE_SELECTOR = '//html/body/table/tbody/tr[638]/td[2]/text()[1]'
        GES_SELECTOR = '//html/body/table/tbody/tr[648]/td[2]/text()'
        ENERGIE_SELECTOR = '//html/body/table/tbody/tr[660]/td[2]/text()'
        DESCRIPTIF_SELECTOR = '//html/body/table/tbody/tr[674]/td[2]/text()'
        
        yield {   
            'intitule' : extractor(INTITULE_SELECTOR),
            'prix': extractor(PRIX_SELECTOR),
            'nbre_pieces' : extractor(NBRE_PIECES_SELECTOR),
            'surface' : extractor(SURFACE_SELECTOR),
            'GES' : extractor(GES_SELECTOR),
            'Energie' : extractor(ENERGIE_SELECTOR),
            'Descriptif' : extractor(DESCRIPTIF_SELECTOR)
        }

