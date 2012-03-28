from twisted.internet import reactor, protocol, utils
from twisted.protocols import basic
from twisted.application import service, internet

class FingerProtocol(basic.LineReceiver):

    def lineReceived(self, user):
        #self.transport.write(self.factory.getUser(user) + '\r\n')
        #self.transport.loseConnection()

        d = self.factory.getUser(user)

        def onError(err):
            return 'Internal error in server'
        d.addErrback(onError)

        def writeResponse(msg):
            self.transport.write(msg + '\r\n')
            self.transport.loseConnection()
        d.addCallback(writeResponse)

class FingerFactory(protocol.ServerFactory):

    protocol = FingerProtocol

    def __init__(self, **kwargs):
        self.users = kwargs

    def getUser(self, user):
        return utils.getProcessOutput('who') 

application = service.Application('finger', uid = 1, gid = 1)
factory = FingerFactory(yan='Blue_elven')

#reactor.listenTCP(1079, FingerFactory(yan='blue_eleven',future='Very Good!'))
internet.TCPServer(79,
        factory).setServiceParent(service.IServiceCollection(application))
reactor.run()
