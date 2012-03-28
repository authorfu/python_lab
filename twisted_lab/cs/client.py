from twisted.internet.protocol import ClientFactory, Protocol
from sys import stdout
import json

data = {'a': '123', 'b': '456'}


class Sender(Protocol):
    
    def connectionMade(self):
        self.transport.write(json.dumps(data))

    def dataReceived(self, data):
        data = json.loads(data)
        stdout.write('num %d' %self.factory.num)
        for k, v in data.items():
            stdout.write('result is %s' %v)

        self.transport.loseConnection()

class SenderFactory(ClientFactory):
    
    count = 1

    def __init__(self):
        self.num, count = SenderFactory.count, SenderFactory.count + 1

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        result = Sender()
        result.factory = self
        return result

    def clientConnectionLost(self, connector, reason):
        print 'Lost connectin. Reason:',  reason

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason


if __name__ == '__main__':
    from twisted.internet import reactor
    reactor.connectTCP('localhost', 8000, SenderFactory())
    reactor.connectTCP('localhost', 8000, SenderFactory())
    reactor.connectTCP('localhost', 8000, SenderFactory())
    reactor.connectTCP('localhost', 8000, SenderFactory())
    reactor.connectTCP('localhost', 8000, SenderFactory())
    reactor.connectTCP('localhost', 8000, SenderFactory())

    reactor.run()
