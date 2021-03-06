###
# amqp.tac
# .tac file for use with amqp.py.
#
# Dan Siemon <dan@coverfire.com>
# March 2010
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
##
from twisted.internet import reactor
from twisted.application import service
from twisted.words.protocols.jabber import jid

from amqp import AmqpFactory

import fcntl, socket, struct
import json

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

ETH0_MAC = str(getHwAddr('eth0'))
print( ETH0_MAC )


application = service.Application("statusbot")

##################################
# AMQP stuff.
##################################
AMQP_HOST="localhost"
AMQP_PORT=5672 
AMQP_VHOST='/vcS3dDCWxcwoGaRKL2uYpvdcviv'
AMQP_USER="uDp3GPbdahahEGBev8vaEM72xJs"
AMQP_PASSWORD="cmDvdug946QGPZvFNmSko43CSn3"
# Get this file out of the txamqp distribution.
AMQP_SPEC="specs/rabbitmq/amqp0-8.stripped.rabbitmq.xml"

def write_ping(amqp):
    amqp.send_message(exchange="messaging/", type="topic", routing_key="presence.ping", msg="CLIENT pong")
    reactor.callLater(10, write_ping, amqp)

def write_switch1(amqp):
	amqp.send_message(exchange="messaging/", type="topic", routing_key="switch.01", msg="CLIENT off")
	reactor.callLater(0.3, write_switch1, amqp)

def write_switch2(amqp):
    amqp.send_message(exchange="messaging/", type="topic", routing_key="switch.02", msg="CLIENT on")
    reactor.callLater(0.7, write_switch2, amqp)

def my_callback_ping(msg):
    print "Callback PING received: ", msg[3], msg[4], msg[5].body
    pass

def my_callback_switch(msg):
    print "Callback SWITCH received: ",  msg[3], msg[4], msg[5].body
    pass
    
def my_callback(msg):
    print "Callback received: ",  msg[3], msg[4], msg[5].body
    pass

amqp = AmqpFactory(host=AMQP_HOST, port=AMQP_PORT, vhost=AMQP_VHOST, user=AMQP_USER, password=AMQP_PASSWORD, spec_file=AMQP_SPEC)

amqp.read(exchange='messaging/', type="topic", queue="", routing_key='#', callback=my_callback)
#amqp.read(exchange='messaging/', type="topic", queue='', routing_key='presence.ping', callback=my_callback_ping)
#amqp.read(exchange='messaging/', type="topic", queue='', routing_key='switch.#', callback=my_callback_switch)


reactor.callLater(5, write_ping, amqp)
reactor.callLater(5, write_switch1, amqp)
reactor.callLater(5, write_switch2, amqp)

