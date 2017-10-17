import requests

RESTAPI = "http://120.25.242.242:10650/getProxy?size=1&stability=100"
# {u'proxyes': [{u'host': u'121.224.123.105', u'password': u'public', u'port': u'8888', u'user': u'adsl'}]}

HEADERS = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
'X-Forwarded-For': '{0}.{1}.{2}.{3}'.format(*__import__('random').sample(range(0,255),4)),
}

def get_proxy():
    return requests.get(RESTAPI, headers=HEADERS).json()['proxyes'][0]

def get_proxy_for_requests():
    proxy = get_proxy()
    uri = "{user}:{password}@{host}:{port}".format(**proxy)
    return {'http': 'http://{0}'.format(uri), 'https': 'https://{0}'.format(uri)}

def get_proxy_for_scrapy():
    proxy = get_proxy()
    return "http://{host}:{port}".format(**proxy), "{user}:{password}".format(**proxy)

def verify():
    proxies = get_proxy_for_requests()
    return requests.get('https://httpbin.org/get?show_env=1', proxies=proxies).json()

def test_x_forwarded_for():
    return requests.get('https://httpbin.org/get?show_env=1', headers=HEADERS).json()


if __name__ == '__main__':
    from pprint import pprint
    #print get_proxy_for_requests()
    #print get_proxy_for_scrapy()
    pprint(verify())
    #pprint(test_x_forwarded_for())

