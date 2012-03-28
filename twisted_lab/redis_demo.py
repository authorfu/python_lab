#!/usr/bin/python
# coding:utf-8

import redis
import json

data = {'name': 'yanjianbo', 'email': 'yanshiyi1983@163.com'}
ds = json.dumps(data)

rdb = redis.StrictRedis(host='localhost', port=6379, db=0)

def insert():
    rdb.lpush('sale', ds)

if __name__ == '__main__':
    from sec_timer import loop_in_sec

    for i in loop_in_sec(1):
        insert() 
    print '%d items inserted' %i 

