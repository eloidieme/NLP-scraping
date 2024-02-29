from typing import Any
import scrapy
from scrapy.http import Response

class JobSpider(scrapy.Spider):
    name = "job"

    def parse(self, response: Response, **kwargs: Any) -> Any:
        pass