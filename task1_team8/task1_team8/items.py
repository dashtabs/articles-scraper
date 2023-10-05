# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class Task1Team8Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_link = scrapy.Field()
    article_uuid = scrapy.Field()
    article_title = scrapy.Field()
    article_id = scrapy.Field()
    article_datetime = scrapy.Field()
    article_author = scrapy.Field()
    article_summary = scrapy.Field()
    scrapping_date = scrapy.Field()
    article_text = scrapy.Field()
    # pass
