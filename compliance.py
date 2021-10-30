from napalm import get_network_driver
from colors import bcolors
from os.path import exists
import pprint


def display_compliance_info(output):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(output)


def main():

    devices = [
        {'name': 'router-A', 'host': '192.168.86.201'},
        {'name': 'router-B', 'host': '192.168.86.202'},
        {'name': 'router-C', 'host': '192.168.86.203'},
    ]

    driver = get_network_driver("eos")

    for device in devices:
        with driver(device['host'], 'admin', 'test') as active_device:
            compliance_file = f"compliance/{device['name']}.yml"
            if exists(compliance_file):
                result = active_device.compliance_report(compliance_file)
                display_compliance_info(result)


if __name__ == "__main__":
    main()
