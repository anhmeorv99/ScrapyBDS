import scrapy
import requests


class ExpresSpider(scrapy.Spider):
    name = 'realestate'
    home_page = "http://nhadatdongnai247.com.vn"
    start_urls = [
        "http://nhadatdongnai247.com.vn"
    ]
    list_infor_broker = []

    def parse(self, response):  # mở các page 1-10 từ trang
        link_page = "http://nhadatdongnai247.com.vn/handler/commonhandler.aspx?command=21&page="
        for i in range(10):
            yield scrapy.Request(link_page + str(i + 1), callback=self.parse_link)

    def parse_link(self, response):
        for item_link in response.xpath('//div[@class="vip-title"]//a/@href').extract():
            yield scrapy.Request(self.home_page + item_link, callback=self.parse_item)

    def parse_item(self, response):
        infor_broker = {}

        infor_apartment = {}
        string_img = ''
        infor_broker['name'] = response.xpath('//div[@class="name"]/text()').get()
        infor_broker['phone_number'] = response.xpath('//div[@class="fone"]/text()').get()

        if infor_broker not in self.list_infor_broker:
            try:
                req = requests.post(url='http://localhost:1337/infor-brokers', data=infor_broker)
                self.list_infor_broker.append(infor_broker)
                print(infor_broker['name'] + ' : successfully!')
            except Exception as e:
                print(e)


        infor_apartment['name_apartment'] = response.xpath(
            '//meta[@name="keywords"]/@content').get()  # nội dung căn nhà
        infor_apartment['description'] = response.xpath('//div[contains(@class,"detail text-content")]/text()').get()
        infor_apartment['price'] = response.xpath('//span[@class="price"]//span[@class="value"]/text()').get()
        infor_apartment['address_apartment'] = response.xpath(
            '//div[@class="address"]//span[@class="value"]/text()').get()

        string_img = "http://nhadatdongnai247.com.vn" + response.xpath('//img[@id="limage"]/@src').get()
        infor_apartment['image_apartment'] = string_img
        infor_apartment['phone_number'] = infor_broker['phone_number']

        # tạo liên kết đến người môi giới

        url_brokers = 'http://localhost:1337/infor-brokers'

        infor_apartment['infor_broker'] = int(self.find_id_broker(url_brokers, infor_apartment['phone_number']))
        try:
            req = requests.post(url='http://localhost:1337/apartments', data=infor_apartment)
            print(infor_apartment['name_apartment'] + ' : successfully !')
        except Exception as e:
            print(e)

    def find_id_broker(self, url, phone_number):
        try:
            req = requests.get(url=url, params={'phone_number': phone_number})
            item = req.json()
            return item[0]['id']
        except Exception as e:
            return None
