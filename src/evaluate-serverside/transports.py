from os import path as op

import tornado.web
import tornadio2
import tornadio2.router
import tornadio2.server
import tornadio2.conn

import tornado.platform.twisted
#from twisted.internet import reactor

from twisted.internet.protocol import ReconnectingClientFactory
from MQTT import MQTTProtocol
from twisted.python import log
import random
ROOT = op.normpath(op.dirname(__file__))


class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('index.html')


class SocketIOHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('../socket.io.js')


class WebSocketFileHandler(tornado.web.RequestHandler):
    def get(self):
        # Obviously, you want this on CDN, but for sake of
        # example this approach will work.
        self.set_header('Content-Type', 'application/x-shockwave-flash')

        with open(op.join(ROOT, '../WebSocketMain.swf'), 'rb') as f:
            self.write(f.read())
            self.finish()


class ChatConnection(tornadio2.conn.SocketConnection):
    # Class level variable
    participants = set()

    def on_open(self, info):
        self.send("Welcome from the server.")
        # TODO create a MQTTClient
        self.mqttClientFactory = MQTTListenerFactory(self)
        self.ClientReaktor = MyReaktor.connectTCP("test.mosquitto.org", 1883, self.mqttClientFactory)
        self.participants.add(self)
        

    def on_message(self, message):
        # Pong message back
        # TODO send message also to MQTTClient
        self.mqttClientFactory.publish("tokudu/beaglebone/"+self.mqttClientFactory.protocol.clientId, ""+str(message))
#        for p in self.participants:
#            if p == self:
#                p.mqttClientFactory.publish("beaglebone/"+p.mqttClientFactory.protocol.clientId, ""+str(message))
#            p.send(message)

    def on_close(self):
        # TODO discard MQTTClient
        # TODO remove scheduled calls (callLater's)
        self.mqttClientFactory.protocol.PingLoop.cancel()
        self.mqttClientFactory.protocol.ProcessMessagesLoop.cancel()
        self.mqttClientFactory.stopTrying()
        self.mqttClientFactory.stopFactory()
        self.ClientReaktor.disconnect()
        self.mqttClientFactory = None
        self.ClientReaktor = None
        print("meeh\n")
        
        self.participants.remove(self)
        
        
class MQTTListener(MQTTProtocol):
    pingPeriod = 60000

    def connectionMade(self):
        log.msg('MQTT Connected')
        self.clientId = "SocketGateway%i" % random.randint(1, 0xFFFF)
        self.connect(self.clientId, keepalive=self.pingPeriod)
        self.ChatConnection = None
        # TODO: make these constants configurable
        self.PingLoop = MyReaktor.callLater(self.pingPeriod//1000, self.pingreq)
        self.ProcessMessagesLoop = MyReaktor.callLater(5, self.processMessages)
            
    def ChatConnection(self):
        return self.factory.ChatConnection
            
    def pingrespReceived(self):
        log.msg('Ping received from MQ broker', logging.DEBUG)
        self.PingLoop = MyReaktor.callLater(self.pingPeriod//1000, self.pingreq)

    def connackReceived(self, status):
        if status == 0:
            self.subscribe("tokudu/beaglebone/#")
        else:
            log.msg('Connecting to MQTT broker failed')
                
    def processMessages(self):
        self.ProcessMessagesLoop = MyReaktor.callLater(5, self.processMessages)
            
    def publishReceived(self, topic, message, qos, dup, retain, messageId):
        # Received a publish on an output topic
        log.msg('RECV Topic: %s, Message: %s' % (topic, message ), logging.DEBUG)
        if self.factory.ChatConnection != None:
            self.factory.ChatConnection.send(message)
        #mqttMessageBuffer.append((topic, message))

class MQTTListenerFactory(ReconnectingClientFactory):
    #protocol = MQTTListener

    def __init__(self, ChatConnection = None, service = None):
        self.ChatConnection = ChatConnection
        self.service = service
        self.protocol = MQTTListener

    def publish(self, topic, message):
        # this is a HACK class needs to be instantiated before it could be used (happens in buildProtocol)
        if self.protocol != MQTTListener:
            log.msg('SEND Topic: %s, Message: %s' % (topic, message ))
            self.protocol.publish(topic, message)

    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        # HACK protocol class is exchanged by instance
        self.protocol = p
        log.msg("protocol build", logging.DEBUG)
        return p
    
    def clientConnectionFailed(self, connector, reason):
        log.err('CAUGHT In The ACT: Connection failed. Reason: %s' % (reason))
        # HACK failed instances where not tolerated, start over 
        self.protocol = MQTTListener
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
        
    def startedConnecting(self, connector):
        log.msg('reset reconnection delay', logging.DEBUG)
        self.resetDelay()

# Create chat server

Tsocket = tornadio2.conn.SocketConnection
ChatRouter = tornadio2.router.TornadioRouter(ChatConnection, dict(websocket_check=True))

# Create application
application = tornado.web.Application(
    ChatRouter.apply_routes([(r"/", IndexHandler),
                             (r"/socket.io.js", SocketIOHandler),
                             (r"/WebSocketMain.swf", WebSocketFileHandler)
                            ]),
    flash_policy_port = 843,
    flash_policy_file = op.join(ROOT, 'flashpolicy.xml'),
    socket_io_port = 8080
)

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    tornado.platform.twisted.install()
    #IOLoop.instance().start()
    tornadio2.server.SocketServer(application,auto_start=False)
    MyReaktor = tornado.platform.twisted.TornadoReactor()
    tornado.ioloop.IOLoop.instance().start()
    
    print("NEVER EVER!!!")
    
    
