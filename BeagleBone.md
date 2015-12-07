http://beagle.s3.amazonaws.com/graphics/beaglebone/beaglebone-in-hand.JPG

# Hardware #

"The BeagleBone is the low-cost, high-expansion hardware-hacker focused BeagleBoard. It is a bare-bones BeagleBoard that acts as a USB or Ethernet connected expansion companion for your current BeagleBoard and BeagleBoard-xM or works stand-alone. The BeagleBone is small even by BeagleBoard standards and with the high-performance ARM capabilities you expect from a BeagleBoard, the BeagleBone brings full-featured Linux to places it has never gone before." (see http://beagleboard.org/bone)

# Software #

I have productive experience with python-twisted integrating Open Sound Control and serial protocols

Twisted is an event-driven networking engine written in Python and licensed under the open source  MIT license.
http://twistedmatrix.com/trac/

# Protocol #

MQTT is a machine-to-machine (M2M)/"Internet of Things" connectivity protocol. It was designed as an extremely lightweight publish/subscribe messaging transport. It is useful for connections with remote locations where a small code footprint is required and/or network bandwidth is at a premium. For example, it has been used in sensors communicating to a broker via satellite link, over occasional dial-up connections with healthcare providers, and in a range of home automation and small device scenarios. It is also ideal for mobile applications because of its small size, low power usage, minimised data packets, and efficient distribution of information to one or many receivers (more...)
http://mqtt.org

### Mosquitto ###
Mosquitto is an open source (BSD licensed) message broker that implements the MQ Telemetry Transport protocol version 3.1. MQTT provides a lightweight method of carrying out messaging using a publish/subscribe model. This makes it suitable for "machine to machine" messaging such as with low power sensors or mobile devices. A good example of this is all of the work that Andy Stanford-Clark (one of the originators of MQTT) has done in home monitoring and automation with his twittering house and twittering ferry. Andy gave a talk on this at OggCamp that explains a bit about MQTT and how he uses it. The slides and audio are available online at slideshare.

http://mosquitto.org

### MQTT for Twisted Python ###

https://github.com/adamvr/MQTT-For-Twisted-Python
