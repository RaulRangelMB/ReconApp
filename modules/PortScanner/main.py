import socket
from scapy.all import srp, ARP, Ether

from .auxx.colors import colors
from .auxx.WKP import WKP_TCP, WKP_UDP
from .auxx.WKP_filtered import WKP_TCP_FILTERED, WKP_UDP_FILTERED

def banner_grabbing(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((target, port))
        banner = s.recv(1024).decode().strip()
        s.close()

        if banner:
            print(colors.fg.yellow + f"Banner from {target}:{port}" + colors.reset)
            print(colors.fg.green + f"{banner}" + colors.reset)
            return banner
        else:
            print(colors.fg.red + f"No banner received from {target}:{port}" + colors.reset)
            return None

    except Exception as e:
        print(colors.fg.red + f"Error scanning banner from {target}:{port} -> {str(e)}" + colors.reset)
        return None

def scan_network(network):
    if '/' not in network:
        print(colors.fg.red + "Invalid network format. Please use CIDR notation.\n" + colors.reset)
        return
    
    print(colors.fg.yellow + f"Scanning LAN: {network}" + colors.reset)
    print()
    arp_request = ARP(pdst=network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    answered, _ = srp(packet, timeout=2, verbose=False)

    for sent, received in answered:
        print(colors.fg.yellow + f"IP: {received.psrc} - MAC: {received.hwsrc}" + colors.reset)
    print()

def scan_range(port_range, scan_target, scan_type):

    print(colors.fg.yellow + f"Starting Scan...\n" + colors.reset)

    WKP = WKP_TCP if scan_type == "TCP" else WKP_UDP

    tries = 0
    open_ports = []
    banners = []
    
    for port in port_range:

        if scan_type == "TCP":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            WKP = WKP_TCP
            s.settimeout(1.0)

            try:
                tries += 1
                result = s.connect_ex((scan_target, port))
                name = WKP.get(scan_type + "-" + str(port), None)

                if result == 0:
                    banners.append(banner_grabbing(scan_target, port))
                    state = "open"
                    open_ports.append(port)
                else:
                    state = "closed"
            
            except socket.timeout:
                print(colors.fg.red + f"Timeout while scanning port {port}." + colors.reset)
                state = "filtered"
            
            except ConnectionRefusedError:
                state = "closed"
            
            finally:
                s.close()
        
        elif scan_type == "UDP":
            WKP = WKP_UDP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(2.0)
            name = WKP.get(scan_type + "-" + str(port), None)
            tries += 1
            try:
                s.sendto(b"\x00", (scan_target, port))
                data, _ = s.recvfrom(1024)
                state = "open"
                open_ports.append(port)
            except socket.timeout:
                state = "filtered"
            except ConnectionRefusedError:
                state = "closed"
            finally:
                s.close()

        port_info = f"{port} - {name}" if name else f"{port}"

        if state == "open":
            print(colors.fg.green + f"Port {port_info} is {state}!" + colors.reset)
        elif state == "filtered":
            print(colors.fg.red + f"Port {port_info} was {state}." + colors.reset)
        else:
            print(colors.fg.red + f"Port {port_info} is {state}." + colors.reset)

    print(colors.fg.yellow + "\nSummary:\n" + colors.reset)

    for port in open_ports:
        name = WKP.get(scan_type + "-" + str(port), None)
        port_info = f"{port} ({name})" if name else f"{port}"
        print(colors.fg.green + f"Port {port_info} is open!" + colors.reset)
    
    print(colors.fg.red + f"\nA total of {tries - len(open_ports)}/{tries} ports were closed/filtered.\n" + colors.reset)

    found_banner = False

    for banner in banners:
        if banner is not None:
            found_banner = True
            print(colors.fg.yellow + f"Banner: {banner}" + colors.reset)
            print()
            break

    if not found_banner:
        print(colors.fg.red + "No banners received." + colors.reset)

def scan_WKP(scan_target, scan_type, filtered=False):
    print(colors.fg.yellow + f"Starting Scan...\n" + colors.reset)

    WKP = (WKP_TCP if not filtered else WKP_TCP_FILTERED) if scan_type == "TCP" else (WKP_UDP if not filtered else WKP_UDP_FILTERED)

    open_ports = []
    banners = []
    tries = 0

    for port, name in WKP.items():
        port = int(port.split("-")[-1])

        if scan_type == "TCP":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            try:
                tries += 1
                result = s.connect_ex((scan_target, port))
                if result == 0:
                    banners.append(banner_grabbing(scan_target, port))
                    state = "open"
                    open_ports.append(port)
                else:
                    state = "closed"
            except socket.timeout:
                state = "filtered"
            except ConnectionRefusedError:
                state = "closed"
            finally:
                s.close()

        elif scan_type == "UDP":
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(2.0)
            tries += 1
            try:
                s.sendto(b"\x00", (scan_target, port))
                data, _ = s.recvfrom(1024)
                state = "open"
                open_ports.append(port)
            except socket.timeout:
                state = "filtered"
            except ConnectionRefusedError:
                state = "closed"
            finally:
                s.close()

        if state == "open":
            print(colors.fg.green + f"Port {port} - {name} is {state}!" + colors.reset)
        elif state == "filtered":
            print(colors.fg.red + f"Port {port} - {name} was {state}." + colors.reset)
        else:
            print(colors.fg.red + f"Port {port} - {name} is {state}." + colors.reset)

    print(colors.fg.yellow + "\nSummary:\n" + colors.reset)

    for port in open_ports:
        name = WKP.get(scan_type + "-" + str(port), None)
        port_info = f"{port} ({name})" if name else f"{port}"
        print(colors.fg.green + f"Port {port_info} is open!" + colors.reset)

    print(colors.fg.red + f"\nA total of {tries - len(open_ports)}/{tries} ports were closed/filtered.\n" + colors.reset)

    found_banner = False
    for banner in banners:
        if banner is not None:
            found_banner = True
            print(colors.fg.yellow + f"Banner: {banner}" + colors.reset)
            print()
            break

    if not found_banner:
        print(colors.fg.red + "No banners received." + colors.reset)


def run_port_scanner():
    print(colors.fg.yellow + "\nWelcome to Raul Rangel's Port Scanner!\n" + colors.reset)

    operating = True

    while operating:
        choice_host_network = '-1'
        while choice_host_network not in ['1', '2']:
            print(colors.fg.lightblue + "\n============================== Host Or Network ==============================" + colors.reset)
            choice_host_network = input(colors.fg.cyan + "1. Host\n2. Network (requires admin priviledges)\nEnter choice between Host or Network: " + colors.reset)
            print()

            if choice_host_network == '1':
                print(colors.fg.lightblue + "\n============================== Scan Target ==============================" + colors.reset)
                scan_target = "-1"
                while scan_target == "-1":
                    scan_target = input(colors.fg.cyan + "Enter the target to scan: " + colors.reset)
                    print()

                    try:
                        scan_target = socket.gethostbyname(scan_target)
                    except:
                        print(colors.fg.red + "Invalid scan target.\n" + colors.reset)
                        scan_target = "-1"                    

                print(colors.fg.yellow + f"\nScanning target: {scan_target}\n" + colors.reset)

                choice_scan_type = '-1'
                choice_scan_method = '-1'

                while choice_scan_type not in ['1', '2']:
                    print(colors.fg.lightblue + "\n============================== Scan Type ==============================" + colors.reset)
                    choice_scan_type = input(colors.fg.cyan + "1. TCP\n2. UDP\nEnter the type of scan: " + colors.reset)
                    print()
                    if choice_scan_type == '1':
                        scan_type = "TCP"
                    elif choice_scan_type == '2':
                        scan_type = "UDP"
                    else:
                        print(colors.fg.red + "Invalid scan type.\n" + colors.reset)

                    while choice_scan_method not in ['1', '2', '3'] and choice_scan_type in ['1', '2']:
                        print(colors.fg.yellow + f"Scanning type chosen: {scan_type}\n" + colors.reset)
                        print(colors.fg.lightblue + "\n============================== Scan Method ==============================" + colors.reset)
                        choice_scan_method = input(colors.fg.cyan + "1. Custom Port Range Scan\n2. Well Known Ports Scan (~3265 entries)\n3. Most Well Known Ports Scan (~20 entries)\nEnter the type of scan: " + colors.reset)
                        print()

                        if choice_scan_method == '1':
                            valid_input = False
                            while not valid_input:
                                try:
                                    port_range_input = input(colors.fg.cyan + "\nEnter the port range to scan \nFormat: x-y (x -> start, y -> end): " + colors.reset)
                                    print()
                                    port_range = port_range_input.split("-")
                                    if len(port_range) != 2:
                                        raise ValueError("Incorrect format. Please use 'x-y'.")
                                    
                                    start_port, end_port = int(port_range[0]), int(port_range[1])

                                    if start_port > end_port:
                                        raise ValueError("Start port cannot be greater than end port.")
                                    
                                    port_range = range(start_port, end_port + 1)
                                    scan_range(port_range, scan_target, scan_type)
                                    valid_input = True 
                                except ValueError as e:
                                    print(colors.fg.red + f"Invalid input: {e}. Please try again." + colors.reset)
                        elif choice_scan_method == '2':
                            scan_WKP(scan_target, scan_type)
                        elif choice_scan_method == '3':
                            scan_WKP(scan_target, scan_type, filtered=True)
                        else:
                            print(colors.fg.red + "Invalid choice.\n" + colors.reset)
            
            elif choice_host_network == '2':
                print(colors.fg.lightblue + "\n============================== Scan Network ==============================" + colors.reset)
                
                network = "-1"
                while network == "-1":
                    network = input(colors.fg.cyan + "Enter the network to scan: " + colors.reset)
                    print()

                    try:
                        scan_network(network)
                    except:
                        print(colors.fg.red + "Invalid scan target.\n" + colors.reset)
                        network = "-1"
                

        choice_continue = '-1'
        while choice_continue not in ['1', '2']:
            print(colors.fg.lightblue + "\n============================== Continue or Exit ==============================" + colors.reset)
            choice_continue = input(colors.fg.cyan + "1. Continue\n2. Exit\nEnter your choice: " + colors.reset)
            print()
            if choice_continue == '2':
                operating = False
            elif choice_continue == '1':
                choice_scan_type = '-1'
                choice_scan_method = '-1'
            else:
                print(colors.fg.red + "Invalid choice.\n" + colors.reset)

    print(colors.fg.yellow + "Exiting..." + colors.reset)
    print()

if __name__ == "__main__":
    run_port_scanner()