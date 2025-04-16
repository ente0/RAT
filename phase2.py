import os
import sys
import subprocess
import logging
import shutil
from datetime import datetime
from termcolor import colored

logging.basicConfig(
    filename="rat_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s"
)

TOOLS = {
    "nmap_ignora_ping": lambda domain: ["nmap", "-Pn", "-T4", domain],
    "nmap_scansione_porte_comuni": lambda domain: ["nmap", "-F", domain],
    "nmap_identificare_script_e_vulnerabilità": lambda domain: ["nmap", "--script", "vuln", domain],
    "nmap_ping_scan": lambda domain: ["nmap", "-sn", domain],
    "nmap_porte_80_443": lambda domain: ["nmap", "-p", "80,443", domain],
    "nmap_version": lambda domain: ["nmap", "-sV", domain],
    "nmap_tutte_le_porte": lambda domain: ["nmap", "-p-", domain],
    "nmap_sistema_operativo": lambda domain: ["nmap", "-O", "-T4", domain],
    "nmap_scansione_aggressiva": lambda domain: ["nmap", "-A", domain],
    "nmap_servizi_ftp_http": lambda domain: ["nmap", "-p", "21", "--script", "ftp-anon", "-T4", domain],
    "nmap_rete_interna": lambda domain: ["nmap", "-p", "80", "--script", "http-enum", domain],
    "nmap_scansione_spoofing": lambda domain: ["nmap", "-D", "RND:10", domain],
}

def print_tool_banner():
    """Display ASCII art logo for tools used in PHASE 2"""
    terminal_width = shutil.get_terminal_size().columns
    
    ascii_art = [
        r"   _____                       _               ",
        r"  / ____|                     (_)              ",
        r" | (___   ___ __ _ _ __  _ __  _ _ __   __ _   ",
        r"  \___ \ / __/ _` | '_ \| '_ \| | '_ \ / _` |  ",
        r"  ____) | (_| (_| | | | | | | | | | | | (_| |  ",
        r" |_____/ \___\__,_|_| |_|_| |_|_|_| |_|\__, |  ",
        r"                                         __/ |  ",
        r"                                        |___/   ",
        "",
        "PHASE 2: VULNERABILITY SCANNING & PORT ANALYSIS",
        "Security Assessment Tool",
        ""
    ]
    
    print("\n")
    for line in ascii_art:
        padding = (terminal_width - len(line)) // 2
        colored_line = colored(line, 'green')
        print(" " * padding + colored_line)
    print("\n")

def print_header(title, color="cyan"):
    """Print a formatted header with the given title"""
    terminal_width = shutil.get_terminal_size().columns
    separator = "=" * terminal_width
    
    print(colored(separator, color))
    print(colored(f"   {title}", color, attrs=['bold']))
    print(colored(separator, color))

def read_domains(file_path):
    """Legge i domini da un file"""
    try:
        with open(file_path, "r") as file:
            domains = [line.strip() for line in file if line.strip()]
            if domains:
                print(colored(f"\n[✓] Successfully loaded {len(domains)} target(s).", 'green'))
            else:
                print(colored("\n[!] File exists but contains no targets.", 'yellow'))
            return domains
    except FileNotFoundError:
        print(colored("\n[!] File not found.", 'red'))
        return []
    except Exception as e:
        print(colored(f"\n[!] Error reading domains: {str(e)}", 'red'))
        logging.error(f"Error reading domains: {str(e)}")
        return []

def save_results(tool_name, domain, output):
    try:
        directory = os.path.join("phase2", tool_name)
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{domain}.txt")
        
        with open(file_path, "w") as file:
            file.write(output)
            
        print(colored(f"[✓] Results saved to {file_path}", 'green'))
        return True
    except Exception as e:
        print(colored(f"[!] Error saving results: {str(e)}", 'red'))
        logging.error(f"Error saving results for {tool_name} on {domain}: {e}")
        return False

def run_tool(tool_name, domain):
    print(colored(f"\n[*] Running {tool_name} on {domain}...", 'cyan'))
    
    try:
        command = TOOLS[tool_name](domain)
        print(colored(f"[*] Executing: {' '.join(command)}", 'blue'))
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            save_results(tool_name, domain, result.stdout)
            print(colored(f"[✓] {tool_name} completed successfully.", 'green'))
        else:
            print(colored(f"[!] {tool_name} failed with error code {result.returncode}", 'yellow'))
            print(colored(f"Error output: {result.stderr}", 'red'))
            save_results(tool_name, domain, f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}")
    except FileNotFoundError:
        print(colored(f"[!] Error executing {tool_name} on {domain}: Command not found", 'red'))
        logging.error(f"Error executing {tool_name} on {domain}: Command not found")
    except Exception as e:
        print(colored(f"[!] Error executing {tool_name} on {domain}: {str(e)}", 'red'))
        logging.error(f"Error executing {tool_name} on {domain}: {e}")

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_interattivo():
    """Displays an interactive menu for tool selection"""
    terminal_width = shutil.get_terminal_size().columns
    separator = "=" * terminal_width
    dash_separator = "-" * terminal_width
    
    print(colored("\n TOOL SELECTION:", 'green', attrs=['bold']))
    
    options = []
    for idx, tool in enumerate(TOOLS.keys(), 1):
        options.append(f"{colored(f'[{idx}]', 'cyan', attrs=['bold'])} {tool}")
    
    options.append(f"{colored(f'[{len(TOOLS) + 1}]', 'cyan', attrs=['bold'])} Run All Tools")
    options.append(f"{colored('[B]', 'magenta', attrs=['bold'])} Back to Main Menu")
    
    print("\n " + "\n ".join(options))
    print("\n" + colored(dash_separator, 'cyan'))
    
    while True:
        try:
            choice = input(colored("\nEnter option (1-13, B to go back): ", 'cyan', attrs=['bold'])).strip().lower()
            
            if choice == 'b':
                return -1
            
            choice = int(choice)
            if 1 <= choice <= len(TOOLS) + 1:
                return choice
            else:
                print(colored("\n[!] Invalid option. Please try again.", 'yellow'))
        except ValueError:
            print(colored("\n[!] Please enter a valid number.", 'yellow'))

def main():
    """Main function to run the scanning module"""
    os.makedirs("phase2", exist_ok=True)
    for tool in TOOLS:
        os.makedirs(os.path.join("phase2", tool), exist_ok=True)
    
    clear_screen()
    print_tool_banner()
    
    if os.path.exists("targets.txt"):
        print(colored("\n[i] Found targets.txt file.", 'cyan'))
        domains = read_domains("targets.txt")
    else:
        file_path = input(colored("\nEnter path to target list file: ", 'cyan')).strip()
        domains = read_domains(file_path)
    
    if not domains:
        print(colored("\n[!] No domains to scan. Aborting.", 'red'))
        input(colored("\nPress Enter to continue...", 'cyan'))
        return
    
    choice = menu_interattivo()
    
    if choice == -1:
        return 
    
    clear_screen()
    print_header("PHASE 2: VULNERABILITY SCANNING", "green")
    
    if choice == len(TOOLS) + 1:
        print(colored("\n[*] Running all scanning tools...", 'cyan'))
        for tool_name in TOOLS:
            print(colored(f"\n[*] Starting {tool_name}...", 'green', attrs=['bold']))
            for domain in domains:
                run_tool(tool_name, domain)
    else:
        tool_name = list(TOOLS.keys())[choice - 1]
        print(colored(f"\n[*] Running {tool_name} on all targets...", 'cyan'))
        for domain in domains:
            run_tool(tool_name, domain)
    
    print(colored("\n[✓] Vulnerability scanning completed.", 'green'))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n\nOperation cancelled by user. Exiting...", 'yellow'))
    except Exception as e:
        logging.critical(f"Unhandled exception: {str(e)}")
        print(colored(f"\n[!] An unexpected error occurred: {str(e)}", 'red'))
        print(colored("Check the log file for more details.", 'red'))