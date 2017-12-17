# -*- coding: utf-8 -*-
import scrapy
import os

import logging
import logging.config
import ast

# CONFIGURATION FILE
CURRENT_DIR = os.getcwd()


# Configuration Parameters
MAIN_URL = "main_url"  # the starting point of the crawler
CATEGORY_NAME = "category_name"  # xpath containing a category name
CATEGORY_PATH = "category_path"  # xpath containing a category link
SUBCATEGORY_NAME = "subcategory_name"  # xpath containing a subcategory name
SUBCATEGORY_PATH = "subcategory_path"  # xpath containing a subcategory link
CATEGORY_RESULTS = "category_results"
SUBCATEGORY_RESULTS = "subcategory_results"
PART_URL="part_url" # string containing inital url path

class CategorySpider(scrapy.Spider):
    '''
    __Category Dumper__ is a configurable crawler which is made to crawl
    job related sites and scrape the categories adn sub-categories.
    The focus is given on websites in which the category and sub-category
    are on different pages. Thus, categoryDumper always follows the link
    given by the category.
    The output of the program is undefined for pages where the category and
    subcategory are on the same page.
    '''

    name = "categorydumper"

    def __init__(self, filename, log_config_file="logging_config.ini"):

        __CONFIG_FILE__ = "configs/" + filename  # internal variable
        # load config file as a python dict in a safe way
        self.config = ast.literal_eval(
                open(__CONFIG_FILE__).read())
        self.start_urls = self.config.get(MAIN_URL, '')

    def parse(self, response):
        '''
        automatically called by scrapy to parse the page.
        Parse does the following :

        1. get a list of results.
        2. Find the category name and link in the result
        3. If there is a sub category, follow the category link
        4. yield output
        '''

        # getting list of categories
        category_results = response.xpath(
                self.config.get(CATEGORY_RESULTS, ''))

        for category in category_results:
            # category name
            category_name = category.xpath(
                    self.config.get(CATEGORY_NAME, "")).extract_first()
            # category link
            category_link = category.xpath(
                    self.config.get(CATEGORY_PATH, "")).extract_first()

            # if part_url is available then, add it to category link
            if 'part_url' in self.config.keys():
                category_link=self.config.get(PART_URL, "")+category_link
            # if only_category parameter is enabled in the configuration,
            # then don't check for sub categories.
            # Else, goto parse_subcategories
            
            if 'only_category' in self.config.keys():
                yield {
                    'category': category_name,
                    'link': category_link
                }
            else:
                yield scrapy.Request(
                        url=category_link,
                        callback=self.parse_subcategory,
                        dont_filter=True,
                        meta={'category': category_name})

    def parse_subcategory(self, response):
        '''
        Similar to `parse`, but parses sb categories and yields the
        output. The meta data given by the parse function contains the
        category name, which is also yielded by this method
        '''
        subcategory_results = response.xpath(
                self.config.get(SUBCATEGORY_RESULTS, ''))

        for subcategory in subcategory_results:
            subcategory_name = subcategory.xpath(
                    self.config.get(SUBCATEGORY_NAME, "")).extract_first()
            subcategory_link = subcategory.xpath(
                    self.config.get(SUBCATEGORY_PATH, "")).extract_first()
            yield {
                'category': response.meta.get("category", ""),
                'subcategory_name': subcategory_name,
                'link': subcategory_link
            }
