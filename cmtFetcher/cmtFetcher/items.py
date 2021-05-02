# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CmtfetcherItem(scrapy.Item):
    # define the fields for your item here like:
    wid = scrapy.Field()
    comment_id = scrapy.Field()
    comment_create = scrapy.Field()
    comment_text = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    user_profile = scrapy.Field()
    user_verified = scrapy.Field()
    user_verified_reason = scrapy.Field()
    user_description = scrapy.Field()
    gender = scrapy.Field()
    statuses_count = scrapy.Field()
    source = scrapy.Field()

