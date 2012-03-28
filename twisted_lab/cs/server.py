from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import json
from time import sleep

class Echo(Protocol):

    def dataReceived(self, data):
        data = json.loads(data)
        sleep(1)
        for k, v in data.items():
            print 'key %s has %s as value' %(k,v)
        self.transport.write(json.dumps({'result':'ok'}))
        self.transport.loseConnection()

class EchoFactory(Factory):

    protocol = Echo

    pass

reactor.listenTCP(8000, EchoFactory())
reactor.run()

