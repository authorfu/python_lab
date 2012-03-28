#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib
from BeautifulSoup import BeautifulSoup 
import re
import os

def write_to_file(file_name, content):
    file_path = os.path.join(u'/home/blue/碧落花飘香', file_name)
    f = open(file_path, 'w+')
    f.write(content)
    f.close()

def read_from_url(url):
    lnk = urllib.urlopen(url)
    result = lnk;
    lnk.close
    return result

def make_soup(html):
    return BeautifulSoup(html)

def read_note(note_url):
    return read_from_url(note_url)

def note_urls(soup):
    return set(lnk['href'] for lnk in soup.findAll('a', 'll'))

def get_page_urls(soup):
    
    return set(link['href'] for link in
            soup.find('div','paginator').findAll('a'))

def download_note(url):
    html = read_from_url(url)
    soup = make_soup(html)
    
    header = soup.find('div','note-header')
    note = soup.find('div', id=re.compile('^note_\d+_full$'))
    
    template = make_soup('''<html><body></body></html>''')
    template.body.insert(0, header)
    template.body.insert(1, note)

    write_to_file(header.h3.text, template.prettify())

def download_notes(page_url):
    html = read_from_url(page_url)
    soup = make_soup(html)

    for note_url in note_urls(soup):
        download_note(note_url)


if __name__ == '__main__':
    
    first_page_url = 'http://www.douban.com/people/blhpx/notes'

    download_notes(first_page_url)
    
    soup = make_soup(read_from_url(first_page_url))

    for page_url in get_page_urls(soup):
        download_notes(page_url)
    


