# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import uuid

class UniqueIDPipeline:
    def process_item(self, item, spider):
        if spider.name == 'board':
            item['unique_id'] = str(uuid.uuid4())
        return item