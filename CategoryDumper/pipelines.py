# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html




class CategoryDumperPipeline(object):
    '''
    CategoryDumperPipeLine writes all the items which are parsed
    into a file defined by output_filename parameter in the configs
    '''
    def open_spider(self, spider):
        self.write_config = False
        if (spider.config.get("output_filename", None)):
            self.output_file = open(
                    spider.config.get('output_filename', ""), "w")
            self.write_config = True

    def close_spider(self, spider):
        if (self.write_config):
            self.output_file.close()

    def process_item(self, item, spider):
        if (self.write_config):
            line = "{0}${1}|{2}\n".format(
                item.get("link", ""),
                item.get("category", ""),
                item.get("subcategory_name", "")
            )
            print(line)
            self.output_file.write(line)
        return item
