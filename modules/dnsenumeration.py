import dns.resolver
from .colors import colors

def query_record(domain, record_type):
    print(colors.fg.blue + f"\n{record_type}" + colors.fg.cyan + f" records for " + colors.fg.blue + f"{domain}")
    
    try:
        answers = dns.resolver.resolve(domain, record_type)
        for rdata in answers:
            print(colors.fg.yellow + format_rdata(rdata, record_type))
    except dns.resolver.NoAnswer:
        print(colors.fg.red + "No response for this record type.")
    except dns.resolver.NXDOMAIN:
        print(colors.fg.red + "Domain not found.")
        return -1
    except Exception as e:
        print(colors.fg.red + f"Error: {str(e)}")

    return True

def format_rdata(rdata, record_type):
    try:
        if record_type == "A":
            return f"IPv4 Address: {rdata.address}"
        elif record_type == "AAAA":
            return f"IPv6 Address: {rdata.address}"
        elif record_type == "MX":
            return f"Mail Server: {rdata.exchange} (Priority: {rdata.preference})"
        elif record_type == "NS":
            return f"Name Server: {rdata.target}"
        elif record_type == "TXT":
            return f'TXT Record: {" ".join([t.decode("utf-8") if isinstance(t, bytes) else str(t) for t in rdata.strings])}'
        elif record_type == "CNAME":
            return f"CNAME: {rdata.target}"
        elif record_type == "SOA":
            return f"Primary NS: {rdata.mname} | Responsible: {rdata.rname} | Serial: {rdata.serial}"
        else:
            return str(rdata)
    except Exception as e:
        return f"Could not parse record: {str(e)}"

def dns_enumeration():
    print(colors.fg.yellow + "\nLoading DNS Enumeration..." + colors.reset)
    record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA']
    print(colors.fg.yellow + "Record types: " + ', '.join(record_types))

    domain = input(colors.fg.cyan + "\nEnter the target domain: " + colors.fg.blue)

    for record_type in record_types:
        success = query_record(domain, record_type)
        if not success:
            break

    print(colors.reset)