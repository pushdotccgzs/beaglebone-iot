# python twisted MQTT #

working example with MQTT for python twisted. Example is connecting to mosquitto test server.
http://test.mosquitto.org

```
from twisted.python import log
from twisted.application.service import Service
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from MQTT import MQTTProtocol

import sys
log.startLogging(sys.stdout)

class MQTTListener(MQTTProtocol):
    pingPeriod = 60000

    def connectionMade(self):
        log.msg('MQTT Connected')
        self.connect("TwistedMQTT", keepalive=self.pingPeriod)
        # TODO: make these constants configurable
        reactor.callLater(self.pingPeriod//1000, self.pingreq)
        reactor.callLater(5, self.processMessages)

    def pingrespReceived(self):
        log.msg('Ping received from MQTT broker')
        reactor.callLater(self.pingPeriod//1000, self.pingreq)

    def connackReceived(self, status):
        if status == 0:
            self.subscribe("#")
        else:
            log.msg('Connecting to MQTT broker failed')

    def processMessages(self):
        #log.msg(self)
        reactor.callLater(5, self.processMessages)

    def publishReceived(self, topic, message, qos, dup, retain, messageId):
        # Received a publish on an output topic
        log.msg('RECV Topic: %s, Message: %s' % (topic, message))
        #mqttMessageBuffer.append((topic, message))

class MQTTListenerFactory(ClientFactory):
    protocol = MQTTListener

    def __init__(self, service = None):
        self.service = service

mqttMessageBuffer = []
mqttFactory = MQTTListenerFactory()

if __name__ == '__main__':
    reactor.connectTCP("test.mosquitto.org", 1883, mqttFactory)
    #reactor.listenTCP(1025, )
    reactor.run()
```