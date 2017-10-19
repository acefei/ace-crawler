# encoding: utf-8

class ParseCookie(object):
    """
    将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
    """
    def __init__(self, cookie):
        self.cookie = cookie

    def str2dict(self):
        cookie_dict = dict()
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            cookie_dict[key] = value
        return cookie_dict

if __name__ == "__main__":
    cookie = 'acw_tc=AQAAAD/a8WLR1gUAVewZcN3tZ9nmho8M; UM_distinctid=15f327298f96d6-038efaaf5ffdd3-3e63430c-144000-15f327298fa4d1; hasShow=1; _uab_collina=150837989429404563531932; _umdata=65F7F3A2F63DF0206B3C872D7FC69168A5F4E56D47227A8819B03954C70FE34EDDF02BFACE3C2FF0CD43AD3E795C914CE49B1734621A1E9528D35D08FBEB385A; PHPSESSID=hv55kkvlbf93ceu0nnbbs7jq21; zg_did=%7B%22did%22%3A%20%2215f3272991349d-0815224c83469b-3e63430c-144000-15f327299151cd%22%7D; CNZZDATA1254842228=544534333-1508376051-%7C1508376051; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201508379891992%2C%22updated%22%3A%201508379938150%2C%22info%22%3A%201508379891994%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22603f45200bf6045947f0c969aedb97f8%22%7D'
    print ParseCookie(cookie).str2dict()
