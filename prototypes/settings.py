# -*- coding: utf-8 -*-

BOT_NAME = 'prototypes'

SPIDER_MODULES = ['prototypes.spiders']
NEWSPIDER_MODULE = 'prototypes.spiders'


####### Below is Common Settings #######

# If you want to add the custom settings, please refer to  
# https://doc.scrapy.org/en/latest/topics/settings.html?highlight=custom%20setting#settings-per-spider
LOG_LEVEL = 'DEBUG'

DOWNLOAD_TIMEOUT = 15

# Settings for anti-anti-crawl
RETRY_ENABLED = False
COOKIES_ENABLED = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 60

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1

# HTTP Proxy Restful, please pull git@github.com:acefei/proxy_pool.git
PROXY_URL = 'http://localhost:5000'

# Settings for fake_useragent module
UA_TYPE = 'random'


# Save result as json
# FEED_URI = 'prototypes.json'

# Json output with chinese
from scrapy.exporters import JsonLinesItemExporter
class CustomJsonLinesItemExporter(JsonLinesItemExporter):
    def __init__(self, file, **kwargs):
        super(CustomJsonLinesItemExporter, self).__init__(file, ensure_ascii=False, **kwargs)

FEED_EXPORTERS = {'json': 'prototypes.settings.CustomJsonLinesItemExporter'}
FEED_EXPORT_ENCODING = 'utf-8'
