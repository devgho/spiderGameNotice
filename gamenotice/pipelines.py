# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GamenoticePipeline:
    def process_item(self, item, spider):
        with open("f1.txt", "w") as f:
            f.writelines(item.values())
        return item
