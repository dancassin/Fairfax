# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FairfaxItem(scrapy.Item):
    #define the fields for your item here like:
    address = scrapy.Field()
    lot_sqft = scrapy.Field()
    sale_date = scrapy.Field()
    sale_amount = scrapy.Field()
    general_fund_taxes = scrapy.Field()
    special_tax_dist = scrapy.Field()
    current_land = scrapy.Field()
    current_building = scrapy.Field()
    style = scrapy.Field()
    total_basement_area = scrapy.Field()
    bedrooms = scrapy.Field()
    full_baths = scrapy.Field()
    half_baths = scrapy.Field()
    construction_quality = scrapy.Field()
    condition_grade = scrapy.Field()
    liv_area_sqft = scrapy.Field()
    pass
