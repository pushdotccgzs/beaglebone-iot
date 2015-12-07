# What is RabbitMQ? #
  * Robust messaging for applications
  * Easy to use
  * Runs on all major operating systems
  * Supports a huge number of developer platforms
  * Open source and commercially supported

see http://rabbitmq.com

# Terminology #

There are some concepts you should be familiar with before starting:

### Publishers ###

Publishers sends messages to an exchange.

### Exchanges ###

Messages are sent to exchanges. Exchanges are named and can be configured to use one of several routing algorithms. The exchange routes the messages to consumers by matching the routing key in the message with the routing key the consumer provides when binding to the exchange.

### Consumers ###

Consumers declares a queue, binds it to a exchange and receives messages from it.

### Queues ###

Queues receive messages sent to exchanges. The queues are declared by consumers.

### Routing keys ###

Every message has a routing key. The interpretation of the routing key depends on the exchange type. There are four default exchange types defined by the AMQP standard, and vendors can define custom types (so see your vendors manual for details).

These are the default exchange types defined by AMQP/0.8:

**Direct exchange**

Matches if the routing key property of the message and the routing\_key attribute of the consumer are identical.

**Fan-out exchange**

Always matches, even if the binding does not have a routing key.

**Topic exchange**

Matches the routing key property of the message by a primitive pattern matching scheme. The message routing key then consists of words separated by dots (".", like domain names), and two special characters are available; star ("**") and hash ("#"). The star matches any word, and the hash matches zero or more words. For example "**.stock.#" matches the routing keys "usd.stock" and "eur.stock.db" but not "stock.nasdaq".