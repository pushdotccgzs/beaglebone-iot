from twisted.python import log
# from twisted.application.service import Service
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.internet.task import LoopingCall
from MQTT import MQTTProtocol

import random
import sys

class MQTTListener(MQTTProtocol):
    pingPeriod = 60000

    def connectionMade(self):
        log.msg('MQTT Connected')
        self.connect("TwistedMQTT02", keepalive=self.pingPeriod)
        # TODO: make these constants configurable
        reactor.callLater(self.pingPeriod//1000, self.pingreq)
        reactor.callLater(5, self.processMessages)
            
    def pingrespReceived(self):
        log.msg('Ping received from MQ broker')
        reactor.callLater(self.pingPeriod//1000, self.pingreq)

    def connackReceived(self, status):
        if status == 0:
            self.subscribe("#")
        else:
            log.msg('Connecting to MQTT broker failed')
            
    def processMessages(self):
        reactor.callLater(5, self.processMessages)
            
    def publishReceived(self, topic, message, qos, dup, retain, messageId):
        # Received a publish on an output topic
        log.msg('RECV Topic: %s, Message: %s' % (topic, message ))
        #mqttMessageBuffer.append((topic, message))

class MQTTListenerFactory(ClientFactory):
    #protocol = MQTTListener
    
    def __init__(self, service = None):
        self.service = service
        self.protocol = MQTTListener

    def publish(self, topic, message):
        if self.protocol != MQTTListener:
            #log.msg('SEND Topic: %s, Message: %s' % (topic, message ))
            self.protocol.publish(topic, message)

    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        self.protocol = p
        log.msg("protocol build")
        return p

def PostFiglet():
    #log.msg('SEND Topic: %s, Message: %s' % (topic, message ))
    x = random.random()
    mqttFactory.publish('test/random', str(x)+' random')
#===============================================================================
#    mqttFactory.FigletPublish('tokudu/figlet', '''
# ... o   o  o-o  o-O-o o-O-o      o-o                       o  o
# ... |\ /| o   o   |     |        |                         |  |            
# ... | O | |   |   |     |       -O- o-o o-o     o-o  o  o -o- O--o o-o o-o  
# ... |   | o   O   |     |        |  | | |       |  | |  |  |  |  | | | |  |
# ... o   o  o-O\   o     o        o  o-o o       O-o  o--O  o  o  o o-o o  o 
# ...                                             |       |                  
# ...                                             o    o--o                   
# ...  o                  o         o 
# ...  |           o      |         | 
# ... -o- o   o   o  o-o -o- o-o  o-O 
# ...  |   \ / \ / |  \   |  |-' |  | 
# ...  o    o   o  | o-o  o  o-o  o-o 
# ''' )
#===============================================================================


if __name__ == '__main__':
    # TODO
    # * twisted logging instead
    log.startLogging(sys.stdout)  
    mqttFactory = MQTTListenerFactory()
    reactor.connectTCP("192.168.42.60", 1883, mqttFactory)
    #reactor.listenTCP(1025, )
    figlet = LoopingCall(PostFiglet)
    figlet.start(5)
    reactor.run()
