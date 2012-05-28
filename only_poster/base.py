#!/usr/bin/python
# coding:utf-8

from pyquery import PyQuery as Query
import urllib
import re

class OnlyPoster(object):

    def __init__(self, url_format, title, file_path):
       self.url_format = url_format
       self.output = open(file_path, 'w+')
       self.output.write(title + "\n\n")


    def get_and_parse_firstpage(self):
        self.read_page(1)
        self.extract_posts()
        self.get_poster()
        self.parse_pages()
        
    def read_page(self, page):
        url = self.url_format %(page)
        content = urllib.urlopen(url).read()
        content = re.subn(r'</?br/?>','\n', content)[0]
        self.page = Query(content)

    # 提取所有帖子，每个子类都必须覆盖此方法
    def extract_posts(self):
        self.posts = self.page(".item")

    # 分析帖子，返回发帖人，帖子内容, 每个子类都必须实现
    def parse_post(self, post):
        post = Query(post)
        return post('a:first').text(), post('.post').text()
    
    def get_poster(self):
        self.author = self.parse_post(self.posts[0])[0]

    def save_one_page(self):
        contents = []
        for post in self.posts:
            author, content = self.parse_post(post)
            if author == self.author and self.is_valid_content(content):
                contents.append(content)
        self.output.write('\n\n\n'.join(contents).encode('utf8'))

    def parse_pages(self):
        page_num = self.page('#pageForm')('span:first').text()
        self.total = int(page_num[1:][:-1])

    def download_and_save(self):
        for i in range(1, self.total):
            self.read_page(i)
            self.extract_posts()
            self.save_one_page()

    def is_valid_content(self, content):
        return not (content.startswith('@') or len(content) < 100)

def test():
    only_poster = OnlyPoster('http://www.tianya.cn/techforum/content/16/%d/753746.shtml', 'story', '/home/blue/story.txt')
    with open('/home/blue/story.html', 'r') as f:
        content = f.read()
    only_poster.page = Query(content)
    only_poster.get_and_parse_firstpage()
    only_poster.download_and_save()
    
if __name__ == '__main__':
    test()
