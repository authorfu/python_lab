from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor, task

import json
import redis
from pymongo import Connection

from time import time

diff_cache = []

def cache_time_diff(diff):
    diff_cache.append(diff)

def show_sum_of_time_diff():
    global diff_cache
    if(diff_cache):
        print 'cost %s second' %(sum(diff_cache)/1000, )
        diff_cache = []

class DataReceiver(Protocol):

    count = 1

    def __init__(self):
        self.num, DataReceiver.count = DataReceiver.count, DataReceiver.count+1

    def dataReceived(self, data):
       
        start = time()
        
        self.factory.write(json.loads(data))
        self.transport.write(json.dumps({'result': 'True'}))
        self.transport.loseConnection()

        cache_time_diff(time() - start)


class ReceiverFactory(Factory):

    protocol = DataReceiver

    def __init__(self):
        self.rdb = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.mongo_connection = Connection()
        self.mongo_db = self.mongo_connection.mongo_lab
        self.sale = self.mongo_db.sale

    def write(self, data):
        self.rdb.lpush('sale', data)

    def sync_data_to_mongo(self):
        sale_len = self.rdb.llen('sale')
        if sale_len < 500:
            return

        [self.sale.insert(json.loads(data)) for data in self.rdb.lrange('sale', 0, 499)]

        self.rdb.ltrim('sale', 500, _len) 


#task.LoopingCall(show_sum_of_time_diff).start(1.0)
factory = ReceiverFactory()

task.LoopingCall(factory.sync_data_to_mongo).start(1.0)
reactor.listenTCP(8000, factory)

reactor.run()

