# -*- coding: utf-8 -*-
import datetime
import re

import os

from prototypes.utils.common import get_html_body
from prototypes.utils.parse_cookie import ParseCookie
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class QichacahSpider(scrapy.Spider):
    name = os.path.basename(__file__).split('.')[0]

    allowed_domains = [name+".com"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
            'prototypes.middlewares.RandomHttpProxyMiddleware_v1': 300,

            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'prototypes.middlewares.RandomUserAgentMiddleware': 301,
        }
    }

    # cookie 有效期一个星期
    def __init__(self, qcc_id='hv55kkvlbf93ceu0nnbbs7jq21', *args, **kwargs):
        super(QichacahSpider, self).__init__(*args, **kwargs)
        self.qcc_cookie = {'PHPSESSID': qcc_id}

    # scrapy start and check page num
    def start_requests(self):
        firm_name = '云软件系统'
        request = scrapy.Request(
            "http://m.qichacha.com/search?key="+firm_name,
            # cookies=self.qcc_cookie,
            callback=self.generate_firm_url
        )

        request.meta['query_info'] = {u'企业名': firm_name}
        request.meta['change_proxy'] = True
        yield request

    def generate_firm_url(self, response):
        query_info = response.meta['query_info']
        best_match_url = response.xpath('//div[@class="list-wrap center-content"]/a/@href').extract_first()
        query_info[u'链接'] = best_match_url
        request = response.follow(best_match_url,
                              # cookies=self.qcc_cookie,
                              callback=self.generate_firm_base)

        request.meta['query_info'] = query_info
        yield request

    def generate_firm_base(self, response):
        query_info = response.meta['query_info']

        # get basic info
        query_info['basic'] = dict()
        l_basic = response.xpath('//div[@class="basic-item"]/div/text()').extract()
        # remove the text for 对外投资与任职
        del l_basic[2]
        for k, v in zip(l_basic[::2], l_basic[1::2]):
            query_info['basic'][k] = v.strip()

        yield query_info

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute('scrapy crawl {0}'.format(os.path.basename(__file__).split('.')[0]).split())

