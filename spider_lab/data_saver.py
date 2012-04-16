#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sqlite3
import os

class Storage(object):
    
    def __init__(self, db_file):
        self.db_file = db_file
        init_db(self.db_file)

    def __connect(self):
        return sqlite3.connect(self.db_file)
    
    def save_content(self, url, title, content):
        with self.__connect() as conn:
            result = conn.execute('insert into web_page(url,title,content) values (?, ?, ?)', (url, title, content))
            conn.commit()
            return result.rowcount
            
    def __contains__(self, url):
        with self.__connect() as conn:
            result = conn.execute('select count(1) from web_page where url = ?', (url,))
            try:
                return result.next()[0] > 0
            except:
                return False

def init_db(db_file):
    db_file = os.path.join(os.getcwd(), db_file)

    if os.path.exists(db_file) and \
           raw_input('数据库已存在，是否删除？[y/n]:') == 'y':
        os.remove(db_file)
    else:
        return
    
    with sqlite3.connect(db_file) as db:
        db.execute('create table web_page(url text, title text, content text)');
        db.commit()
    

                       

    

