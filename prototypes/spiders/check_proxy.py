import scrapy


class CheckProxySpider(scrapy.Spider):
    name = "check_proxy"
    start_urls = ['https://httpbin.org/get?show_env=1']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
        'prototypes.middlewares.RandomHttpProxyMiddleware_v1':1,}
    }

    def parse(self, response):
        print response.body
