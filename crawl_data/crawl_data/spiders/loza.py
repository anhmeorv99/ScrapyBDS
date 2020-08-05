import os
import scrapy


class LozaSpider(scrapy.Spider):
    name = "loza"
    home_page = 'https://loza.vn'
    start_urls = [
      "https://loza.vn/ao-so-mi-nu",
      # "https://loza.vn/quan-cong-so-nu",
      # "https://loza.vn/vay-dam",
      # "https://loza.vn/chan-vay",
      # "https://loza.vn/vest-nu",
      # "https://loza.vn/ao-khoac-nu",
      # "https://loza.vn/set-do",
      # "https://loza.vn/thoi-trang-dao-pho"
    ]

    def parse(self, response):
      for item_link in response.xpath('//div[contains(@class,"box product-item")]//h3//a//@href').extract():
        yield scrapy.Request(self.home_page + item_link, callback=self.parse_single_item)

    def parse_single_item(self, response):
        list_url = []
        for link in response.xpath('//div[contains(@class,"image-cover")]//img//@src').extract():
            img_link_thumbnail = link.replace("thumbnail", "large")
            split_version = img_link_thumbnail.split('?')
            img_link = split_version[0]
            list_url.append(img_link)
            if 'https' in img_link:
                yield scrapy.Request(img_link, callback=self.parse_img)


  #  def parse_img(self, response):
   #     os.listdir()
    #    with open("./image/%s" % response.url.split('/')[-1], 'wb+') as f:
     #       f.write(response.body)

    # https://loza.vn/uploads/media/product/large/LS1442XA-1.jpg
    # https://loza.vn/uploads/media/product/thumbnail/LS1442XA-1.jpg?v=1595813341000