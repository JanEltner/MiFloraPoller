from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend
from btlewrap.base import BluetoothBackendException
from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
import os, yaml

import sys

def load_config(file):
    with open(file, 'r') as f:
        return yaml.safe_load(f)

def get_miflora_data_dict(poller):
    d = dict()
    try:
        d['firmware'] = poller.firmware_version()
        d['name'] = poller.name()
        d['temperature'] = poller.parameter_value(MI_TEMPERATURE)
        d['moisture'] = poller.parameter_value(MI_MOISTURE)
        d['light'] = poller.parameter_value(MI_LIGHT)
        d['conductivity'] = poller.parameter_value(MI_CONDUCTIVITY)
        d['battery'] = poller.parameter_value(MI_BATTERY)
    except BluetoothBackendException as e:
        d['data'] = 'no data'
    return d



if __name__ == "__main__":
    configuration = load_config("{}/{}".format("/home/pi", "floral-config.yaml"))

    sensors = configuration.get("sensors")
    bt_mac = sensors[1].get('bluetooth_mac_address')
    poller = MiFloraPoller(bt_mac, BluepyBackend)
    miflora_data_dict = get_miflora_data_dict(poller)
    print(miflora_data_dict['moisture'])