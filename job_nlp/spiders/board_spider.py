from typing import Any
import scrapy
from scrapy.http import Response

class BoardSpider(scrapy.Spider):
    name = "board"
    start_urls = ['https://groupecreditagricole.jobs/fr/nos-offres/metiers/170477/']
    
    def parse(self, response: Response, **kwargs: Any) -> Any:
        for offers in response.css('a.card.offer.detail'):
            yield {
                'title': offers.attrib['data-gtm-jobtitle'],
                'category': offers.attrib['data-gtm-jobcategory'],
                'date': offers.attrib['data-gtm-jobpublishdate'],
                'contract': offers.attrib['data-gtm-jobcontract'],
                'country': offers.attrib['data-gtm-jobcountry'],
                'city': offers.attrib['data-gtm-jobcity'],
                'link': offers.attrib['href'] 
            }
        
        current = int(response.css('nav.pagination-bottom').css('li.current-folio').css('a.folio-item').attrib['data-page'])
        for pages in response.css('nav.pagination-bottom').css('ul.folios').css('li.folio'):
            try:
                if int(pages.css('a.folio-item').attrib['data-page']) == current + 1:
                    next_page = pages.css('a.folio-item').attrib['href']
                    if next_page is not None:
                        yield response.follow(next_page, callback=self.parse)
            except:
                break
                    