import os
import subprocess
from datetime import datetime
from .auxx.colors import colors

def wapiti_scan():
    print(colors.fg.yellow + "\nLoading Wapiti Web Scanner...\n")
    target = input(colors.fg.cyan + "Enter the target URL: " + colors.fg.blue)
    
    print(colors.fg.cyan + "\nHow do you want to run Wapiti?")
    print("1. Native (installed directly on this system)")
    print("2. WSL (Windows Subsystem for Linux)")
    option = input(colors.fg.cyan + "Enter your choice: " + colors.fg.blue)

    output_dir = os.path.join(os.path.dirname(__file__), '../outputs')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"wapiti_scan_{timestamp}.json")

    command = ['wapiti', '-u', target, '--flush-session', '-o', output_file] if option == '1' else ['wsl', 'wapiti', '-u', target, '--flush-session', '-o', output_file]
    ran = False

    try:
        print(colors.fg.yellow + f"\nStarting Wapiti scan. Output will be saved in {output_file}\n" + colors.reset)
        subprocess.run(command, check=True)
        ran = True
    except FileNotFoundError:
        if option == '2':
            print(colors.fg.red + "WSL or Wapiti not found in your WSL environment." + colors.reset)
        else:
            print(colors.fg.red + "Wapiti not installed or not in PATH." + colors.reset)
    except Exception as e:
        print(colors.fg.red + f"Error: {e}" + colors.reset)

    if ran:
        print(colors.fg.green + "\nWapiti scan completed.\nCheck the results in the 'outputs' folder in the root directory of ReconApp or in Wapiti's original output folder." + colors.reset)
    else:
        print(colors.fg.red + "\nWapiti scan failed.\nPlease check the error message above.\nAlso check if the domain you entered is correct (maybe you forgot http:// or https://).")
