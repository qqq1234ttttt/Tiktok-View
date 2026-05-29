# Termux Compatible Version

import os
import time
import requests
from colorama import Fore, init

init(autoreset=True)

banner = f"""{Fore.CYAN}

███████ ███████ ███████  ██████  ██    ██
   ███  ██      ██      ██    ██  ██  ██
  ███   █████   █████   ██    ██   ████
 ███    ██      ██      ██    ██    ██
███████ ███████ ██       ██████     ██

"""

class ZefoyTermux:

    def __init__(self):
        self.sent = 0

    def clear(self):
        os.system("clear")

    def print_menu(self):
        print(Fore.GREEN + "[1] Followers")
        print(Fore.GREEN + "[2] Hearts")
        print(Fore.GREEN + "[3] Views")
        print(Fore.GREEN + "[4] Shares")
        print(Fore.RED   + "[0] Exit")

    def send_fake(self, url, service):
        print(Fore.YELLOW + f"\nSending {service}...")
        time.sleep(2)

        try:
            r = requests.get("https://zefoy.com")

            if r.status_code == 200:
                self.sent += 1
                print(Fore.GREEN + f"Success! Total Sent: {self.sent}")
            else:
                print(Fore.RED + "Website Error")

        except Exception as e:
            print(Fore.RED + f"Error: {e}")

    def main(self):

        while True:
            self.clear()
            print(banner)

            self.print_menu()

            choice = input(Fore.CYAN + "\nSelect Option: ")

            if choice == "0":
                break

            url = input(Fore.WHITE + "\nTikTok Video URL: ")

            services = {
                "1": "Followers",
                "2": "Hearts",
                "3": "Views",
                "4": "Shares"
            }

            if choice in services:
                self.send_fake(url, services[choice])
            else:
                print(Fore.RED + "Invalid Option")

            input("\nPress Enter to continue...")


if __name__ == "__main__":
    app = ZefoyTermux()
    app.main()
