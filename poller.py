from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend
from btlewrap.base import BluetoothBackendException
from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from jinja2 import Environment, FileSystemLoader
import os, yaml
import sys


def load_config_from_file(file):
    with open(file, 'r') as f:
        return yaml.safe_load(f)


def get_miflora_data_dict(plant_name, poller):
    datadict = dict()
    try:
        datadict['plant'] = plant_name
        datadict['firmware'] = poller.firmware_version()
        datadict['name'] = poller.name()
        datadict['temperature'] = poller.parameter_value(MI_TEMPERATURE)
        datadict['moisture'] = poller.parameter_value(MI_MOISTURE)
        datadict['light'] = poller.parameter_value(MI_LIGHT)
        datadict['conductivity'] = poller.parameter_value(MI_CONDUCTIVITY)
        datadict['battery'] = poller.parameter_value(MI_BATTERY)
    except BluetoothBackendException as e:
        datadict['data'] = 'no data'
    return datadict


if __name__ == "__main__":
    configuration = load_config_from_file("{}/{}".format("/home/pi", "floral-config.yaml"))
    sensors = configuration.get("sensors")
    sensory_data_array = []
    
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment( loader = FileSystemLoader(templates_dir) )
    template = env.get_template('index.html')

    for sensor in sensors:
        bluetooth_mac_adress = sensor.get('bluetooth_mac_address')
        sensor_name = sensor.get('name')
        plant = sensor.get('plant')
        print("Trying to connect to " + str(sensor_name) + " with MAC " +str(bluetooth_mac_adress) + " on plant " + plant)
        poller = MiFloraPoller(bluetooth_mac_adress, BluepyBackend)
        miflora_data_dict = get_miflora_data_dict(plant, poller)
        if 'firmware' in miflora_data_dict:
            sensory_data_array.append(miflora_data_dict)
            print(str(sensor_name) + " meldet eine Feuchtigkeit von " + str(miflora_data_dict['moisture']) +u"% sowie einen N??hrstoffgehalt von " + str(miflora_data_dict['conductivity']) + "uS/cm")
    
    filename = os.path.join('/var', 'www', 'html', 'dashboard', 'index.html')
    with open(filename, 'w') as fh:
        fh.write(template.render(plantsensors = sensory_data_array))
    