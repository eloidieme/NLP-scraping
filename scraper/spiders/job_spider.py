from typing import Any, Iterable
import scrapy
from scrapy.http import Response
import json
from scraper.items import JobItem

class JobSpider(scrapy.Spider):
    name = "job"

    custom_settings = {
        'FEEDS': {
            'data/jobs.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
                'overwrite': True,
            },
        },
    }

    def start_requests(self) -> Iterable[scrapy.Request]:
        with open('data/board.json', 'r') as f:
            jobs = json.load(f)
            for job in jobs:
                yield scrapy.Request(job['link'], self.parse_detail, meta={'job_id': job["unique_id"]})

    def parse_detail(self, response: Response) -> Any:
        item = JobItem()
        item["unique_id"] = response.meta['job_id']
        text_list = response.css('section.block.offer-content.text-container ::text').getall()
        all_text = ' '.join([text.strip() for text in text_list if text.strip()])
        item["description"] = all_text
        for infos in response.css('div.block.informations').css('ul'):
            match infos.css('li.information-title ::text').get():
                case "Date de prise de fonction":
                    item["starting_date"] = infos.css('li.information-text ::text').get()
                case "Formation / Spécialisation":
                    item["degree"] = ' '.join([text.strip() for text in infos.css('li.information-text ::text').getall() if text.strip()])
                case "Niveau d'expérience minimum":
                    item["experience"] = infos.css('li.information-text ::text').get()
                case "Compétences recherchées":
                    item["skills"] = ' '.join([text.strip() for text in infos.css('li.information-text ::text').getall() if text.strip()])
                case _:
                    continue
        yield item