import os

from modules.auxx.colors import colors
from modules.portscanner import run_port_scanner
from modules.whoislookup import whois_lookup
from modules.dnsenumeration import dns_enumeration
from modules.whatweb import whatweb_scan
from modules.subdomainscan import subdomain_scan
from modules.wapiti import wapiti_scan

inputs = {'1': run_port_scanner, '2': whois_lookup, '3': dns_enumeration, '4': whatweb_scan, '5': subdomain_scan, '6': wapiti_scan}

while True:
    print(colors.fg.cyan + "\nWelcome to Raul Rangel's ReconApp!\n")
    print("1. Port Scan")
    print("2. Whois Lookup")
    print("3. DNS Enumeration")
    print("4. WhatWeb Scan")
    print("5. Subdomain Scan")
    print("6. Wapiti Web Scan")
    print("7. Exit")
    choice = input("Enter your choice: " + colors.fg.blue)

    if choice in ['7', 'exit', 'quit']:
        print(colors.fg.yellow + "\nExiting..." + colors.reset)
        print()
        break
    elif choice in inputs:
        inputs[choice]()
    else:
        print(colors.fg.red + "\nInvalid choice.")
    
    continue_choice = input(colors.fg.cyan + "\nDo you wish to continue using ReconApp?\n1. Continue\n2. Exit\nEnter your choice: " + colors.fg.blue)
    if continue_choice.lower() not in ['1', 'continue', 'c', 'yes', 'y']:
        os.system('cls' if os.name == 'nt' else 'clear')
        break
    
    os.system('cls' if os.name == 'nt' else 'clear')
