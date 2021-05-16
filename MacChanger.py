#!/usr/bin/env python

import subprocess
import optparse
import re
import sys

def GetArguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to Change it's MAC Address")
    parser.add_option("-m", "--mac", dest="newAddress", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.newAddress:
        parser.error("[-] Please specify a new MAC Address, use --help for more info")
    else:
        return options


def ChangeMac(interface, newAddress):
    print("[+] Changing MAC Address for " + interface + " to " + newAddress)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["macchanger", "-m", newAddress, interface])
    subprocess.call(["ifconfig", interface, "up"])


def GetCurrentMAC(interface):
    ifconfigResult = subprocess.check_output(["ifconfig", interface])
    MacAddressSearchResult = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfigResult)
    if MacAddressSearchResult:
        return MacAddressSearchResult.group(0)
    else:
        print("[-] Could not read MAC Address")

def CheckMAC_AddressFormat(MAC_Address):
    matched = re.match(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", MAC_Address)
    if matched is None:
        print("[-] Please Enter Correct Format of new MAC Address")
        sys.exit(1)

def DisplayFinalMessage(interface ,MAC_Address):
    currentMac = GetCurrentMAC(interface)
    if currentMac == MAC_Address:
        print("[+] MAC address was successfully changed to " + currentMac)
    else:
        print("[-] MAC address did not change")


options = GetArguments()
CheckMAC_AddressFormat(options.newAddress)
currentMac = GetCurrentMAC(options.interface)
print("Current MAC = " + str(currentMac))
ChangeMac(options.interface, options.newAddress)
DisplayFinalMessage(options.interface, options.newAddress)