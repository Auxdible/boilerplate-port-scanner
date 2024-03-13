import socket
import re
import common_ports
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)

def is_ip(ip):
    try:
        socket.gethostbyaddr(ip)
        return True
    except socket.herror:
        return False

def get_open_ports(target, port_range, verbose = False):
    is_hostname = re.match(r"^[a-zA-Z0-9]+([.-][a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$", target)
    try:
        host, aliases, ip = socket.gethostbyaddr(target) if is_ip(target) else socket.gethostbyname_ex(target)
        ports = filter(lambda x: x in range(port_range[0], port_range[-1]+1), common_ports.ports_and_services)
        open_ports = [port for port in ports if s.connect_ex((host, port))]
        
        if verbose:
            return f'Open ports for {host}{f' ({ip[0]})' if host != ip[0] else ''}\nPORT     SERVICE\n{"\n".join([f'{str(port).ljust(4)}     {common_ports.ports_and_services[port]}' for port in open_ports])}'
        
        return open_ports
    except socket.gaierror:
        if is_hostname:
            return "Error: Invalid hostname"
        else:
            return "Error: Invalid IP address"