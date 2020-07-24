# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FairfaxItem(scrapy.Item):
    # define the fields for your item here like:
    address = scrapy.Field()
    sale_date = scrapy.Field()
    sale_amount = scrapy.Field()
    general_fund_taxes = scrapy.Field()
    special_tax_dist = scrapy.Field()
    current_land = scrapy.Field()
    current_building = scrapy.Field()
    pass
