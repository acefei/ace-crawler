#!/usr/bin/env python
#encoding: utf-8
"""Web Crawler with Keyword on Sougou

Usage:
  run.py [-k KEYWORD] [-n NAV] [-d DEPTH_LIMIT]

Options:
  -k KEYWORD        Query KEYWORD [default: 东莞农村商业银行]
  -n NAV            Query Category, [default: news]
                    Options: [web, news]
  -d DEPTH_LIMIT    The maximum depth that will be allowed to crawl [default: 1]
"""
from docopt import docopt
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


if __name__ == '__main__':
    settings = get_project_settings()

    args    = docopt(__doc__)
    keyword = args['-k']
    nav     = args['-n']
    depth   = args['-d']

    print " k = {0},  n = {1},  d = {2}".format(keyword, nav, depth)

    if depth is not None:
        settings.set('DEPTH_LIMIT', depth)
        print "Update DEPTH_LIMIT settings ", settings.get('DEPTH_LIMIT')

    process = CrawlerProcess(settings)
    process.crawl('sougou_search', keyword=keyword, nav=nav, depth=depth)
    process.start()
