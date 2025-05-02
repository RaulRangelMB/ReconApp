import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'PortScanner'))

from modules.PortScanner.main import run_port_scanner
from modules.PortScanner.auxx.colors import colors
from modules.whoislookup import whois_lookup

while True:
    print(colors.fg.cyan + "1. PortScanner")
    print("2. Whois Lookup")
    print("3. Exit")
    choice = input("Enter your choice: " + colors.fg.blue)

    if choice == '1':
        run_port_scanner()
    elif choice == '2':
        whois_lookup()
    elif choice in ['3', 'exit', 'quit']:
        print(colors.fg.yellow + "\nExiting..." + colors.reset)
        print()
        break

    continue_choice = input(colors.fg.cyan + "\n1. Continue\n2. Exit\nEnter your choice: " + colors.fg.blue)
    if continue_choice != '1':
        print(colors.fg.yellow + "\nExiting..." + colors.reset)
        print()
        break
