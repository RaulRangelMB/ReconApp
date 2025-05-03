import socket
import concurrent.futures
from .colors import colors

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "webmail", "admin", "blog", 
    "dev", "api", "test", "stage", "git", "gitlab", "github",
    "portal", "vpn", "cloud", "mobile", "app", "cdn", "media",
    "shop", "store", "secure", "support", "help", "docs",
    "wiki", "login", "m", "status", "beta", "dashboard", "static",
    "news", "images", "files", "upload", "download", "forum", 
    "intranet", "db", "search", "home", "office"
]

def resolve_subdomain(sub, domain):
    full_domain = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        return full_domain, ip
    except socket.gaierror:
        return None

def subdomain_scan():
    print(colors.fg.yellow + "Loading Subdomain Scanner...\n")

    print("Subdomains to scan: " + ', '.join(COMMON_SUBDOMAINS) + '.\n')

    domain = input(colors.fg.cyan + "Enter the target domain (e.g., example.com): " + colors.fg.blue)

    print(colors.fg.yellow + "\nScanning for common subdomains...\n" + colors.reset)

    found = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(resolve_subdomain, sub, domain) for sub in COMMON_SUBDOMAINS]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                full_domain, ip = result
                print(colors.fg.green + f"Found: {full_domain} -> {ip}" + colors.reset)
                found.append(result)

    if not found:
        print(colors.fg.red + "No subdomains found." + colors.reset)
    else:
        print(colors.fg.green + "\n============= RESULTS =============")
        print(colors.fg.cyan + f"Total found: " + colors.fg.yellow + f"{len(found)}")
        for subdomain, ip in found:
            print(colors.fg.cyan + f"{subdomain} -> " + colors.fg.yellow + f"{ip}" + colors.reset)