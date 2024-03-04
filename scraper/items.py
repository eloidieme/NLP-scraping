# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BoardItem(scrapy.Item):
    unique_id = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    date = scrapy.Field()
    contract = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    link = scrapy.Field()

class JobItem(scrapy.Item):
    unique_id = scrapy.Field()
    description = scrapy.Field()
    starting_date = scrapy.Field()
    degree = scrapy.Field()
    experience = scrapy.Field()
    skills = scrapy.Field()
