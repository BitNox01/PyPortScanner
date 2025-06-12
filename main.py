import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def display_banner():
    banner = r"""
  _____           _      _____                                    ______          ____  _ _   _   _         __  
 |  __ \         | |    / ____|                                  / /  _ \        |  _ \(_) | | \ | |        \ \ 
 | |__) |__  _ __| |_  | (___   ___ __ _ _ __  _ __   ___ _ __  | || |_) |_   _  | |_) |_| |_|  \| | _____  _| |
 |  ___/ _ \| '__| __|  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__| | ||  _ <| | | | |  _ <| | __| . ` |/ _ \ \/ / |
 | |  | (_) | |  | |_   ____) | (_| (_| | | | | | | |  __/ |    | || |_) | |_| | | |_) | | |_| |\  | (_) >  <| |
 |_|   \___/|_|   \__| |_____/ \___\__,_|_| |_|_| |_|\___|_|    | ||____/ \__, | |____/|_|\__|_| \_|\___/_/\_\ |
                                                                 \_\       __/ |                            /_/ 
                                                                          |___/                                 
"""
    print(GREEN + banner + RESET)

def scan_port(ip, port, timeout=0.8):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((ip, port)) == 0
    except Exception:
        return False

def scan_host(ip, start_port, end_port, max_threads=100):
    open_ports = []
    total_ports = end_port - start_port + 1

    print(f"{CYAN}Scanning {ip} ports {start_port}-{end_port} ({total_ports} ports)...{RESET}")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}

        completed = 0
        for future in as_completed(futures):
            port = futures[future]
            completed += 1
            try:
                if future.result():
                    print(f"{GREEN}[+] Port {port} is open on {ip}{RESET}")
                    open_ports.append(port)
            except Exception:
                pass
            progress = (completed / total_ports) * 100
            sys.stdout.write(f"\rProgress: {progress:.1f}%")
            sys.stdout.flush()

    print()

    if not open_ports:
        print(f"{YELLOW}[-] No open ports found on {ip}{RESET}")
    else:
        print(f"{GREEN}[+] Total open ports on {ip}: {len(open_ports)}{RESET}")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def valid_port(port_str):
    try:
        port = int(port_str)
        if 1 <= port <= 65535:
            return port
    except ValueError:
        pass
    return None

if __name__ == "__main__":
    display_banner()

    print(f"{CYAN}Choose an option:{RESET}")
    print(f"{CYAN}[1] Scan a network range{RESET}")
    print(f"{CYAN}[2] Scan localhost{RESET}")

    while True:
        choice = input(f"{CYAN}Enter 1 or 2: {RESET}").strip()
        if choice in ['1', '2']:
            break
        else:
            print(f"{RED}Invalid input, please enter 1 or 2.{RESET}")

    try:
        if choice == '1':
            while True:
                network = input(f"{CYAN}Enter network address (e.g. 192.168.1.0/24): {RESET}").strip()
                try:
                    net = ipaddress.ip_network(network, strict=False)
                    break
                except ValueError:
                    print(f"{RED}Invalid network address format.{RESET}")

            while True:
                start_port = valid_port(input(f"{CYAN}Enter start port (1-65535): {RESET}"))
                if start_port is not None:
                    break
                print(f"{RED}Invalid port number.{RESET}")

            while True:
                end_port = valid_port(input(f"{CYAN}Enter end port (>= start port): {RESET}"))
                if end_port is not None and end_port >= start_port:
                    break
                print(f"{RED}Invalid port number or less than start port.{RESET}")

            print(f"{CYAN}Scanning {net.num_addresses - 2} hosts in network {network}...{RESET}")
            for ip in net.hosts():
                scan_host(str(ip), start_port, end_port)

        else:
            ip = get_local_ip()
            print(f"{CYAN}Local IP detected: {ip}{RESET}")

            while True:
                start_port = valid_port(input(f"{CYAN}Enter start port (1-65535): {RESET}"))
                if start_port is not None:
                    break
                print(f"{RED}Invalid port number.{RESET}")

            while True:
                end_port = valid_port(input(f"{CYAN}Enter end port (>= start port): {RESET}"))
                if end_port is not None and end_port >= start_port:
                    break
                print(f"{RED}Invalid port number or less than start port.{RESET}")

            print(f"{CYAN}Scanning localhost {ip}...{RESET}")
            scan_host(ip, start_port, end_port)

    except KeyboardInterrupt:
        print(f"\n{YELLOW}Scan interrupted by user. Thanks for using Port Scanner by BitNox!{RESET}")
    except Exception as e:
        print(f"{RED}Error occurred: {e}{RESET}")


