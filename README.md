<p align="center">
  <img src="https://img.shields.io/badge/license-green" alt="License">
  <img src="https://img.shields.io/badge/language-python-blue" alt="Language: Python">
  <img src="https://img.shields.io/badge/release-v1.0.0-green" alt="Version">
  <img src="https://img.shields.io/badge/platform-linux-orange" alt="Platform">
</p>

<div align="center">
  
# RAT: Scan and Analyze
### **A comprehensive offensive security framework that automates reconnaissance, scanning, and enumeration phases for penetration testing.**

</div>


> [!CAUTION]
> This tool is strictly for authorized security testing and educational purposes. Always obtain explicit permission before conducting any security assessments.

## 🚀 Key Features

- 🔍 **Three-phase workflow**
  - Phase 1: Reconnaissance - Initial information gathering
  - Phase 2: Scanning - Detailed system analysis
  - Phase 3: Enumeration - Service and vulnerability identification

- 🧰 **Integration with popular tools**
  - nmap, whois, whatweb, theHarvester
  - amass, sublist3r, nuclei
  - dirbuster, hydra, sqlmap, nikto

- 📊 **Centralized result management**
  - Organized output structure
  - Comprehensive logging system
  - Automatic report generation

- 🔧 **Advanced utilities**
  - Target list import
  - Dependency management
  - Results export functionality

## 💻 System Requirements

### 🐧 Linux Environment
- **Distributions**: 
  - Kali Linux (Recommended)
  - Arch Linux
  - Debian/Ubuntu

> [!WARNING]
> This tool is designed for Linux environments only. Windows compatibility is not supported.

## 🔧 Dependencies Installation

```bash
# For Kali/Debian/Ubuntu systems
sudo apt update && sudo apt install -y whois dnsutils whatweb theharvester \
amass sublist3r nuclei nmap dirbuster hydra sqlmap nikto python3-pip

# For Arch-based systems
sudo pacman -Sy && sudo pacman -S --noconfirm whois bind-tools whatweb \
theharvester amass sublist3r nuclei nmap dirbuster hydra sqlmap nikto python3-pip
```

## 📦 Installation & Usage

### Clone the repository
```bash
git clone https://github.com/ente0/RAT.git
cd RAT
```

### Run RAT
```bash
python3 rat.py
```

### Setting up targets
Before running scans, you need to specify your targets in a file named `targets.txt` in the root directory of the project. Each target should be on a separate line.

```bash
# Example targets.txt content
example.com
192.168.1.1
test-server.local
```

You can create this file manually or import targets from an existing file:

1. From the main menu, select `[U]` for Utility Functions
2. Choose option `[1]` Import Target List
3. Enter the path to your existing target list file
4. The program will read from this file and use these targets for scanning

Note that RAT does not create the file automatically - it expects the specified file to exist at the path you provide.

### Dependency check
If you're missing any required tools, you can use the built-in dependency checker:

1. From the main menu, select `[U]` for Utility Functions
2. Choose option `[3]` Check Dependencies
3. Follow the prompts to install missing dependencies

> [!NOTE]
> During the dependency check, a dirbuster window may appear. Simply close this window - this is a known issue that will be fixed in a future update.

> [!TIP]
> Results are stored in the `results/` directory, organized by phase and target.

## 🎮 Menu Options

| Option | Description | Function |
|--------|-------------|----------|
| 1 | Phase 1: Reconnaissance | Initial information gathering (whois, DNS, OSINT) |
| 2 | Phase 2: Scanning | Port scanning, service identification, web analysis |
| 3 | Phase 3: Enumeration | Service enumeration, vulnerability scanning |
| U | Utility Functions | Import targets, export results, check dependencies |
| L | View Logs | Display detailed operation logs |
| C | Clear Results | Remove all generated results |
| Q | Quit | Exit the application |

## 🛠️ Module Details

### Phase 1: Reconnaissance
- Domain WHOIS information
- DNS enumeration
- Email harvesting
- Subdomain discovery
- Web technology identification

### Phase 2: Scanning
- Port scanning
- Service version detection
- Web server analysis
- SSL/TLS assessment
- Network topology mapping

### Phase 3: Enumeration
- Service vulnerability scanning
- Web application analysis
- Directory brute forcing
- Authentication testing
- Exploitation preparation

## 📚 Recommended Resources

#### Information Gathering
- 🔍 [OSINT Framework](https://osintframework.com/)
- 🌐 [SecLists](https://github.com/danielmiessler/SecLists)

#### Learning Resources
- 📘 [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- 🎓 [HackTricks](https://book.hacktricks.xyz/)

## 📝 License
Licensed under GNU License. See LICENSE file for details.

## 🤝 Support and Contributions

- 🐛 [Report Issues](https://github.com/ente0/RAT/issues)
- 💡 [Feature Requests](https://github.com/ente0/RAT/issues)
- 📧 Contact: enteo.dev@protonmail.com

> [!IMPORTANT]
> Always use this tool responsibly and ethically. Respect legal boundaries and obtain proper authorization before security testing.