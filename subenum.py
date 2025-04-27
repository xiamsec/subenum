import asyncio
import aiohttp
import socket
import random
import string
import argparse
import sys
from colorama import Fore, Style, init
import json

# Initialize colorama
init(autoreset=True)

# Banner
def print_banner():
    banner = f"""
{Fore.CYAN}

  ███████╗██╗   ██╗██████╗ ███████╗███╗   ██╗██╗   ██╗███╗   ███╗
██╔════╝██║   ██║██╔══██╗██╔════╝████╗  ██║██║   ██║████╗ ████║
███████╗██║   ██║██║  ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║
╚════██║██║   ██║██║  ██║██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║
███████║╚██████╔╝██████╔╝███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║
╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝
                

{Fore.GREEN}         Subdomain Enumerator | {Fore.RED}by xiamsec
    """
    print(banner)

# Validate DNS (check if subdomain resolves)
async def dns_lookup(subdomain):
    loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(subdomain, None)
        return True
    except:
        return False

# Check if alive (HTTP server responds)
async def is_alive(subdomain):
    urls = [f"http://{subdomain}", f"https://{subdomain}"]
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for url in urls:
            try:
                async with session.get(url, ssl=False) as resp:
                    if resp.status < 500:
                        return True
            except:
                pass
    return False

# Check if domain has wildcard DNS
async def is_wildcard(domain):
    random_sub = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    test_subdomain = f"{random_sub}.{domain}"
    try:
        socket.gethostbyname(test_subdomain)
        return True
    except socket.gaierror:
        return False

# Fetch from crt.sh
async def fetch_crtsh(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json(content_type=None)
                    return [entry['name_value'] for entry in data]
    except:
        return []

# Fetch from ThreatCrowd
async def fetch_threatcrowd(domain):
    try:
        url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('subdomains', [])
    except:
        return []

# Fetch from HackerTarget
async def fetch_hackertarget(domain):
    try:
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    return [line.split(',')[0] for line in text.splitlines()]
    except:
        return []

# Bruteforce subdomains
async def bruteforce(domain, wordlist):
    subs = set()
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        for word in wordlist:
            subdomain = f"{word.strip()}.{domain}"
            tasks.append(dns_lookup(subdomain))
        
        results = await asyncio.gather(*tasks)

        for word, result in zip(wordlist, results):
            if result:
                subs.add(f"{word.strip()}.{domain}")
    return subs

# Main Enumeration
async def main_async(args):
    domain = args.domain
    wordlist = args.wordlist
    output_file = args.output
    json_file = args.json

    all_subdomains = set()

    # Wildcard Check
    wildcard = await is_wildcard(domain)
    if wildcard:
        print(Fore.RED + "[!] Wildcard DNS detected! Filtering results...")
    else:
        print(Fore.GREEN + "[+] No wildcard DNS detected.")

    # Fetching from multiple sources
    print(Fore.YELLOW + "\n[*] Fetching subdomains from public sources...")
    sources = await asyncio.gather(
        fetch_crtsh(domain),
        fetch_threatcrowd(domain),
        fetch_hackertarget(domain)
    )

    for src in sources:
        if src:  # Check if not None or empty
            all_subdomains.update(src)

    # Bruteforce if enabled
    if wordlist:
        print(Fore.YELLOW + "\n[*] Bruteforcing subdomains...")
        try:
            with open(wordlist, 'r') as f:
                words = f.read().splitlines()
            brute_subs = await bruteforce(domain, words)
            all_subdomains.update(brute_subs)
        except Exception as e:
            print(Fore.RED + f"[!] Bruteforce Error: {e}")

    # Validate found subdomains
    print(Fore.YELLOW + "\n[*] Validating found subdomains...")
    validated = set()
    tasks = []
    for sub in all_subdomains:
        tasks.append(dns_lookup(sub))

    results = await asyncio.gather(*tasks)

    for sub, valid in zip(all_subdomains, results):
        if valid:
            validated.add(sub)

    # Filter wildcards
    found_subdomains = set()
    if wildcard:
        # Extra strict if wildcard
        for sub in validated:
            if not sub.startswith("www."):
                found_subdomains.add(sub)
    else:
        found_subdomains = validated

    # Alive check
    print(Fore.YELLOW + "\n[*] Checking which subdomains are alive...")
    alive = set()
    tasks = []
    for sub in found_subdomains:
        tasks.append(is_alive(sub))

    results = await asyncio.gather(*tasks)

    for sub, ok in zip(found_subdomains, results):
        if ok:
            alive.add(sub)

    # Final output
    print(Fore.GREEN + f"\n[+] Found {len(alive)} alive subdomains:\n")
    for sub in alive:
        print(Fore.CYAN + sub)

    # Save TXT
    if output_file:
        try:
            with open(output_file, "w") as f:
                for sub in alive:
                    f.write(sub + "\n")
            print(Fore.CYAN + f"\n[+] Results saved to {output_file}")
        except Exception as e:
            print(Fore.RED + f"[!] Failed to save TXT: {e}")

    # Save JSON
    if json_file:
        try:
            with open(json_file, "w") as f:
                json.dump(list(alive), f, indent=4)
            print(Fore.CYAN + f"[+] Results also saved to {json_file}")
        except Exception as e:
            print(Fore.RED + f"[!] Failed to save JSON: {e}")

# CLI parser
def main():
    parser = argparse.ArgumentParser(
        description="Advanced Subdomain Enumerator Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("-d", "--domain", required=True, help="Target domain (example.com)")
    parser.add_argument("-b", "--wordlist", help="Bruteforce wordlist path")
    parser.add_argument("-o", "--output", help="Save output to a file (e.g., results.txt)")
    parser.add_argument("--json", help="Save output as JSON file")

    args = parser.parse_args()

    print_banner()

    try:
        asyncio.run(main_async(args))
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Keyboard Interrupted! Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
