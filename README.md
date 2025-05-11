
# 🛠️ **CTF Crypto Toolkit**

![Logo](https://your-logo-url.com/logo.png)  <!-- Replace with your actual logo URL -->

**CTF Crypto Toolkit** is an advanced set of tools designed to help cybersecurity enthusiasts, penetration testers, and CTF players tackle a variety of challenges related to cryptography, hash cracking, and encoding/decoding. This toolkit offers features like hash detection, hash cracking, and more.

---

### 🔧 **Features**
- **Auto Hash Detection**: Automatically identifies hash types and suggests cracking methods.
- **Hash Cracking**: Uses tools like `hashcat` to crack known hashes (e.g., SHA256, SHA1, MD5).
- **Multi-mode Support**: Supports various modes for cracking, decoding, and forensic analysis.
- **Extendable**: Easily extendable with new algorithms and features.

---

### 💻 **Installation**

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/xiamsec/CTF-Crypto-Toolkit.git
    cd CTF-Crypto-Toolkit
    ```

2. Install dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

3. **Download the Wordlist** (e.g., `rockyou.txt` for cracking):

    ```bash
    curl -O https://github.com/danielmiessler/SecLists/raw/master/Passwords/Leaked-Databases/rockyou.txt.gz
    gunzip rockyou.txt.gz
    ```

4. **Ensure Hashcat is Installed**:

    - Follow the installation guide for Hashcat: [Hashcat Installation Guide](https://hashcat.net/hashcat/)

---

### 🚀 **Usage**

To run the toolkit, use the following commands:

#### **Auto Mode (Detect Hash Type and Crack)**

```bash
python3 main.py --input "aec12651782dc34ce9106b3bc070d0979aa62d17" --mode auto
```

- This will auto-detect the hash type and attempt to crack it.

#### **Hash Mode (Manually Crack a Given Hash)**

```bash
python3 main.py --input "aec12651782dc34ce9106b3bc070d0979aa62d17" --mode hash
```

- This will attempt to crack the hash using available wordlists like `rockyou.txt`.

#### **Additional Modes (Coming Soon)**

- **Decode Mode**: Decode various types of encoded text.
- **Stego Mode**: Forensic analysis for hidden data inside files (coming soon).

---

### ⚙️ **Configuration**

The configuration is mostly automatic, but if needed, you can manually specify the hash type or wordlist path in the `main.py` file.

---

### 📝 **Notes**

- Ensure `hashcat` is installed and accessible in your system's PATH.
- You can customize the wordlist used by changing the path in the `crack_hash` function.
- For large hashes, you might need more powerful hardware or optimizations.

---

### 👨‍💻 **Author & Creator**

**XiamSec** - Cybersecurity Enthusiast and Penetration Tester.

Follow me on social media:

- **Twitter**: [@xiamsec](https://twitter.com/xiamsec)
- **LinkedIn**: [XiamSec](https://linkedin.com/in/xiamsec)
- **GitHub**: [@xiamsec](https://github.com/xiamsec)

---

### 📃 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### 🛠️ **Support**

For any issues or feature requests, please create an issue on GitHub or reach out to me via the social media links above.
