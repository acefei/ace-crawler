#!/usr/bin/env python
# encoding: utf-8
"""
@author: Acefei
@file: 58_job_cates.py
@time: 17-10-30 上午2:06
"""


class JobCates(object):
    def __init__(self, device):
        if device == 'pc':
            self.base_url = 'http://j1.58cdn.com.cn/job/pc/full/cate/0.1/jobCates.js'
        elif device == 'm':
            self.base_url = 'http://m.58.com/api/thirdcate/bj/job/'


if __name__ == "__main__":
    pass