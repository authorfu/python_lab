#!/usr/bin/env python
#-*- coding:utf-8 -*-

import socket
from optparse import OptionParser

from studio import managers
from spider import Spider
from data_saver import Storage
import logger

parser = OptionParser()
parser.add_option("-u", "--url", dest="url",
                  help=u"目标URL，例如:www.sina.com。", metavar="URL")

parser.add_option("-d", "--depth", dest="max_level", type='int',
                  help=u"爬虫要深入的级别。", metavar="DEPTH")

parser.add_option("-f", dest="log_file",
                  help=u"日志文件路径，默认为%default。", 
                  default="spider.log", metavar="LOG_FILE")                 

parser.add_option("-l", "--loglevl", dest="log_level", default='1', type='int',
                  help=u"日志级别，默认为%default。",  metavar="LOG_LEVEL")

parser.add_option("-k", "--key", dest="keyword",
                  help=u"查询关键字，不输入则无差别提取。", 
                  default="", metavar="KEYWORD")    
                  
parser.add_option("-t", "--testself", dest="testself", action='store_true',
                  help=u"是否进行自测",  default=False)                                 

parser.add_option("--thread", dest="num_of_threads", type='int', help=u"线程数")

parser.add_option("--dbfile", dest="db_file", help=u"采集数据存储文件。")

def main():
 
      options, args = parser.parse_args()
      
      socket.setdefaulttimeout(30)
      
      Storage.init_db(options.db_file)
      storage = Storage(options.db_file)
      
      logger.init(options.log_level, options.log_file)
      
      worker_manager = managers.NormalManager(options.num_of_threads, max_wait_time=400)
      spider = Spider(options.url, worker_manager, storage, 
                    keyword=options.keyword, max_level = options.max_level)
      worker_manager.put_job(spider)
      worker_manager.start()


if __name__ == '__main__':
	main()
