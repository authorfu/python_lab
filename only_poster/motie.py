#!/usr/bin/python
# coding:utf-8

from pyquery import PyQuery as Query
import urllib
import re

NEWLINE="\r\n"

class OnlyPoster(object):

    def __init__(self, chapter_url, url_format, title, file_path):
       self.url_format = url_format
       self.output = open(file_path, 'w+')
       self.output.write(title + NEWLINE)
       self.chapter_url = chapter_url

    def get_contents(self):
        self.read_page(self.chapter_url)
        self.pages = []
        for link in self.page('.txtbox-item li a'):
            self.pages.append(Query(link).attr('href'))

    def read_page(self, url):
        content = urllib.urlopen(url).read()
        self.page = Query(content)

    # 提取所有帖子，每个子类都必须覆盖此方法
    def extract_posts(self):
        pass 

    # 分析帖子，返回发帖人，帖子内容, 每个子类都必须实现
    def parse_post(self, post):
        post = Query(post)
        return post('h1').text(), post('.page-content').text()
    
    def get_poster(self):
        self.author = self.parse_post(self.posts[0])[0]

    def save_one_page(self):
        title_and_content = self.parse_post(self.page)
        self.output.write(NEWLINE.join(title_and_content).encode('utf8') + NEWLINE)

    def parse_pages(self):
        page_num = self.page('#pageForm')('span:first').text()
        self.total = int(page_num[1:][:-1])

    def download_and_save(self):
        for i in self.pages:
            self.read_page(self.url_format %i)
            self.extract_posts()
            self.save_one_page()

def test():
    only_poster = OnlyPoster('http://www.motie.com/book/992/chapter', 'http://www.motie.com%s', '齐天传', '/home/blue/齐天传.txt')
    only_poster.get_contents()
    only_poster.download_and_save()
    
if __name__ == '__main__':
    
    test()
