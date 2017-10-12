# -*- coding: utf-8 -*-

import requests
from fake_useragent import UserAgent


class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())
        spider.logger.debug('[RandomUserAgentMiddleware] Request Headers: {0}'.format(request.headers))


class RandomHttpProxyMiddleware(object):
    def __init__(self, crawler):
        self.proxy_restful = crawler.settings.get('PROXY_URL', None)

    def _fetch_proxy(self):
        for _ in xrange(3):
            res = requests.get("{0}/get".format(self.proxy_restful))
            if res.status_code != 200:
                continue

            if self._double_check_conn(res.content):
                return res

        return None

    def _double_check_conn(self, proxy):
        proxies = {"http": "http://{0}".format(proxy)}
        try:
            r = requests.get('https://httpbin.org/get?show_env=1', proxies=proxies)
            if r.status_code == 200:
                print r.json()
                return True
        except:
            self._remove_proxy(proxy)
            return False

    def _remove_proxy(self, proxy):
        return requests.get("http://{0}/delete/?proxy={1}".format(self.proxy_restful, proxy))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        if self.need_to_change_proxy():
            proxy = self._fetch_proxy()
            if proxy is None:
                spider.logger.error("Fetch http proxy failed!")
                return response

            request.mate['proxy'] = "http://{0}".format(proxy)
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request
        return response

    def need_to_change_proxy(self, *args, *kwargs):
        return False
