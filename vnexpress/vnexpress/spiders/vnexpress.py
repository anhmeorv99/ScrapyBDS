import scrapy
from scrapy.spiders import Rule
from vnexpress.items import VnexpressItem
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re


class ExpresSpider(CrawlSpider):
    name = 'vnexpress'
    # home_page = 'https://vnexpress.net'
    start_urls = [
        "https://vnexpress.net"
       # "https://thanhnien.vn"
       # "https://vietnamnet.vn"
    ]

    rules = (
        Rule(LinkExtractor(
            allow=(
                r"^https:\/\/vnexpress.net\/.*-\d{7}\.html$",
            ),
        ),
            callback='parse_item',
           #  follow=True,
        ),
    )

    def parse_item(self, response):
        name_of_file = response.url.split('/')[-1]
        name_of_file = name_of_file.replace('.html', '.txt')
        with open("content_vnexpress/%s" % name_of_file, 'a', encoding='utf-8') as f:
       # with open("content_vnexpress/%s" % name_of_file, 'wb+') as f:


            title = response.selector.xpath('//meta[contains(@itemprop,"headline")]//@content').get() + '<end_of_title>\n'
            f.write(title)

            description = response.selector.xpath(
                '//meta[contains(@itemprop,"description")]//@content').get() + '<end_of_descripton>\n'

            f.write(description)
            content =  response.xpath('//p[contains(@class,"Normal")]/text()').extract()
            content1 = '\n'.join(content)
            f.write(content1)
           
