from twisted.internet.protocol import ClientFactory, Protocol
from sys import stdout
import json
from datetime import datetime
import random

class Sender(Protocol):
    
    def __init__(self, factory, num):
        self.num = num
        self.factory = factory

    def connectionMade(self):
        data = {'create_at': str(datetime.now()), 'num': random.randint(0, 10)}  
        self.transport.write(json.dumps(data))

    def dataReceived(self, data):
        data = json.loads(data)
        #print 'result is %s' %data['result']
        self.factory.the_last_job_is_done(self.num)
        self.transport.loseConnection()

class SenderFactory(ClientFactory):
    
    def __init__(self):
        self.count = 0

    def the_last_job_is_done(self, connection_num):
        if self.count == connection_num:
            print 'All jobs are done'

    def startedConnecting(self, connector):
        #print 'Started to connect.'
        pass

    def buildProtocol(self, addr):
        #print 'Connected.'
        self.count += 1
        return Sender(self, self.count)

    def clientConnectionLost(self, connector, reason):
        #print 'Lost connectin. Reason:',  reason
        pass

    def clientConnectionFailed(self, connector, reason):
        #print 'Connection failed. Reason:', reason
        pass

def print_count(i):
    print '%d connection created...' %i

if __name__ == '__main__':
    from twisted.internet import reactor
    from sec_timer import loop_in_sec

    factory = SenderFactory()

    for i in range(100):
        reactor.connectTCP('localhost', 8000, factory)

    reactor.run()

