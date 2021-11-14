from napalm import get_network_driver
from colors import bcolors
from os.path import exists
from os import system, name
import json


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def print_result(test_name, test_result, level):
    if test_result:
        print((" " * level) + u'\u2705' + " - " + test_name)
    else:
        print((" " * level) + u'\u274c' + " - " + test_name)


def display_compliance_info(output, level=0):
    keywords = ['extra', 'missing', 'skipped', 'complies', 'present', 'diff']
    for check, value in output.items():
        if check not in keywords:
            print_result(check, value['complies'], level)
            if 'present' in value.keys():
                display_compliance_info(value['present'], level+2)
            elif 'diff' in value.keys():
                if len(value['diff']['missing']) > 0:
                    for missing_value in value['diff']['missing']:
                        print_result(missing_value, False, level+2)
                display_compliance_info(value['diff']['present'], level+2)


def main():
    clear()

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
                print(
                    f"Checking {bcolors.HEADER}{device['name']}{bcolors.ENDC} for compliance...")
                result = active_device.compliance_report(compliance_file)
                display_compliance_info(result)
                print('\n')


if __name__ == "__main__":
    main()
