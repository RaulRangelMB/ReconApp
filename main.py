import os

from modules.portscanner import run_port_scanner
from modules.auxx.colors import colors
from modules.whoislookup import whois_lookup
from modules.dnsenumeration import dns_enumeration
from modules.wapiti import wapiti_scan
from modules.subdomainscan import subdomain_scan

inputs = {'1': run_port_scanner, '2': whois_lookup, '3': dns_enumeration, '4': wapiti_scan, '5': subdomain_scan}

while True:
    print(colors.fg.cyan + "1. Port Scanner")
    print("2. Whois Lookup")
    print("3. DNS Enumeration")
    print("4. Wapiti Web Scanner")
    print("5. Subdomain Scanner")
    print("6. Exit")
    choice = input("Enter your choice: " + colors.fg.blue)

    if choice in ['6', 'exit', 'quit']:
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
