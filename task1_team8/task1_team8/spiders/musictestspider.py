import scrapy
from w3lib.url import add_or_replace_parameter


class MusicTestSpider(scrapy.Spider):
    # name = 'links'
    # start_urls = ['https://www.unian.ua/lite/music', 'https://uamusic.com.ua/uanews']
    #
    # def parse(self, response, **kwargs):
    #     yield scrapy.Request(url='https://www.unian.ua/lite/music', callback=self.parse_page)
    #     for i in range(1, 37):
    #         url = response.url + '?ajax=1&page=' + str((i+1))
    #         if 'https://uamusic.com.ua/uanews' in url:
    #             continue
    #         yield scrapy.Request(url, callback=self.parse_page)
    #     yield scrapy.Request(url='https://uamusic.com.ua/uanews', callback=self.parse_page)
    #     for i in range(40, 241, 40):
    #         url = response.url + '?start=' + str(i)
    #         if 'https://www.unian.ua/lite/music' in url:
    #             continue
    #         yield scrapy.Request(url, callback=self.parse_page)
    #
    # def parse_page(self, response):
    #     for items in response.css('div.lite-background__item'):
    #         yield {
    #             'title': items.css('a.lite-background__link::text').get().replace('\n', ''),
    #             # 'date': items.css('span.lite-background__date::text').get(),
    #             'link': items.css('a.lite-background__link').attrib['href'],
    #         }
    #     if not response.css('div.lite-background__item'):
    #         for items in response.css('article.news-cat'):
    #             yield {
    #                 'title': items.css('.article-title-news a::text').get().replace('\n', '').strip(),
    #                 # 'date': items.css('').get(),
    #                 'link': 'https://uamusic.com.ua' + items.css('a').attrib['href'],
    #                 }
    name = 'links'
    start_urls = [
        'https://www.unian.ua/lite/music',
        'https://uamusic.com.ua/uanews'
    ]

    def parse(self, response, **kwargs):
        if 'unian.ua' in response.url:
            yield from self.parse_unian(response)
        elif 'uamusic.com.ua' in response.url:
            yield from self.parse_uamusic(response)

    def parse_unian(self, response):
        for items in response.css('div.lite-background__item'):
            yield {
                'title': items.css('a.lite-background__link::text').get().replace('\n', ''),
                'link': items.css('a.lite-background__link').attrib['href'],
            }

        for page in range(1, 37):
            url = add_or_replace_parameter(
                url=response.url, name="page", new_value=str(page + 1)
            )
            print(url)
            yield scrapy.Request(url, callback=self.parse_unian)

    def parse_uamusic(self, response):
        for items in response.css('article.news-cat'):
            yield {
                'title': items.css('.article-title-news a::text').get().replace('\n', '').strip(),
                'link': 'https://uamusic.com.ua' + items.css('a').attrib['href'],
            }

        for offset in range(40, 241, 40):
            url = add_or_replace_parameter(
                url=response.url, name="start", new_value=str(offset)
            )
            yield scrapy.Request(url, callback=self.parse_uamusic)
