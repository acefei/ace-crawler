#!/usr/bin/env python
# encoding: utf-8
"""
@author: Acefei
@file: qichacha_with_phantomjs.py
@time: 17-10-19 8:31
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# wait for the page to load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import sys
import time
import json
reload(sys)
sys.setdefaultencoding('utf-8')

####### utils func ########
import contextlib
@contextlib.contextmanager
def smart_quit(thing):
    """
    通过上下文管理器来实现driver自动退出, 而且在with语句内部的function能直接访问
    driver对象，从而能少定义一个入参。
    """
    yield thing
    thing.quit()

def wait_render_and_find_element(pattern, mode=By.XPATH, timeout=30):
    wait = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((mode, pattern))
    )

    # Tricky! Sleep 0.1 sec to ganrantee all of content was rendered well.
    time.sleep(0.1)
    return wait

def extract_link(element):
    return element.get_attribute("href")

def extract_inner_html(element):
    return element.get_attribute("innerHTML")

def print_dict(d):
    print json.dumps(d,ensure_ascii=False)

def view(html, page = "/tmp/view.html"):
    with open(page, 'w') as f:
        f.write(html)
    os.system("chromium "+page)

######## qcc func #######
def custom_headers():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = \
        ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36")
    return dcap

def login_homepage_to_get_cookie():
    """
    访问企查查网站时，服务器会对cookie进行校验，
    所以必须通过匿名访问首页或者用户登陆首页来获取
    注意：匿名用户访问详细信息会受限
    """
    driver.get("http://www.qichacha.com")
    #print driver.get_cookies()
    print "准备..."

def do_query(keyword=u"南京银行"):
    """
    在企查查搜索框搜索keyword相关企业，并取第一个作为最佳匹配结果
    """
    # enter keyword
    input = wait_render_and_find_element("searchkey", By.ID)
    input.send_keys(keyword)

    # submit
    submit = wait_render_and_find_element("V3_Search_bt", By.ID)
    submit.submit()

    # select the first result which is the best matching.
    best_match = wait_render_and_find_element('//*[@id="searchlist"]/table/tbody/tr[1]/td[2]/a')
    # TODO,  can not turn to new page by click
    # best_match.click()
    url = extract_link(best_match)
    driver.get(url)

    firm_name = wait_render_and_find_element('//*[@class="text-big font-bold company-top-name"]')
    print "跳转到[{0}]页面...".format(firm_name.text)

def extract_firm_base(firm_info):
    """
    获取企业基本信息
    """
    firm_info[u"工商信息"] = dict()
    gs_info = firm_info[u"工商信息"]
    gs_list = driver.find_elements_by_xpath('//*[@id="Cominfo"]/table/tbody/tr/td')
    for k, v in zip(gs_list[::2], gs_list[1::2]):
        print k.text, v.text
        gs_info[k.text] = v.text

def extract_ws_content(count, i, tmp_dict):
    """
    企查查web页面需要点击链接来获取判决书正文
    """
    ws_xpath = '//*[@id="wenshulist"]/table/tbody/tr[{0}]/td[{1}]/a[@onclick]'.format(count, i+1)
    pjs = driver.find_element_by_xpath(ws_xpath)
    pjs.click()
    print "获取{0}".format(pjs.text)
    wsview = wait_render_and_find_element('//*[@id="wsview"]')

    tmp_dict['判决书'] = extract_inner_html(wsview)
    # print tmp_dict['判决书']

    # Tricky! It's not have to close the wenmodal.
    # close = driver.find_element_by_xpath('//*[@id="wenModal"]//button')
    # print close.get_attribute("class")
    # close.click()

def extract_firm_susong(firm_info):
    """
    切换导航栏里的tab来获取诉讼信息
    """
    firm_info[u"涉诉列表"] = list()
    ws_list = firm_info[u"涉诉列表"]

    # Tricky! the element found by ID could not click...
    # susong_tab = wait_render_and_find_element("susong_title", By.ID)
    susong_tab = wait_render_and_find_element('//ul[@class="nav nav-tabs"]/li[2]/a')
    tab_text, susong_num = susong_tab.text.split()
    susong_tab.click()

    wenshulist = wait_render_and_find_element("wenshulist", By.ID)
    print u"获取{0}信息...".format(tab_text)
    ws_title = driver.find_elements_by_xpath('//*[@id="wenshulist"]/table/tbody/tr[1]/th')
    ws_item_list = [item.text for item in ws_title]

    ws_detail = driver.find_elements_by_xpath('//*[@id="wenshulist"]/table/tbody/tr/td')
    # reverse for keeping order is in concert with the items below
    ws_detail.reverse()

    # Note: tbody/tr[1] is title, tbody/tr[2] is the value, so here start from 2
    count = 2
    while ws_detail:
        tmp_dict = dict()
        for i, key in enumerate(ws_item_list):
            value = ws_detail.pop().text
            print key, value
            if key == u"案件名称":
                extract_ws_content(count, i, tmp_dict)
            tmp_dict[key] = value
        count += 1
        ws_list.append(tmp_dict)


if __name__ == "__main__":
    firm_info = dict()
    keyword = sys.argv[1].decode('utf-8')
    with smart_quit(webdriver.PhantomJS(desired_capabilities=custom_headers())) as driver:
        login_homepage_to_get_cookie()
        do_query(keyword)
        extract_firm_base(firm_info)
        extract_firm_susong(firm_info)
        print_dict(firm_info)
