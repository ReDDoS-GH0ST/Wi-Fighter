import os
import sys
import re
import platform
import subprocess
from time import sleep
from termcolor import colored
from rich.console import Console
from prettytable import PrettyTable

console = Console()
table = PrettyTable()
os_system = platform.system()
commands = {
    "scan": "Scan all networks",
    "showinfo": "Show network's data",
    "help": "Print the commands",
    "--h": "Print the commands",
    "clear": "Clear the screen",
    "banner": "Print the banner",
    "quit": "Exit the program",
    "exit": "Exit the program"
}


class WiFighter:

    def progressBar(self, title):
        with console.status(colored(f"[*] {title}...", "yellow")) as st:
            sleep(2.5)

    def greeting_animation(self, text=colored("Starting the Wi-Fighter...................", "yellow"),
                           delay=0.06):
        global commands
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            sleep(delay)

        sleep(3)
        sys.stdout.write('\r')
        sys.stdout.write(' ' * len(text))
        sys.stdout.write('\r')
        sys.stdout.write(text + colored("Done\n", "yellow"))
        sys.stdout.flush()
        sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        sleep(1)

        print(colored("""
██╗    ██╗██╗      ███████╗██╗ ██████╗ ██╗  ██╗████████╗███████╗██████╗ 
██║    ██║██║      ██╔════╝██║██╔════╝ ██║  ██║╚══██╔══╝██╔════╝██╔══██╗
██║ █╗ ██║██║█████╗█████╗  ██║██║  ███╗███████║   ██║   █████╗  ██████╔╝
██║███╗██║██║╚════╝██╔══╝  ██║██║   ██║██╔══██║   ██║   ██╔══╝  ██╔══██╗
╚███╔███╔╝██║      ██║     ██║╚██████╔╝██║  ██║   ██║   ███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝      ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                        by R3DDoS_GH0$T""", "red"))

        table = PrettyTable()
        table.field_names = ["Command", "Description"]
        for cmd, desc in commands.items():
            table.add_row([cmd, desc])

        print(table, '\n')

    def scan_networks(self):
        try:
            if os_system == "Windows":
                WiFighter.progressBar(self, "Scanning networks")
                scan = subprocess.run("netsh wlan show networks mode=bssid", text=True, capture_output=True,
                                      encoding="utf-8")
                out = scan.stdout or ''
                ssids = re.findall(r"^\s*SSID\s+\d+\s*:\s*(.+?)\s*$", out, flags=re.M)
                real_ssids = [s for s in ssids if "Инфраструктура" not in s and "сеть" not in s.lower()]
                unique_networks = list(set(real_ssids))
                table.clear_rows()
                if len(unique_networks) <= 1:
                    print(colored("[+] 1 network was found!", "green"))
                    table.field_names = ['№', "Network"]
                    table.add_row(['1', unique_networks[0] if unique_networks else "None"])
                    print(table, '\n')
                else:
                    print(colored(f"[+] {len(unique_networks)} networks were found!", "green"))
                    table.field_names = ['№', "Network"]
                    for i, net in enumerate(unique_networks, start=1):
                        table.add_row([str(i), net])
                    print(table, '\n')
            elif os_system == "Linux":
                WiFighter.progressBar(self, "Scanning networks")
                scan = subprocess.run("nmcli -t -f SSID,BSSID,CHAN,SIGNAL,SECURITY dev wifi list",
                                      text=True, capture_output=True, encoding="utf-8")
                out = scan.stdout or ''
                networks = []
                for line in out.strip().split('\n'):
                    if not line:
                        continue
                    parts = line.split(':')
                    if len(parts) >= 5:
                        ssid = parts[0].strip()
                        if ssid and ssid != "--":
                            networks.append(ssid)

                unique_networks = list(set(networks))
                table.clear_rows()
                if len(unique_networks) <= 1:
                    print(colored("[+] 1 network was found!", "green"))
                    table.field_names = ['№', "Network"]
                    table.add_row(['1', unique_networks[0] if unique_networks else "None"])
                    print(table, '\n')
                else:
                    print(colored(f"[+] {len(unique_networks)} networks were found!", "green"))
                    table.field_names = ['№', "Network"]
                    for i, net in enumerate(unique_networks, start=1):
                        table.add_row([str(i), net])
                    print(table, '\n')
        except Exception as e:
            print(colored(f"[-] Something error was occurred: {e}", "red"))

    def show_WiFi_data(self, network):
        if os_system == "Windows":
            try:
                WiFighter.progressBar(self, "Extracting the network's data")

                def get_value(lines, keywords):
                    for line in lines:
                        for keyword in keywords:
                            if keyword in line and ':' in line:
                                parts = line.split(':')
                                if len(parts) > 1 and parts[1].strip():
                                    return parts[1].strip()
                    return "N/A"

                profile = subprocess.check_output(f'netsh wlan show profile "{network}" key=clear', shell=True).decode(
                    "utf-8").split('\n')

                data = {
                    "Password": get_value(profile, ["Key Content", "Содержимое ключа"]),
                    "Authentication": get_value(profile, ["Authentication", "Проверка подлинности"]),
                    "Cipher": get_value(profile, ["Cipher", "Шифр"]),
                    "Network Type": get_value(profile, ["Network type", "Тип сети"]),
                    "Radio Type": get_value(profile, ["Radio network type", "Тип радиосети"]),
                    "Type": get_value(profile, ["Type", "Тип"])
                }

                table.clear_rows()
                table.title = f"Data of the {network} network"
                table.field_names = ["Property", "Value"]
                for key, value in data.items():
                    table.add_row([key, value])
                print(table)

            except subprocess.CalledProcessError:
                print(colored("[-] Network not found or no saved profile", "red"))
            except Exception as e:
                print(colored(f"[-] Something error was occurred: {e}", "red"))
        elif os_system == "Linux":
            try:
                WiFighter.progressBar(self, "Extracting the network's data")

                list_result = subprocess.run("nmcli -t connection show",
                                             capture_output=True, text=True, shell=True, encoding='utf-8')
                saved_networks = []
                for line in list_result.stdout.strip().split('\n'):
                    if ':' in line:
                        name = line.split(':')[0].strip()
                        if name:
                            saved_networks.append(name)

                if network not in saved_networks:
                    print(colored(f"[-] Network '{network}' is not saved", "red"))
                    return

                result = subprocess.run(
                    f'nmcli -t -f 802-11-wireless-security.psk,802-11-wireless.ssid,802-11-wireless.mode,802-11-wireless-security.key-mgmt connection show "{network}"',
                    capture_output=True,
                    text=True,
                    shell=True,
                    encoding='utf-8'
                )

                if result.returncode != 0:
                    print(colored("[-] Failed to get network data", "red"))
                    return

                lines = result.stdout.strip().split('\n')
                data = {}
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if 'psk' in key.lower():
                            data["Password"] = value
                        elif 'ssid' in key.lower():
                            data["SSID"] = value
                        elif 'mode' in key.lower():
                            data["Mode"] = value
                        elif 'key-mgmt' in key.lower():
                            data["Authentication"] = value

                if "Password" not in data:
                    try:
                        with open(f'/etc/NetworkManager/system-connections/{network}.nmconnection', 'r') as f:
                            content = f.read()
                            psk_match = re.search(r'psk=([^\n]+)', content)
                            if psk_match:
                                data["Password"] = psk_match.group(1)
                            ssid_match = re.search(r'ssid=([^\n]+)', content)
                            if ssid_match:
                                data["SSID"] = ssid_match.group(1)
                    except Exception:
                        pass

                data.setdefault("Password", "None")
                data.setdefault("Authentication", "None")
                data.setdefault("Mode", "Infrastructure")
                data.setdefault("SSID", network)

                table.clear_rows()
                table.title = f"Data of the {network} network"
                table.field_names = ["Property", "Value"]
                for key, value in data.items():
                    table.add_row([key, value])
                print(table)

            except subprocess.CalledProcessError:
                print(colored("[-] Network not found or no saved profile", "red"))
            except Exception as e:
                print(colored(f"[-] Something error was occurred: {e}", "red"))


wifighter = WiFighter()
wifighter.greeting_animation()
while True:
    try:
        command = input(colored("Wi-Fighter$ ", "cyan"))
        if command == "scan":
            wifighter.scan_networks()
            table.clear_rows()
        elif command == "showinfo":
            wifi_network = input(colored("[*] Enter the network's name: ", "yellow"))
            wifighter.show_WiFi_data(wifi_network)
        elif command in ["help", "--h"]:
            table.clear_rows()
            table.field_names = ["Command", "Description"]
            for cmd, dsc in commands.items():
                table.add_row([cmd, dsc])
            print(table, '\n')
            print("To use Wi-Fighter just write command and necessary arguments")
        elif command == "clear":
            if os_system == "Windows":
                subprocess.run("cls", shell=True)
            else:
                subprocess.run("clear", shell=True)
        elif command == "banner":
            print(colored("""
██╗    ██╗██╗      ███████╗██╗ ██████╗ ██╗  ██╗████████╗███████╗██████╗ 
██║    ██║██║      ██╔════╝██║██╔════╝ ██║  ██║╚══██╔══╝██╔════╝██╔══██╗
██║ █╗ ██║██║█████╗█████╗  ██║██║  ███╗███████║   ██║   █████╗  ██████╔╝
██║███╗██║██║╚════╝██╔══╝  ██║██║   ██║██╔══██║   ██║   ██╔══╝  ██╔══██╗
╚███╔███╔╝██║      ██║     ██║╚██████╔╝██║  ██║   ██║   ███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝      ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                        by R3DDoS_GH0$T""", "red"))
        elif command in ["quit", "exit"]:
            sys.exit(0)
    except KeyboardInterrupt:
        exit()
