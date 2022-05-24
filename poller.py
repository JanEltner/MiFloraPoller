from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend

import sys

php_param = sys.argv[1]
poller = MiFloraPoller(php_param, BluepyBackend)

from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY

print("\"{}\"".format(poller.firmware_version()))
print("\"{}\"".format(poller.name()))
print("\"{}\"".format(poller.parameter_value(MI_TEMPERATURE)))
print("\"{}\"".format(poller.parameter_value(MI_MOISTURE)))
print("\"{}\"".format(poller.parameter_value(MI_LIGHT)))
print("\"{}\"".format(poller.parameter_value(MI_CONDUCTIVITY)))
print("\"{}\"".format(poller.parameter_value(MI_BATTERY)))
