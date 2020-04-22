# -*- coding: utf-8 -*-
import json
import scrapy
from tencent.items import TencentItem


class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['careers.tencent.com']
    start_urls = []
    for page in range(1, 10):
        url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1587458177901&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'.format(page)
        start_urls.append(url)

    def parse(self, response):
        content = response.body.decode('utf-8')
        data = json.loads(content)
        job_list = data['Data']['Posts']
        for job in job_list:
            item = TencentItem()
            item['name'] = job['RecruitPostName']
            item['duty'] = job['Responsibility']  # 工作职责
            item['location'] = job['LocationName']  # 工作国家
            yield item

        # div_list = response.xpath('')
        # print(div_list)
        # div_list = response.xpath('/html/body/div/div[4]/div[3]/div[2]/div[2]')
        # /html/body/div/div[4]/div[3]/div[2]/div[2]
        # for div in div_list:
        #     item = {}
        #     item["title"] = div.xpath('/h4/text()').extract_first()
        #     print(item)
