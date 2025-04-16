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

DEFAULT_WORDLISTS = {
    "dirb": "/usr/share/dirb/wordlists/common.txt",
    "hydra": "wordlist.txt",
    "gobuster": "/usr/share/wordlists/dirb/common.txt"
}

selected_wordlists = {
    "dirb": DEFAULT_WORDLISTS["dirb"],
    "hydra": DEFAULT_WORDLISTS["hydra"],
    "gobuster": DEFAULT_WORDLISTS["gobuster"]
}

def get_tools():
    return {
        "dirbuster_dirs": lambda domain: ["dirb", f"http://{domain}", selected_wordlists["dirb"]],
        "dirbuster_extensions": lambda domain: ["dirb", f"http://{domain}", selected_wordlists["dirb"], "-x", ".php,.txt,.html"],
        "gobuster_dirs": lambda domain: ["gobuster", "dir", "-u", f"http://{domain}", "-w", selected_wordlists["gobuster"]],
        "gobuster_dns": lambda domain: ["gobuster", "dns", "-d", domain, "-w", selected_wordlists["gobuster"]],
        "gobuster_vhost": lambda domain: ["gobuster", "vhost", "-u", f"http://{domain}", "-w", selected_wordlists["gobuster"]],
        "sqlmap_scan_base": lambda domain: ["sqlmap", "-u", f"http://{domain}", "--batch"],
        "sqlmap_scan_forms": lambda domain: ["sqlmap", "-u", f"http://{domain}", "--forms", "--batch"],
        "sqlmap_scan_post": lambda domain: ["sqlmap", "-u", f"http://{domain}", "--data", "param1=value1&param2=value2", "--batch"],
        "sqlmap_dump_db": lambda domain: ["sqlmap", "-u", f"http://{domain}", "--dump", "--batch"],
        "nikto_scan_base": lambda domain: ["nikto", "-h", domain, "-o", "report.html", "-Format", "html"],
        "nikto_scan_ssl": lambda domain: ["nikto", "-h", domain, "-ssl"],
        "nikto_scan_tuning": lambda domain: ["nikto", "-h", domain, "-Tuning", "x6789"],
        "hydra_http_form": lambda domain: ["hydra", "-l", "admin", "-P", selected_wordlists["hydra"], domain, "http-post-form", "/login.php:username=^USER^&password=^PASS^:Login failed"],
        "hydra_basic_auth": lambda domain: ["hydra", "-l", "admin", "-P", selected_wordlists["hydra"], domain, "http-get", "/admin"], 
    }

def print_tool_banner():
    """Display ASCII art logo for tools used in phase 3"""
    terminal_width = shutil.get_terminal_size().columns
    
    ascii_art = [
        r"  ______                                      _   _             ",
        r" |  ____|                                    | | (_)            ",
        r" | |__   _ __  _   _ _ __ ___   ___ _ __ __ _| |_ _  ___  _ __  ",
        r" |  __| | '_ \| | | | '_ ` _ \ / _ \ '__/ _` | __| |/ _ \| '_ \ ",
        r" | |____| | | | |_| | | | | | |  __/ | | (_| | |_| | (_) | | | |",
        r" |______|_| |_|\__,_|_| |_| |_|\___|_|  \__,_|\__|_|\___/|_| |_|",
        r"                                                                ",
        "",
        "PHASE 3: ENUMERATION",
        "Security Assessment Tool",
        ""
    ]
    
    print("\n")
    for line in ascii_art:
        padding = (terminal_width - len(line)) // 2
        colored_line = colored(line, 'red')
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
        directory = os.path.join("phase3", tool_name)
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
        command = get_tools()[tool_name](domain)
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
    
    print(colored("\n TOOL SELECTION:", 'red', attrs=['bold']))
    
    options = []
    for idx, tool in enumerate(get_tools().keys(), 1):
        options.append(f"{colored(f'[{idx}]', 'cyan', attrs=['bold'])} {tool}")
    
    options.append(f"{colored(f'[{len(get_tools()) + 1}]', 'cyan', attrs=['bold'])} Run All Tools")
    options.append(f"{colored(f'[{len(get_tools()) + 2}]', 'cyan', attrs=['bold'])} Configure Wordlists")
    options.append(f"{colored('[B]', 'magenta', attrs=['bold'])} Back to Main Menu")
    
    print("\n " + "\n ".join(options))
    print("\n" + colored(dash_separator, 'cyan'))
    
    while True:
        try:
            choice = input(colored(f"\nEnter option (1-{len(get_tools()) + 2}, B to go back): ", 'cyan', attrs=['bold'])).strip().lower()
            
            if choice == 'b':
                return -1
            
            choice = int(choice)
            if 1 <= choice <= len(get_tools()) + 2:
                return choice
            else:
                print(colored("\n[!] Invalid option. Please try again.", 'yellow'))
        except ValueError:
            print(colored("\n[!] Please enter a valid number.", 'yellow'))

def validate_wordlist(wordlist_path):
    """Validate if the wordlist exists."""
    if os.path.isfile(wordlist_path):
        return True
    else:
        return False

def configure_wordlists():
    """Configure wordlists for the various tools."""
    clear_screen()
    print_header("WORDLIST CONFIGURATION", "green")
    
    tools = ["dirb", "hydra", "gobuster"]
    
    for tool in tools:
        print(colored(f"\n[*] Configure wordlist for {tool.upper()}", 'cyan'))
        print(colored(f"[i] Current wordlist: {selected_wordlists[tool]}", 'blue'))
        
        while True:
            new_wordlist = input(colored(f"Enter path to new wordlist for {tool} (or press Enter to keep current): ", 'cyan')).strip()
            
            if not new_wordlist:
                print(colored(f"[i] Keeping current wordlist for {tool}", 'blue'))
                break
            
            if validate_wordlist(new_wordlist):
                selected_wordlists[tool] = new_wordlist
                print(colored(f"[✓] Updated wordlist for {tool} to: {new_wordlist}", 'green'))
                break
            else:
                print(colored(f"[!] Wordlist not found at: {new_wordlist}", 'red'))
                retry = input(colored("Try again? (y/n): ", 'yellow')).lower()
                if retry != 'y':
                    break
    
    print(colored("\n[✓] Wordlist configuration complete.", 'green'))
    input(colored("\nPress Enter to continue...", 'cyan'))

def main():
    """Main function to run the web application testing module"""
    os.makedirs("phase3", exist_ok=True)
    for tool in get_tools():
        os.makedirs(os.path.join("phase3", tool), exist_ok=True)
    
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
    
    while True:
        choice = menu_interattivo()
        
        if choice == -1:
            return 
        
        if choice == len(get_tools()) + 2:
            configure_wordlists()
            continue
        
        clear_screen()
        print_header("PHASE 3: WEB APPLICATION TESTING", "red")
        
        if choice == len(get_tools()) + 1:
            print(colored("\n[*] Running all web application testing tools...", 'cyan'))
            for tool_name in get_tools():
                print(colored(f"\n[*] Starting {tool_name}...", 'blue', attrs=['bold']))
                for domain in domains:
                    run_tool(tool_name, domain)
        else:
            tool_name = list(get_tools().keys())[choice - 1]
            print(colored(f"\n[*] Running {tool_name} on all targets...", 'cyan'))
            for domain in domains:
                run_tool(tool_name, domain)
        
        print(colored("\n[✓] Web application testing completed.", 'green'))
        input(colored("\nPress Enter to continue...", 'cyan'))
        clear_screen()
        print_tool_banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n\nOperation cancelled by user. Exiting...", 'yellow'))
    except Exception as e:
        logging.critical(f"Unhandled exception: {str(e)}")
        print(colored(f"\n[!] An unexpected error occurred: {str(e)}", 'red'))
        print(colored("Check the log file for more details.", 'red'))