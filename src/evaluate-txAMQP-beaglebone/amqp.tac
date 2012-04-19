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

application = service.Application("statusbot")

##################################
# AMQP stuff.
##################################
AMQP_HOST="localhost"
AMQP_PORT=5672
AMQP_VHOST='/'
AMQP_USER="guest"
AMQP_PASSWORD="guest"
# Get this file out of the txamqp distribution.
AMQP_SPEC="specs/rabbitmq/amqp0-8.stripped.rabbitmq.xml"

def write_message(amqp):
    amqp.send_message(exchange="tobot", routing_key="key", msg="11111")
    #amqp.send_message(exchange="testbot", routing_key="key", msg="22222")
    #amqp.send_message(exchange="testbot2", routing_key="key", msg="33333")
    #amqp.send_message(exchange="toweb", routing_key="key", msg="33333")

    reactor.callLater(0.001, write_message, amqp)

def my_callback(msg):
    # print "Callback received: ", msg
    pass

amqp = AmqpFactory(host=AMQP_HOST, port=AMQP_PORT, vhost=AMQP_VHOST, user=AMQP_USER, password=AMQP_PASSWORD, spec_file=AMQP_SPEC)

amqp.read(exchange='tobot', routing_key='key', callback=my_callback)
#amqp.read(exchange='testbot', routing_key='key', callback=my_callback)
#amqp.read(exchange='testbot2', routing_key='key', callback=my_callback)
#amqp.read(exchange='toweb', routing_key='key', callback=my_callback)

reactor.callLater(1, write_message, amqp)

