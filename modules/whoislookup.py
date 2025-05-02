import whois
from .colors import colors

def whois_lookup():
    domain = input(colors.fg.cyan + "Digite o domínio: " + colors.fg.blue)
    try:
        w = whois.whois(domain)

        print(colors.fg.green + "============= RESULTS =============" + colors.reset)

        for k, v in w.items():
            if v:
                print(colors.fg.cyan + f"{k}: " + colors.reset, end='')
                if isinstance(v, list):
                    print(colors.fg.yellow + ', '.join(v) + colors.reset)
                else:
                    print(colors.fg.yellow + str(v) + colors.reset)

    except Exception as e:
        return {'Error': {e}}