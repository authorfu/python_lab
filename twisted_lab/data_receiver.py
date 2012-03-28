from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import json
from datetime import datetime
from pymongo import Connection
from time import sleep
import random

class DataReceiver(Protocol):

    count = 1

    def __init__(self):
        self.num, DataReceiver.count = DataReceiver.count, DataReceiver.count+1
        print 'No.%d connection build' %self.num

    def dataReceived(self, data):
        
        #print 'receiver num %d recevie data at %s' %(self.num, datetime.now())
        self.factory.write(json.loads(data))
        self.transport.write(json.dumps({'result': 'True'}))

        #sleep(random.uniform(0.01, 0.05))

        #print 'receiver num %d write data to db at %s' %(self.num, datetime.now())
        self.transport.loseConnection()

class ReceiverFactory(Factory):

    protocol = DataReceiver

    def __init__(self):
        self.connection = Connection()
        self.db = self.connection.mongo_lab
        self.sale = self.db.sale

    def write(self, data):
        self.sale.insert(data)


reactor.listenTCP(8000, ReceiverFactory())
reactor.run()

