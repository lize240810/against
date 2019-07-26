# coding:utf-8
'''
食品抽检信息瑞数反爬
'''
import requests
import execjs
from lxml import etree
import os


with open(r'getcookie.js', 'r', encoding='utf-8') as f:
    js1 = f.read()
    ecjs = execjs.compile(js1)


class SpiderMain(object):
    def __init__(self):
        # 参数
        self.F82S = ''
        self.F82T = ''
        self.F82T_true = ''
        self.JSESSIONID = ''
        self.meta = ''
        self.url = 'http://samr.cfda.gov.cn/WS01/CL1792/'
        # self.url_list = 'http://app1.sfda.gov.cn/datasearchcnda/face3/base.jsp'
        # 请求头
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache - Control": "max - age = 0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "app1.sfda.gov.cn",
            "Referer": "http://app1.sfda.gov.cn/datasearchcnda/face3/base.jsp?tableId=121&tableName=TABLE121&title=%C8%AB%B9%FA%D2%A9%C6%B7%B3%E9%BC%EC&bcId=152894035121716369704750131820",
            "Upgrade - Insecure - Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
        }

        # 请求cookie
        self.cookies = {
            'FSSBBIl1UgzbN7N82S': '',
            'FSSBBIl1UgzbN7N82T': '',
            'JSESSIONID': ''
        }
        

    def getCookie(self):
        rsq = requests.get(self.url, headers=self.headers)
        rsq.close()
        # print(rsq.cookies)
        # 第一次请求得到假的f82s,f82t,和metacontent
        self.F82S = rsq.cookies['FSSBBIl1UgzbN7N82S']
        self.F82T = rsq.cookies['FSSBBIl1UgzbN7N82T']
        rsqHtml = etree.HTML(rsq.text)
        self.meta = rsqHtml.xpath(
            '//*[@id="9DhefwqGPrzGxEp9hPaoag"]/@content')[0]
        self.F82T_true = ecjs.call("getcookie", self.meta, self.F82T)
        self.cookies['FSSBBIl1UgzbN7N82S'] = self.F82S
        self.cookies['FSSBBIl1UgzbN7N82T'] = self.F82T_true
        rsq = requests.get(self.url, headers=self.headers,
                           cookies=self.cookies)
        print(rsq.status_code)
        return rsq

if __name__ == '__main__':
    spider = SpiderMain()
    rsq = spider.getCookie()
