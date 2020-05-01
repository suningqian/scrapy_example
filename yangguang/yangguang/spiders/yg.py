# -*- coding: utf-8 -*-
import urllib

import scrapy
from yangguang.items import YangguangItem


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&type=4&page=1']

    def parse(self, response):
        # 分组
        li_list = response.xpath('//ul[@class="title-state-ul"]/li')
        for li in li_list:
            item = YangguangItem()
            item["title"] = li.xpath('./span[@class="state3"]/a/text()').extract_first()
            item["href"] = li.xpath('./span[@class="state3"]/a/@href').extract_first()
            item["publish_date"] = li.xpath('./span[@class="state5 "]/text()').extract_first()

            if item["href"] is not None:
                item["href"] = "http://wz.sun0769.com" + item["href"]
                yield scrapy.Request(
                    item["href"],
                    callback=self.parse_detail,  # 由哪个函数处理
                    meta={"item": item}
                )

            # 翻页
        next_url = response.xpath('//a[@class="arrow-page prov_rota"]/@href').extract_first()

        next_url = "http://wz.sun0769.com" + next_url

        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self, response):  # 处理详情页
        item = response.meta["item"]
        item["content"] = response.xpath('//div[@class="details-box"]//text()').extract()
        item["content_img"] = response.xpath('//div[@class="clear details-img-list Picture-img"]/img/@src').extract()
        yield item
