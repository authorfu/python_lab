#!/usr/bin/python
# coding:utf-8

import sys, traceback
import urllib
import re
import time

from pyquery import PyQuery as query

from studio import managers
from data_saver import Storage
import logger
from readability import Readability

re_url = r'''
^https?:// # protocol
[\d\-a-zA-Z]+(\.[\d\-a-zA-Z]+)+ # hostname
(?::\d+)? # port
(?:/[\d\-a-zA-Z]*/?)* # path
(?P<qm>\?)?(?(qm)(\w+=.*&?)*)$ # querystring
'''

re_basepath = r'''
https?:// # protocol
[\d\-a-zA-Z]+(\.[\d\-a-zA-Z]+)+ # hostname
(?P<colon>:)?(?(colon)\d+)/? # port
'''

def is_url(url):
    if url is None : return False
    return re.search(re_url, url, re.X) != None
    
def validate_and_extract_basepath(url):
    if is_url(url):
        match = re.match(re_basepath, url, re.X)
        if match : return match.group(0)

    raise NotValidUrl(url)

def has_key(key, content):
    if not key :return True
    #return re.search(key, content) != None
    return key in content
    
class NotValidUrl(Exception):
    
    def __init__(self, url):
        self.url = url
        super(self.__class__, self).__init__()
    
    def __str__(self):
        return 'expect a url in format:[protocol://hostname:port/path?querystring],but given %s' %url

class Status(object):
    
    def __init__(self, before, after):
        self.before = before
        self.after = after
        self.desc = before
        
    def __call__(self, func):
        def wrapper(obj):

            func(obj)
            
            self.desc = self.after
            obj.status = self
        return wrapper
        
    def __str__(self):
        return self.desc
            
class Spider(managers.Job):

    def __init__(self, url, pool, storage, level = 1, keyword='', max_level=5):

        self.url = url if url.startswith('http') else 'http://' + url

        if not is_url(self.url):
            raise ValueError('Expect a url in format:[protocol://hostname:port/path?querystring],but given %s' %url)
        
        if not isinstance(storage, Storage):
            raise ValueError('The storage is supposed to be a object of Storage class!')

        self.level = level
        self.max_level = max_level
        self.keyword = keyword
        self.pool = pool
        self.storage = storage
        self.article = None
        self.status = '没有启动'
        self.start_at = None
        
        super(Spider, self).__init__(self)
    
    def __call__(self):
        
        logger.info("开始抓取%s的内容,页面深度%d" %(self.url, self.level))
        
        self.read()
        
        if self.has_data():self.parse()
        
        if self.is_data_parsed():self.save()
            
        if self.can_deepin():self.generate()
        
        logger.info("来自%s的内容已经处理完成, 耗时%f" %(self.url, self.to_now))
        
    def put_into_pool(self, spider, pool=None):
        pool = pool or self.pool
        pool.put_job(spider)
    
    @Status('网页下载开始', '网页下载结束')
    def read(self):

        try:
            self.html = urllib.urlopen(self.url).read()
        except (IOError, UnicodeEncodeError, UnicodeError), e:
            self.html = None
            print '编码错误！'
    
    def has_data(self):
        return self.html is not None
    
    @Status('提取正文开始', '提取正文结束')
    def parse(self):
        try:
            self.article = Readability(self.html, self.url)
        except UnicodeEncodeError, e:
            print '正文提取失败, 内容来自 %s'  %self.url
            
    def is_data_parsed(self):
        return self.article is not None
    
    @Status('保存正文开始', '保存正文结束')
    def save(self):
       
        if has_key(self.keyword, self.article.title) and \
                             self.url not in self.storage:
            self.storage.save_content(self.article.url, self.article.title, self.article.content)
    
    def can_deepin(self):
        return self.level < self.max_level
   
    @Status('派生子爬虫开始', '派生子爬虫结束')     
    def generate(self):
        
        if self.html is None: return 
        
        self.links = query(self.html)('a')
        for link in self.links:
            href = link.attrib.get('href', None)
            if is_url(href):
                self.put_into_pool(Spider(href, self.pool, self.storage, self.level+1, self.keyword, self.max_level))
            self.links.pop()

    def handle_exception(self, exception):
        traceback.print_exc()
    
    def __str__(self):
        return '''
               %s\n
               I am at level %d and reading from %s 
               ''' %(self.status, self.level, self.url)

       

