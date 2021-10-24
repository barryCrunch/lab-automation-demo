from napalm import get_network_driver
from colors import bcolors

def main():
    devices = [
        {'name': 'router-A', 'host': '192.168.86.201'},
        {'name': 'router-B', 'host': '192.168.86.202'},
        {'name': 'router-C', 'host': '192.168.86.203'},
    ]


    print(f"{bcolors.HEADER}******************************************************************{bcolors.ENDC}")
    for device in devices:
        driver = get_network_driver('eos')
        active_device = driver(device['host'], 'admin', 'test')
        print(f"Connectiong to {device['name']}...")
        active_device.open()
        print("Loading configuration...")
        active_device.load_replace_candidate(filename=f"configurations/{device['name']}.conf")
        compare_result = active_device.compare_config()
        if compare_result == '':
            print(f"{bcolors.OKGREEN}<<<<<<<<<<<<<NO CHANGES>>>>>>>>>>>>{bcolors.ENDC}")
            active_device.discard_config()
        else:
            print("Configuration changes....\n")
            print(compare_result)
            active_device.commit_config()
            print("Commiting configuration....")
            print(f"{bcolors.OKGREEN}COMPLETED{bcolors.ENDC}")
        active_device.close()
        print(f"\n\n{bcolors.HEADER}******************************************************************{bcolors.ENDC}")

if __name__ == "__main__":
    main()




