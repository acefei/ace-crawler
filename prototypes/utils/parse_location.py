#encoding: utf-8
import requests
from fake_useragent import UserAgent
import re


class ParseLocation(object):
    """
    Parse the location from search engine url which is encrypted string
    """
    def __init__(self, proxy=None):
        self.ua = UserAgent().chrome
        self.location_reg = re.compile(r'window.location.replace\("([^"]+)"\)')
        self.proxy = dict() if proxy is None else proxy

    def run(self, url):
        try:
            body = requests.get(url,
                                headers={"User-Agent": self.ua,
                                         'X-Forwarded-For': '{0}.{1}.{2}.{3}'.format(
                                             *__import__('random').sample(range(0, 255), 4)),
                                         },
                                proxies=self.proxy,
                                timeout=10).content
        except Exception, e:
            print "--> Error:", e
        else:
            m = self.location_reg.search(body)
            if m:
                url = m.group(1)
        return url

if __name__ == "__main__":
    #url = 'https://www.sogou.com/link?url=LeoKdSZoUyDAr6Ild5QHpJaTvP_inKRFjIrho_dN7az_UhTa9FfZYELLdCYoZiKbs540aueKv0Ay-WGTWQLhKM_fE_qQkO2P'
    url = 'https://www.baidu.com/link?url=9JlYgDwzI8hApY_6iHYEUwg-j33TaOY0vmEQ0X7Sl87oHdVBaYjTyJkbRN7lMAAM&wd=&eqid=ef082904000024b30000000359e566c9'
    print ParseLocation().run(url)
