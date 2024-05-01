# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewItem(scrapy.Item):
    # product_name = scrapy.Field()
    # pros = scrapy.Field()
    # cons = scrapy.Field()
    review_text = scrapy.Field()
    sentiment = scrapy.Field()
    # rating = scrapy.Field()
    # date = scrapy.Field()
