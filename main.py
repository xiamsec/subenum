import asyncio
import sys
from colorama import Fore, init
import argparse
from subenum import main_async, print_banner

# Initialize Colorama
init(autoreset=True)

def main():
    parser = argparse.ArgumentParser(
        description="Advanced Subdomain Enumerator Tool",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""{Fore.YELLOW}
Example Usage:
  python3 main.py -d example.com
  python3 main.py -d example.com -b wordlist.txt
  python3 main.py -d example.com -b wordlist.txt -o output.txt --json output.json
"""
    )

    parser.add_argument("-d", "--domain", required=True, help="Target domain (example.com)")
    parser.add_argument("-b", "--wordlist", help="Bruteforce wordlist path (optional)")
    parser.add_argument("-o", "--output", help="Save results to a text file")
    parser.add_argument("--json", help="Save results to a JSON file")

    args = parser.parse_args()

    print_banner()

    try:
        asyncio.run(main_async(args))
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Keyboard Interrupted! Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
