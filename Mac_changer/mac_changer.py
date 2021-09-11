#!/usr/bin/env python
import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface that you want to change")
    parser.add_option("-m", "--mac", dest="new_mac", help="MAC that u want to change")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("\n[-]Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("\n[-]Please specify a new mac, use --help for more info")
    return parser.parse_args()


def mac_changer(interface, new_mac):
    print("[+]Changing MAC for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig",interface])
    mac_adress_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if not mac_adress_search_result:
        print("[-]Could not read interface MAC adress")
    else:
        return mac_adress_search_result.group(0)

(options,arguments) = get_arguments()
current_mac = get_current_mac(options.interface)

mac_changer(options.interface, options.new_mac)

if current_mac == options.new_mac:
    print("[+]Mac adress was successfully changed to " + current_mac)
else:
    print("[-]Mac adress didnt get change")
