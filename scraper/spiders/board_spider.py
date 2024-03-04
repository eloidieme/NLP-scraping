from typing import Any
import scrapy
from scrapy.http import Response
from scraper.items import BoardItem

class BoardSpider(scrapy.Spider):
    name = "board"
    start_urls = ['https://groupecreditagricole.jobs/fr/nos-offres/metiers/170477/']

    custom_settings = {
        'FEEDS': {
            'data/board.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
                'overwrite': True
            },
        },
    }
    
    def parse(self, response: Response, **kwargs: Any) -> Any:
        item = BoardItem()
        for offers in response.css('a.card.offer.detail'):
            item['title'] = offers.attrib['data-gtm-jobtitle']
            item['category'] = offers.attrib['data-gtm-jobcategory']
            item['date'] = offers.attrib['data-gtm-jobpublishdate']
            item['contract'] = offers.attrib['data-gtm-jobcontract']
            item['country'] = offers.attrib['data-gtm-jobcountry']
            item['city'] = offers.attrib['data-gtm-jobcity']
            item['link'] = offers.attrib['href'] 

            yield item
        
        current = int(response.css('nav.pagination-bottom').css('li.current-folio').css('a.folio-item').attrib['data-page'])
        for pages in response.css('nav.pagination-bottom').css('ul.folios').css('li.folio'):
            try:
                if int(pages.css('a.folio-item').attrib['data-page']) == current + 1:
                    next_page = pages.css('a.folio-item').attrib['href']
                    if next_page is not None:
                        yield response.follow(next_page, callback=self.parse)
            except:
                break
                    