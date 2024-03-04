import sys
sys.path.append('../')

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.board_spider import BoardSpider
from spiders.job_spider import JobSpider

process = CrawlerProcess(get_project_settings())
process.crawl(BoardSpider)
process.crawl(JobSpider)