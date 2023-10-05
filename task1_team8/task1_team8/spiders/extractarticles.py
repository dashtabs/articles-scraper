from __future__ import absolute_import
import scrapy
import json
import hashlib
import datetime

from ..items import Task1Team8Item


class ExtractArticlesSpider(scrapy.Spider):
    name = "text"

    def start_requests(self):
        with open('./links1.json', encoding='utf-8') as json_file:
            data = json.load(json_file)

        for link_url in data:
            print('' + link_url['link'])
            request = scrapy.Request(link_url['link'], callback=self.parse)
            yield request

    def parse(self, response, **kwargs):
        item = Task1Team8Item()

        item['article_link'] = response.url
        item['article_uuid'] = hashlib.sha256(str(response.url).encode('cp437')).hexdigest()
        item['article_title'] = response.xpath('//div[@class="article"]/h1/text()').extract()
        if not item['article_title']:
            item['article_title'] = response.xpath('//div[@class="span12"]/h1/text()').get().replace('\n', '').replace('\t', '').strip()
        item['article_datetime'] = response.xpath('//div[@class="article__info-item time "]/text()').extract()
        if not item['article_datetime']:
            item['article_datetime'] = "Date not specified"
        item['article_author'] = response.xpath('//*[@id="block_left_column_content"]/div/div/div[2]/div[1]/p/a/text()').extract()
        if not item['article_author']:
            item['article_author'] = "Author not specified"
        item['article_summary'] = response.xpath('//*[@id="block_left_column_content"]/div/div/p/text()').extract()
        if not item['article_summary']:
            item['article_summary'] = "Summary not specified"
        item['scrapping_date'] = datetime.date.today()
        item['article_text'] = ''.join(
            [s.strip() for p in response.xpath('//div[@class="span12"]/p') for s in p.xpath('.//text()').extract()])
        if item['article_text'] == '' or not item['article_text'] :
            item['article_text'] = ["\n".join(line.strip()
                                              for line in
                                              response.xpath('//div[@class="article-text  "]//text()').extract()
                                              if line.strip())]
            # item['article_text'] = ["\n".join(line.strip()
            #                         for line in response.xpath('//div[@class="span12"]/p/text()').extract()
            #                         if line.strip())]
        return item
