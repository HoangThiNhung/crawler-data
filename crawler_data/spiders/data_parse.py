# -*- coding: utf-8 -*-
import scrapy
import re
import random
from scrapy.http import Request
from scrapy.selector import Selector
from crawler_data.items import CrawlerDataItem


class DataParseSpider(scrapy.Spider):
    name = 'data-parse'
    allowed_domains = ['www.spreadshirt.com']
    start_urls = ['http://www.spreadshirt.com/']

    # categories have to crawl
    categories = [
        {'url': 'https://www.spreadshirt.com/men+t-shirts?q=D1K118614O1', 'patten': 'men', 'type': 't-shirt'},
        {'url': 'https://www.spreadshirt.com/men+hoodies+&+sweatshirts?q=D1K118617O1', 'patten': 'men', 'type': 'hoodies'},
        {'url': 'https://www.spreadshirt.com/women+t-shirts?q=D2K118614O1', 'patten': 'women', 'type': 't-shirt'},
        {'url': 'https://www.spreadshirt.com/women+hoodies+&+sweatshirts?q=D2K118617O1', 'patten': 'women', 'type': 'hoodies'}
    ]

    domain = "https://www.spreadshirt.com"

    def parse(self, response):
        for i in range(len(self.start_urls)):
            link_page = self.categories[i]['url']
            request = Request(link_page, callback=self.parse_link, meta={'patten': self.categories[i]['patten'], 'type': self.categories[i]['type']})
            yield request

    # get link product detail
    def parse_link(self, response):
        sel = Selector(response)
        patten = response.meta['patten']
        type = response.meta['type']

        #links product details
        links = sel.xpath('//*[@id="articleTileList"]/div/a/@href').extract()

        # next page
        next = sel.xpath('//*[@id="paginationBar"]/a[3]/@href').extract()[0]
        if next:
            request = Request(next, callback=self.parse_link, meta={'patten': patten, 'type': type})
            yield request
        if links:
            for i in range(len(links)):
                product_link = self.domain + links[i].split("?")[0]
                product_code = product_link.split("-")[-1]
                request = Request(product_link, callback=self.parse_product, meta={'patten': patten, 'type': type, 'product_code': product_code})
                yield request


    # get link product with color
    def parse_product(self, response):
        sel=Selector(response)

        url = response.url
        patten = response.meta['patten']
        type = response.meta['type']
        product_code = response.meta['product_code']

        colors = sel.xpath('//*[@id="detailColorSelector"]/div[2]/div/@title').extract()
        appearances  = sel.xpath('//*[@id="detailColorSelector"]/div[2]/div/@data-appearance-id').extract()

        for i in range(len(colors)):
            color =  colors[i]
            appearance = appearances[i]
            link = url + "?appearance=" + appearance
            request = Request(link, callback=self.parse_item)
            request.meta['color'] = color
            request.meta['patten'] = patten
            request.meta['product_code'] = product_code
            request.meta['type'] = type
            yield request

    # extract data
    def parse_item(self, response):
        sel = Selector(response)
        type_name = ['t-shirts', 't-shirt', 'tee shirt', 'tee shirts', 'shirt', 'shirts']

        product_code = response.meta['product_code']
        color = response.meta['color']
        patten = response.meta['patten']
        type = response.meta['type']
        name = sel.xpath('//*[@id="detail-header"]/h2/text()').extract()[0]

        item = CrawlerDataItem()
        item['product_asin'] = product_code
        item['product_is_have_patten'] = 1
        item['imported_code'] = product_code + '_' + color
        item['color'] = patten.title() + ' ' + color.title()
        item['image_link'] = 'https:' + sel.xpath('//*[@id="detail-product-image"]/img/@src').extract()[0]
        item['product_description'] = sel.xpath('//*[@id="longDescription"]').extract()[0]
        item['patten'] = patten
        item['original_image'] = item['image_link']

        if type == 't-shirt':
            if not 'shirt' in name:
                item['product_name'] = name + ' ' + random.choice(type_name)
            item['price'] = 18.95
        else:
            item['product_name'] = name
            item['price'] = 34.95

        yield item
