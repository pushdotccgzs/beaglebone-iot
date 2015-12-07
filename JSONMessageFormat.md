# Introduction #

All new message types added from here on will be in JSON format. It is hoped that eventually everything will be JSON, making parsing of messages easier.


# Details #

# Commands from page to hub #
The hub recognized and responds to the following commands:
> ### rescan ###
  * Format: {"command":"rescan"}
  * Function: Causes the node to report all connected zwave devices, by sending NodeLine message for each device. See NodeLine section under "Messages from hub to page".
> ### nodeOn ###
  * Format: {"command":"NodeOn", "nodeId":nodeId}
  * Turns the node with the given nodeId on. nodeId must be a number from 1 to 232.
> ### nodeOff ###
  * Format: {"command":"NodeOff", "nodeId":nodeId}
  * Turns the node with the given nodeId off. nodeId must be a number from 1 to 232.
> ### nodeLevel ###
  * Format: {"command":"NodeLevel", "nodeId":nodeId, "level", level}
  * Sets the node with nodeId to the level given by level. nodeId must be from 1 to 232 as above, and level may be from 0 to 99, or 255. The former range is a percent intensity, and the latter means "on to previous value."

# Messages from hub to page #

## Zwave messages ##
Currently, all Zwave messages are converted to JSON and sent from the hub. Later, in the interests of reducing clutter, we will probably only relay those messages of which are of interest. Only such messages of interest are listed below.

### NodeLine ###
  * Format: {"notificationType":"NodeLine", "nodeId": nodeId, "nodeType": nodeType }
  * Informs the page that a node with the given nodeId has been detected and should be added to the list of controls if it is not present already. Currently supported values for nodeType are 'Binary Scene Switch' and 'Multilevel Scene Switch'. The page will create on/off controls for both of them, and also a dimming slider for the latter.

### ValueChanged ###
  * Format: {"homeId": homeId, "valueId": {"index": 0, "units": "", "type": type, "nodeId": nodeId, "value": value, "commandClass": commandClass, "instance": instance, "readOnly": readOnly, "homeId": homeId, "label": label, "genre": genre, "id": valueId}, "notificationType": "ValueChanged", "nodeId": nodeId}
  * This is actually a raw Zwave notification that the page listens for, which is why there are a bunch of extra values in it. We don't use most of these. The important ones are nodeId and valueId.value. If the given nodeId exists in the table of nodes displayed on the page, its "value" column will be updated accordingly.