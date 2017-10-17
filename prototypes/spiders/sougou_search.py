import os
import scrapy
import sys

from scrapy.http import HtmlResponse

from prototypes.utils.common import get_html_body

reload(sys)
sys.setdefaultencoding('utf-8')



class SGSearchSpider(scrapy.Spider):
    name = os.path.basename(__file__).split('.')[0]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
            'prototypes.middlewares.RandomHttpProxyMiddleware_v1': 300,

            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'prototypes.middlewares.RandomUserAgentMiddleware': 301,
        }
    }

    search_nav = {
        'web': {
            'url': 'http://www.sogou.com/web?query="{0}"',
        },
        'news': {
            'url': 'http://news.sogou.com/news?query={0}',
            'items_url_xpath': '//h3/a/@href',
        },
    }

    def __init__(self, **kw):
        super(SGSearchSpider, self).__init__(**kw)
        self.kw = kw.get('keyword')
        self.nav = kw.get('nav', 'news')
        self.query = self.search_nav[self.nav]
        self.depth = kw.get('depth', '1')
        self.custom_settings.update({'DEPTH_LIMIT': self.depth})

    def start_requests(self):
        query_url = self.query['url']
        request = scrapy.Request(query_url.format(self.kw),
                                 callback=getattr(self, 'parse_' + self.nav))

        # See RandomHttpProxyMiddleware_v1
        request.meta['change_proxy'] = True
        yield request

    def parse_web(self, response):
        pass

    def parse_news(self, response):
        items = response.xpath(self.query['items_url_xpath']).extract()
        for i, item in enumerate(items):
            self.logger.debug("Item {0} url is {1}".format(i, item))
            yield scrapy.Request(item, callback=self.parse_content)

    def parse_content(self, response):
        if not isinstance(response, HtmlResponse):
            return

        link_info = {'url': response.url,
                'title': '',
                'body_text': ''}

        # get title
        title = response.xpath("//title/text()").extract_first()
        if title:
            link_info['title'] = title

        # get body text
        #html_content = response.body.decode(response.encoding).encode('utf-8')
        html_content = response.body
        content = get_html_body(html_content)
        if content:
            link_info['body_text'] = content

        yield link_info

