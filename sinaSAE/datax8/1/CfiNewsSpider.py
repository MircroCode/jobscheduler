#!/usr/local/bin/python
# -*-coding:utf8-*-
import random
from time import sleep

import urllib2
from lxml import etree
import re
import Queue
import json
import MySQLdb
import datetime
import settings

class RotateUserAgent(object):
    def get_agent(self):
        #这句话用于随机选择user-agent
        ua = random.choice(self.user_agent_list)
        if ua:
            return ua
        else:
            return 'TMAX'

    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]


class dbutil(object):
    def __init__(self):
        self.host = settings.DB_HOST_NAME
        self.user = settings.DB_USER_NAME
        self.passwd = settings.DB_PASSWORD
        self.db = settings.DB_DATABASE_NAME
        self.charset = settings.DB_CHARSET
        self.port = settings.DB_PORT

        self.conn = MySQLdb.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd, db=self.db, charset=self.charset)
        self.cur = self.conn.cursor()
    def execute(self, sql, args):
        self.cur.execute(sql, args)
    def fetchall(self):
        self.cur.fetchall()
    def commitAndClose(self):
        self.conn.commit()
        self.conn.close()
    def close(self):
        self.close()

class superSpider(object):
    def __init__(self,spider_name='spiderX', allowed_domain='*', start_url=None, url_regs=['*'], max_deepth=None, save_file=None):
        if start_url is None:
            print 'start_url can not be none'
        if save_file is None:
            save_file = spider_name+'_data.json'

        self.spider_name = spider_name
        self.allowed_domain = allowed_domain
        self.start_url = start_url
        self.save_file = save_file
        self.url_regs = url_regs
        self.max_deepth = max_deepth
        self.spider_interval = settings.SPIDER_INTERVAL

        self.visited_urls=set() #使用set()对象，进行url去重
        self.scheduler_queue = Queue.Queue() #FIFO queue
        self._initVisitedUrls()

    def _initVisitedUrls(self):
        db = dbutil()
        sql = "select fullurl from spider_visited_urls where spider=%s"
        db.execute(sql, self.spider_name)
        visitedUrl = db.fetchall()
        if visitedUrl is not None:
            self.visited_urls = set(visitedUrl)
        print '--Finished load visited url from db.'
    def runSpider(self):
        '''
            使用FIFO的queue作为调度，当下载失败时，跳过，进入下一条url下载
        '''
        self.scheduler_queue.put("0_"+self.start_url)
        while(self.scheduler_queue.qsize()>0):
            level_url = self.scheduler_queue.get()
            level = level_url[:str(level_url).find("_")]
            url = level_url[str(level_url).find("_")+1:]

            #添加对爬取深度的支持，在url前面加上level_代表爬取的深度，当超过最大深度时停止爬取
            if self.max_deepth is not None and int(level) > self.max_deepth:
                continue
            self.visited_urls.add(url)
            try:
                self._downloader(url, level)
                # sleep(self.spider_interval) #爬虫间隔
            except Exception,e:
                print e
                continue

    def _downloader(self, url, level=0):
        rua = RotateUserAgent()
        request = urllib2.Request(url)
        ua = rua.get_agent()
        request.add_header('User-Agent', ua)
        response = urllib2.urlopen(request)
        htmlData = response.read()
        tree = etree.HTML(htmlData)
        # status = response.getcode()
        status = 200
        print '--spider level:', level, 'code:', status, 'url:', url
        self._parse_url(url, tree, self.allowed_domain, self.url_regs, level)
        self._parse_items(url, tree)


    def _parse_url(self, sourceUrl, htmlTree, domainRegexp, urlRegexps, level=0):
        cur_level = int(level) + 1 #下一批链接的爬取深度
        # if self.max_deepth is not None and cur_level > self.max_deepth: #当下一批的链接深度超过最大，停止放入任务队列
        #     return
        urlsInHTML = htmlTree.xpath('//attribute::href')
        domainPattern = re.compile(domainRegexp)
        for urls in urlsInHTML:
            urlEncoded = str(urls.encode('utf8'))
            if urlEncoded.startswith('http') and domainPattern.findall(urlEncoded) and urlEncoded not in self.visited_urls: #去除不符合url匹配规则的，以及访问过的url
                self.scheduler_queue.put(str(cur_level)+"_"+urlEncoded) #url带http通常是大的功能模块,不保存数据库
            elif not (urlEncoded.startswith("www") or urlEncoded.startswith('http'))\
                    and urlEncoded.endswith('.html'):
                for reg in urlRegexps:
                    urlPattern = re.compile(reg)
                    if not urlPattern.findall(urlEncoded):#不满足url过滤条件
                        break
                else:#上面的for发生break，这里就不执行
                    if urlEncoded.startswith("/"):
                        urlEncoded = sourceUrl + urlEncoded
                    else:
                        if not self.allowed_domain.startswith("http://"):
                            pref = "http://"+self.allowed_domain
                        else:
                            pref = self.allowed_domain
                        urlEncoded = pref + "/" + urlEncoded
                    if urlEncoded not in self.visited_urls:
                        self.scheduler_queue.put(str(cur_level) + "_" + urlEncoded)
                        cur_time = datetime.datetime.now().__format__("%Y%m%d%H%M%S")
                        self._saveVisitedUrl2DB((self.spider_name, urlEncoded, cur_time)) #直接将这类承载具体页面内容的页面放入已爬取表，虽然此时还没有开始

            else:
                pass
    def _parse_items(self, url, htmlTree):
        '''
            parse html data
        '''
        titles = htmlTree.xpath("//div[@id='tdcontent']/h1/text()")
        time_author = htmlTree.xpath('//div[@id="tdcontent"]//table[1]//td/text()')
        contents = htmlTree.xpath('//*[@id="tdcontent"]/text()')
        if len(titles) > 0:
            new_titles = ' '.join(titles)
            time_author_str = ' '.join(time_author).replace("&nbsp", ' ')
            news_time = ' '.join(time_author_str.split(' ')[:2] if len(time_author) > 0 else [''])
            news_author = time_author_str.split(' ')[2] if len(time_author) > 0 else ''
            news_content = ' '.join(contents).strip('\r\n').strip().replace('\r\n', ' ').replace('\n', ' ') if len(contents)>0 else ''
            self._save2News((new_titles, news_time, news_author, self.spider_name, news_content, url))

    def _save2File(self, json_data):
        '''
            save json to file
        '''
        if len(json_data)==0:
            return
        f = open(self.save_file, 'a')
        for d in json_data:
            f.write(d)
            f.write('\n')
        f.flush()
        f.close()
    def _saveVisitedUrl2DB(self, urlTuple):
        db = dbutil()
        sql = "insert into spider_visited_urls (spider, fullurl, createdate) values (%s,%s,date_format(%s,'%%Y-%%m-%%d %%H:%%i:%%S'))";
        db.execute(sql, urlTuple)
        db.commitAndClose()
    def _save2News(self, newsTuple):
        db = dbutil()
        sql = "insert into finance_news (title, publish_time, author, source, content, url) values (%s,%s,%s,%s,%s,%s)"
        db.execute(sql, newsTuple)
        db.commitAndClose()


if __name__ == '__main__':
    spider_name = 'cfiNews'
    allowed_domain = 'www.cfi.cn'
    url_regs = ["[0-9a-zA-Z]+.html"]
    start_url = 'http://www.cfi.cn/'
    max_deepth = 4
    spider = superSpider(spider_name, allowed_domain, start_url, url_regs, max_deepth)
    spider.runSpider()
    #TODO:1.每次爬取的新内容，taskid
    #     2.添加新闻爬取时间字段
    #   3.提供接口返回最新一次的新闻
    #   4.添加自动任务
    #   5.添加爬取深度
    #   6.优化已爬取的校验