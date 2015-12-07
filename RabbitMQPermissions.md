# Introduction #

Some first thoughts howto handle permissions with rabbitMQ:
  * create an account for each beaglebone
  * each beaglebone has its own vhost
  * beagleboard has configure permission (declares exchanges and queues)
  * consumers have read write permission
  * use ssl later unique certificate for every beaglebone
  * there is a CLI tool **rabbitmqctl** where the webserver could create users and permissions on demand (CRUD pattern to implement, have also some oauth pattern in mind)

# Details #

RabbitMQ distinguishes between configure, write and read operations on a resource. The configure operations create or destroy resources, or alter their behaviour. The write operations inject messages into a resource. And the read operations retrieve messages from a resource.

In order to perform an operation on a resource the user must have been granted the appropriate permissions for it. The following table shows what permissions on what type of resource are required for all the AMQP commands which perform permission checks.

| AMQP command | configure | write | read |
|:-------------|:----------|:------|:-----|
| exchange.declare (passive=false) | exchange  |       |      |
| exchange.delete | exchange  |       |      |
| queue.declare (passive=false) | queue     |       |      |
| queue.delete | queue     |       |      |
| exchange.bind |           | exchange (destination) | exchange (source) |
| exchange.unbind |           | exchange (destination) | exchange (source) |
| queue.bind   |           | queue | exchange |
| queue.unbind |           | queue | exchange |
| basic.publish |           | exchange |      |
| basic.get    |           |       | queue |
| basic.consume |           |       | queue |
| queue.purge  |           |       | queue |

Permissions are expressed as a triple of regular expressions - one each for configure, write and read - on per-vhost basis. The user is granted the respective permission for operations on all resources with names matching the regular expressions. (Note: For convenience RabbitMQ maps AMQP's default exchange's blank name to 'amq.default' when performing permission checks.)


# see #
  * http://www.rabbitmq.com/access-control.html
  * http://www.rabbitmq.com/man/rabbitmqctl.1.man.html