import subprocess
from .auxx.colors import colors

def whatweb_scan():
    print(colors.fg.yellow + "\nLoading WhatWeb Scanner...\n")
    target = input(colors.fg.cyan + "Enter the target URL: " + colors.fg.blue)

    print(colors.fg.cyan + "\nHow do you want to run WhatWeb?")
    print("1. Native (installed directly on this system)")
    print("2. WSL (Windows Subsystem for Linux)")
    option = input(colors.fg.cyan + "Enter your choice: " + colors.fg.blue)

    print(colors.fg.cyan + "\nDo you want verbose output?")
    print("1. Yes")
    print("2. No")
    verbose = input(colors.fg.cyan + "Enter your choice: " + colors.fg.blue)

    if verbose == '1':
        command = ['whatweb', '-v', target] if option == '1' else ['wsl', 'whatweb', '-v', target]
    else:
        command = ['whatweb', target] if option == '1' else ['wsl', 'whatweb', target]

    print(colors.fg.yellow + f"\nStarting WhatWeb scan on {target}...\n" + colors.reset)

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(colors.fg.green + "\n============= RESULTS =============")
        print(colors.fg.yellow + result.stdout + colors.reset)

        if result.stderr:
            print(colors.fg.red + "\nSome warnings/errors occurred:\n" + result.stderr + colors.reset)
    except FileNotFoundError:
        print(colors.fg.red + "WhatWeb not installed or not in PATH/WSL environment." + colors.reset)
    except Exception as e:
        print(colors.fg.red + f"Error: {e}" + colors.reset)