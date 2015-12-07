# Introduction #

## ANgström ##
As quick as possible we need an overview of the avaiable tools for the beaglebone.
```
root@beaglebone:~# uname -a
Linux beaglebone 3.2.5+ #1 Mon Feb 13 19:22:44 CET 2012 armv7l GNU/Linux
```

## ubuntu oneiric ##
Installed ubuntu oneiric on the sd card
according to howto here: http://elinux.org/BeagleBoardUbuntu
```
root@omap:~# uname -a
Linux omap 3.2.0-psp3 #1 Tue Feb 28 06:08:20 UTC 2012 armv7l armv7l armv7l GNU/Linux
```


## cloude9 & node.js ##

## Angström ##
Version on the beaglebone 27.03.2012

```
root@beaglebone:~# node --version
v0.4.12
```
looks a bit old for me, actual version is: v0.6.14 according to webpage

## ubuntu oneiric ##
```
root@omap:~# node --version
v0.4.9
```


## python-twisted ##


## Angström ##
Have very good experience in productive installations.
situation on the beaglebone:
```
root@beaglebone:~# opkg list | grep python-twisted 
python-twisted - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-conch - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-core - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-dbg - 10.2.0-r0 - pyroot@omap:~# node --version
v0.4.9
thon-twisted version 10.2.0-r0 - Debugging files
python-twisted-dev - 10.2.0-r0 - python-twisted version 10.2.0-r0 - Development files
python-twisted-flow - 8.2.0-r0 - python-twisted version 8.2.0-r0
python-twisted-lore - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-mail - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-names - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-news - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-pair - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-protocols - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-runner - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-test - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-web - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-words - 10.2.0-r0 - python-twisted version 10.2.0-r0
python-twisted-zsh - 10.2.0-r0 - python-twisted version 10.2.0-r0
```

## ubuntu oneiric ##
```
root@omap:~# apt-cache search python-twisted
python-twisted - Event-based framework for internet applications (transitional package)
python-twisted-bin - Event-based framework for internet applications
python-twisted-bin-dbg - Event-based framework for internet applications (debug extension)
python-twisted-conch - The Twisted SSH Implementation
python-twisted-core - Event-based framework for internet applications
python-twisted-lore - Documentation generator with HTML and LaTeX support
python-twisted-mail - An SMTP, IMAP and POP protocol implementation
python-twisted-names - A DNS protocol implementation with client and server
python-twisted-news - An NNTP protocol implementation with client and server
python-twisted-runner - Process management, including an inetd server
python-twisted-runner-dbg - Process management, including an inetd server (debug extension)
python-twisted-web - An HTTP protocol implementation together with clients and servers
python-twisted-words - Chat and Instant Messaging
python-pynetsnmp - Python ctypes bindings for NET-SNMP with Twisted integration
python-twisted-calendarserver - Twisted components for Apple's Calendarserver
python-twisted-web2 - An HTTP/1.1 Server Framework
```

installed python twisted
```
apt-get install python-twisted
```

tested with simple python echo server
```
from twisted.internet import protocol, reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

reactor.listenTCP(1234, EchoFactory())
reactor.run()
```

and works
tested with netcat
```
nc 192.168.42.4 -p 1234
hello
hello
```

## virtualbox development ##
For development on the beaglebone installed a virtualbox ubuntu oneiric session including:
  * eclipse
    * pydev
    * egit
  * python-twisted
  * txosc
  * mosquitto
  * mosquitto-client

# DONE #
  * check dongle is serial device? - ordered some, installed py-openzwave
  * check network device reconnects gracefully - reconnects // rewrote mqtt code to reconnect as well
  * check node on ubuntu for beaglebone (cloud9 ide??) - dropped for now
  * research & big picture what services running where and talking which protocol

# TODO #
  * implement first code snippets