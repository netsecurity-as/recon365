import re
from colorama import Fore, Style


class Printer:
    def __init__(self, color, verbose):
        self.color = color
        self.verbose = verbose

    def content(self, text: str):
        text = re.sub("^", " | ", str(text))
        text = text.replace("\n", "\n | ")
        print(text)

    def positive(self, text: str):
        prefix = f"{Fore.GREEN}[+]{Style.RESET_ALL}" if self.color else "[+]"
        print(f"{prefix} {text}")

    def negative(self, text: str):
        prefix = f"{Fore.RED}[-]{Style.RESET_ALL}" if self.color else "[-]"
        print(f"{prefix} {text}")

    def good(self, text: str):
        prefix = f"{Fore.GREEN}[✔]{Style.RESET_ALL}" if self.color else "[✔]"
        print(f"{prefix} {text}")

    def bad(self, text: str):
        prefix = f"{Fore.RED}[✘]{Style.RESET_ALL}" if self.color else "[✘]"
        print(f"{prefix} {text}")

    def warning(self, text: str):
        prefix = f"{Fore.YELLOW}[!]{Style.RESET_ALL}" if self.color else "[!]"
        print(f"{prefix} {text}")
        
    def info(self, text: str):
        prefix = f"{Fore.BLUE}[i]{Style.RESET_ALL}" if self.color else "[i]"
        print(f"{prefix} {text}", end="\n" if self.verbose else "\r")
