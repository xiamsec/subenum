Got it!  
You want me to create a **ready-to-use `README.md`** file (in **English**) for your `subenum` project, based on everything I wrote above.  
I'll make it clean, professional, and properly formatted — you can directly put it into your GitHub repo.

Here’s the full `README.md` for your `subenum` folder:

---

# SubEnum

**SubEnum** is a fast and asynchronous subdomain enumeration tool.  
It gathers subdomains from multiple public sources, supports bruteforce, and validates DNS records.

---

## ✨ Features

- 🔍 Collects subdomains from multiple sources like crt.sh, ThreatCrowd, and HackerTarget
- 🚀 Asynchronous networking for faster request handling
- 🛡️ DNS record validation for discovered subdomains
- 🧠 Supports bruteforce with custom wordlists
- 📂 Save results to a file
- 🎨 Colorful and clean CLI output
- 📜 Simple and clean code structure

---

## ⚡ Installation

> Requirements: **Python 3.8 or higher**

```bash
# Clone the repository
git clone https://github.com/xiamsec/subenum.git

# Navigate into the directory
cd subenum

# Install required packages
pip install -r requirements.txt
```

---

## 🛠️ Usage

Basic subdomain enumeration:

```bash
python3 main.py -d example.com
```

Subdomain enumeration with bruteforce:

```bash
python3 main.py -d example.com -b wordlist.txt
```

Save results into a file:

```bash
python3 main.py -d example.com -o output.txt
```

---

### ➡️ Full Options

| Option | Description |
|:------|:------------|
| `-d`   | Target domain (example: example.com) |
| `-b`   | Bruteforce wordlist file path |
| `-o`   | Output file to save the results |
| `-t`   | Number of concurrent threads (default: 20) |

---

## 📖 Example

```bash
python3 main.py -d hackerone.com -b common_subdomains.txt -o hackerone_subdomains.txt
```

---

## 📋 Requirements

- Python 3.8+
- aiohttp
- aiodns
- colorama
- argparse
- requests

(All required packages are listed in `requirements.txt`)

---

## 🤝 Contribution

Found a bug? Have a feature request?  
Feel free to open an issue or submit a pull request. Contributions are always welcome!

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🔗 Author

Developed by **[xiamsec](https://github.com/xiamsec)** 🚀

---

# 🚀 Happy Hunting!
