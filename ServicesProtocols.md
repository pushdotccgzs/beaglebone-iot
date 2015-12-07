![https://lh3.googleusercontent.com/-xHVUmTBwahM/T5xX0tyUxCI/AAAAAAAAANs/XnT8XQkCdwo/s800/SERVER-HUB-CLIENT-relations.png](https://lh3.googleusercontent.com/-xHVUmTBwahM/T5xX0tyUxCI/AAAAAAAAANs/XnT8XQkCdwo/s800/SERVER-HUB-CLIENT-relations.png)

# Introduction #

Bird view of central services and protocols. Central for all real time communication is RabbitMQ with a AMQP protocol. The HUB stays connected all the time and updates continuously status changes of devices. authentication encryption etc will be described separate in detail. The user can access his installation through a web browser from outside. The website is served by django (login, user context, static content) real time data is served separate through ajax and socket.io wich connects by tornadoio2 on the server to the RabbitMQ AMQP broker.


# Details #

## RabbitMQ ##
  * delivers real time communication
  * organises pubsub content in a topic structur
  * every HUB has its own "vhost" to isolate each other from another
  * could be seen as a _**model**_ in the sense of MVC architecture

## tornadio2 ##
  * provides an server side interface for client socketio
  * translates between MQTT broker and webbrowser through socketio (gateway service)
  * could be seen as _**controller**_ in the sense of an MVC architecture

## django ##
  * provides user context and static content
  * delivers authentfication (oauth) for other services
  * could be seen as _**view**_ in the sense of an MVC architecture