#!/usr/bin/python
# coding:utf-8

import unittest as ut
import os
import sqlite3

from data_saver import Storage

class TestStorageInit(ut.TestCase):

    def setUp(self):
        self.db_file = 'unittest.db'
    
    ut.skip('default init_db need interactive')
    def test_init_db(self):
        Storage.init_db(self.db_file, force=False)
        self.assertTrue(os.path.isfile(self.db_file), u'数据库文件没有生成！')

    def test_init_db_force(self):
        Storage.init_db(self.db_file, force=True)
        self.assertTrue(os.path.isfile(self.db_file), u'数据库文件没有生成!')

    def test_web_content_create(self):
        Storage.init_db(self.db_file, force=True)
        conn = sqlite3.connect(self.db_file)
        try:
            table = conn.execute('select * from sqlite_master').next()
            self.assertIn('web_page', table)
        except:
            pass

class TestStorage(ut.TestCase):

    def setUp(self):
        self.db_file = 'test2.db'
        Storage.init_db(self.db_file, force=True)
        self.storage = Storage(self.db_file)

    def test_save_content(self):
        count = self.storage.save_content('www.sina.com', 'title', 'content')
        self.assertEqual(1, count)
        self.assertIn('www.sina.com', self.storage)

    def tearDown(self):
        pass

if __name__ == '__main__':
    ut.main()
