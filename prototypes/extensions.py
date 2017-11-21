#!/usr/bin/env python
# encoding: utf-8
"""
@author: Acefei
@file: extensions.py
@time: 17-11-13 9:48
"""
import logging
from twisted.internet import task
from scrapy.exceptions import NotConfigured
from scrapy import signals

logger = logging.getLogger(__name__)


class CloseSpiderRedis(object):
    """
    Start a task to check if scrapy_redis spider is idle in every minutes,
    when it found the idle times granter then CLOSE_SPIDER_AFTER_IDLE_TIMES which add in settings,
    the spider would be closed.

    Usage:
    In settings.py
    EXTENSIONS = {
         'prototypes.extensions.CloseSpiderRedis': 100,
    },

    CLOSE_SPIDER_AFTER_IDLE_TIMES = 5
    """
    def __init__(self, crawler, idle_close_after_times):
        self.crawler = crawler
        self.stats = crawler.stats
        self.idle_close_after_times = idle_close_after_times
        self.reason = 'close spider after {0} times of spider idle'.format(self.idle_close_after_times)
        self.idle_count = 0
        self.interval = 60.0
        self.multiplier = 60.0 / self.interval

    @classmethod
    def from_crawler(cls, crawler):
        idle_close_after_times = crawler.settings.getint('CLOSE_SPIDER_AFTER_IDLE_TIMES')
        if not idle_close_after_times:
            raise NotConfigured
        o = cls(crawler, idle_close_after_times)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        self.pagesprev = 0
        self.itemsprev = 0

        self.task = task.LoopingCall(self.idle_close, spider)
        self.task.start(self.interval)

    def idle_close(self, spider):
        items = self.stats.get_value('item_scraped_count', 0)
        pages = self.stats.get_value('response_received_count', 0)
        irate = (items - self.itemsprev) * self.multiplier
        prate = (pages - self.pagesprev) * self.multiplier
        self.pagesprev, self.itemsprev = pages, items

        if irate == 0 and prate == 0:
            if self.idle_count == self.idle_close_after_times:
                self.crawler.engine.close_spider(spider, reason=self.reason)
            else:
                self.idle_count += 1

    def spider_closed(self, spider, reason):
        if self.task.running:
            self.task.stop()
