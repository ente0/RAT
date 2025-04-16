import os
import sys
import shutil
import importlib
import subprocess
import logging
from datetime import datetime
from termcolor import colored

logging.basicConfig(
    filename="rat_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s"
)

MODULES = [
    "phase1",
    "phase2",
    "phase3",
]

def print_ascii_title():
    """Display ASCII art logo"""
    terminal_width = shutil.get_terminal_size().columns
    ascii_art = [
        r"     __             _,-\"~^\"-.             ",
        r"     _// )      _,-\"~`          `.             ",
        r"     ./\" ( /`\"-,-\"`               ;             ",
        r"    / 6                               ;             ",
        r"   /           ,             ,-\"     ;             ",
        r" (,__.--.      \           /        ;             ",
        r"          //'   /`-.\   |          |        `._________             ",
        r"              _.-'_/`  )  )--...,,,___\     \-----------,)             ",
        r"           (((\"~` _.-'.-'           __`-.   )        //             ",
        r"               (((\"`             (((---~\"`       //             ",
        r"                                                                 ((________________             ",
        r"                                                                   `--------~~~~~~~~`             ",
        "",
    ]


    
    print("\n")
    for line in ascii_art:
        padding = (terminal_width - len(line)) // 2
        colored_line = colored(line, 'blue')
        print(" " * padding + colored_line)
    print("\n")

def print_header(title, color="cyan"):
    """Print a formatted header with the given title"""
    terminal_width = shutil.get_terminal_size().columns
    separator = "=" * terminal_width
    
    print(colored(separator, color))
    print(colored(f"   {title}", color, attrs=['bold']))
    print(colored(separator, color))

def load_modules():
    """Dynamically load all available main_phase*.py modules"""
    available_modules = {}
    
    display_names = {
        "phase1": "phase 1",
        "phase2": "phase 2",
        "phase3": "phase 3",
        "phase4": "phase 4"
    }
    
    for module_name in MODULES:
        try:
            module = importlib.import_module(module_name)
            module_title = display_names.get(module_name, module_name)
            available_modules[module_name] = {
                'module': module,
                'title': module_title
            }
        except ImportError:
            logging.warning(f"Module {module_name} not found. Skipping.")
    
    return available_modules

def show_status_info():
    """Show current configuration and status information"""
    status_info = []
    
    if os.path.exists("targets.txt"):
        with open("targets.txt", "r") as f:
            targets = [line.strip() for line in f if line.strip()]
            if targets:
                status_info.append(f"[✓] {len(targets)} target(s) loaded")
    
    results_count = 0
    for root, dirs, files in os.walk("results", topdown=False):
        results_count += len(files)
    
    if results_count > 0:
        status_info.append(f"[✓] {results_count} result file(s) generated")
    
    if os.path.exists("rat_debug.log"):
        status_info.append(f"[✓] Last run: {datetime.fromtimestamp(os.path.getmtime('rat_debug.log')).strftime('%Y-%m-%d %H:%M:%S')}")
    
    return "\n    ".join(status_info) if status_info else ""

def show_main_menu(available_modules):
    """Display the main menu options"""
    terminal_width = shutil.get_terminal_size().columns
    separator = "=" * terminal_width
    dash_separator = "-" * terminal_width

    print_ascii_title()
    
    print(colored(separator, 'cyan'))
    print(colored(f"   Welcome to RAT!", 'cyan', attrs=['bold']))
    print(colored("   Reconnaissance and Analysis Toolkit", 'cyan', attrs=['dark']))
    print(colored(separator, 'cyan'))
    
    status_info = show_status_info()
    if status_info:
        print(colored(f"\n    {status_info}", 'green', attrs=['bold']))
    
    print(colored("\n AVAILABLE MODULES:", 'blue', attrs=['bold']))
    
    display_names = {
        "phase1": "Phase 1",
        "phase2": "Phase 2",
        "phase3": "Phase 3"
    }
    
    descriptions = {
        "phase1": "Reconnaissance",
        "phase2": "Scanning",
        "phase3": "Enumeration"
    }
    
    options = []
    for idx, (module_name, module_info) in enumerate(available_modules.items(), 1):
        display_name = display_names.get(module_name, module_name)
        description = descriptions.get(module_name, "")
        options.append(f"{colored(f'[{idx}]', 'cyan', attrs=['bold'])} {display_name} - {description}")
    
    print("\n " + "\n ".join(options))
    
    print("\n" + colored(dash_separator, 'cyan'))
    
    utility_options = [
        f"{colored('[U]', 'magenta', attrs=['bold'])} Utility Functions",
        f"{colored('[L]', 'magenta', attrs=['bold'])} View Logs",
        f"{colored('[C]', 'magenta', attrs=['bold'])} Clear All Results"
    ]
    
    print(colored("\n SYSTEM OPTIONS:", 'magenta', attrs=['bold']))
    print("\n " + "\n ".join(utility_options))
    
    print(colored("\n" + separator, 'magenta'))
    
    user_option = input(colored("\nEnter option (1-3, U, S, L, C, Q to quit): ", 'cyan', attrs=['bold'])).strip().lower()
    return user_option
def show_utility_menu():
    """Display utility functions menu"""
    print_header("Utility Functions", "magenta")
    
    options = [
        f"{colored('[1]', 'magenta', attrs=['bold'])} Import Target List",
        f"{colored('[2]', 'magenta', attrs=['bold'])} Export Results",
        f"{colored('[3]', 'magenta', attrs=['bold'])} Check Dependencies",
        f"{colored('[B]', 'cyan', attrs=['bold'])} Back to Main Menu"
    ]
    
    print("\n " + "\n ".join(options) + "\n")
    
    user_option = input(colored("\nEnter option (1-3, B to go back): ", 'magenta', attrs=['bold'])).strip().lower()
    return user_option

def import_target_list():
    """Import a list of targets from a file"""
    file_path = input(colored("\nEnter path to target list file: ", 'cyan')).strip()
    
    try:
        with open(file_path, "r") as file:
            targets = [line.strip() for line in file if line.strip()]
            
        if not targets:
            print(colored("\n[!] No targets found in file.", 'yellow'))
            return
            
        with open("targets.txt", "w") as outfile:
            for target in targets:
                outfile.write(f"{target}\n")
                
        print(colored(f"\n[✓] Successfully imported {len(targets)} targets.", 'green'))
        
    except FileNotFoundError:
        print(colored("\n[!] File not found.", 'red'))
    except Exception as e:
        print(colored(f"\n[!] Error importing targets: {str(e)}", 'red'))
        logging.error(f"Error importing targets: {str(e)}")

def execute_module(module_name, module_info):
    """Execute the specified module"""
    try:
        if hasattr(module_info['module'], 'main'):
            module_info['module'].main()
        else:
            print(colored(f"\n[!] The module {module_name} doesn't have a main function.", 'yellow'))
    except Exception as e:
        print(colored(f"\n[!] Error executing module {module_name}: {str(e)}", 'red'))
        logging.error(f"Error executing module {module_name}: {str(e)}")

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def view_logs():
    """Display the contents of the log file"""
    if os.path.exists("rat_debug.log"):
        try:
            with open("rat_debug.log", "r") as f:
                log_content = f.read()
                
            print_header("Log File Contents", "yellow")
            print(log_content)
            
            input(colored("\nPress Enter to continue...", 'cyan'))
        except Exception as e:
            print(colored(f"\n[!] Error reading log file: {str(e)}", 'red'))
    else:
        print(colored("\n[!] Log file not found.", 'yellow'))
        input(colored("\nPress Enter to continue...", 'cyan'))

def clear_results():
    """Clear all results and temporary files"""
    confirm = input(colored("\nAre you sure you want to clear all results? (y/n): ", 'red')).strip().lower()
    
    if confirm != 'y':
        return
        
    try:
        dirs_to_clean = ["results", "phase1", "phase2", "phase3", "phase4"]
        
        for directory in dirs_to_clean:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                os.makedirs(directory, exist_ok=True)
                
        print(colored("\n[✓] All results have been cleared.", 'green'))
    except Exception as e:
        print(colored(f"\n[!] Error clearing results: {str(e)}", 'red'))
        
    input(colored("\nPress Enter to continue...", 'cyan'))

def check_dependencies():
    """
    Check if required tools are installed and install missing ones
    """
    print_header("Checking Dependencies", "cyan")
    
    TOOLS = {
        "whois": {"apt": "whois", "pacman": "whois", "command": "whois"},
        "nslookup": {"apt": "dnsutils", "pacman": "bind-tools", "command": "nslookup"},
        "whatweb": {"apt": "whatweb", "pacman": "whatweb", "command": "whatweb"},
        "theHarvester": {"apt": "theharvester", "pacman": "theharvester", "command": "theHarvester"},
        "amass": {"apt": "amass", "pacman": "amass", "command": "amass"},
        "sublist3r": {"apt": "sublist3r", "pacman": "sublist3r", "command": "sublist3r"},
        "nuclei": {"apt": "nuclei", "pacman": "nuclei", "command": "nuclei"},
        "nmap": {"apt": "nmap", "pacman": "nmap", "command": "nmap"},
        "dirbuster": {"apt": "dirbuster", "pacman": "dirbuster", "command": "dirbuster"},
        "hydra": {"apt": "hydra", "pacman": "hydra", "command": "hydra"},
        "sqlmap": {"apt": "sqlmap", "pacman": "sqlmap", "command": "sqlmap"},
        "nikto": {"apt": "nikto", "pacman": "nikto", "command": "nikto"}
    }
    
    if shutil.which("apt"):
        pkg_manager = "apt"
        install_cmd = ["apt", "install", "-y"]
        update_cmd = ["apt", "update"]
    elif shutil.which("pacman"):
        pkg_manager = "pacman"
        install_cmd = ["pacman", "-S", "--noconfirm"]
        update_cmd = ["pacman", "-Sy"]
    else:
        print(colored("\n[!] Unsupported package manager. Only apt (Kali Linux) and pacman (Arch Linux) are supported.", "red"))
        return
    
    print(colored(f"\n[i] Detected package manager: {pkg_manager}", "cyan"))
    
    if os.geteuid() != 0:
        print(colored("\n[!] This function requires root privileges to install missing dependencies.", "yellow"))
        confirm = input(colored("Do you want to continue with checking only? (y/n): ", "yellow")).strip().lower()
        if confirm != 'y':
            return
        install_mode = False
    else:
        confirm = input(colored("\nDo you want to install missing dependencies? (y/n): ", "cyan")).strip().lower()
        install_mode = confirm == 'y'
    
    missing_tools = []
    installed_tools = []
    
    for tool, info in TOOLS.items():
        command = info["command"]
        package = info[pkg_manager]
        
        print(colored(f"\n[*] Checking {tool}...", "blue"))
        
        if shutil.which(command):
            installed_tools.append(tool)
            print(colored(f"[✓] {tool} is installed.", "green"))
            
            try:
                if tool == "nmap":
                    version_cmd = [command, "--version"]
                elif tool in ["amass", "nuclei", "sublist3r", "theHarvester"]:
                    version_cmd = [command, "-h"]
                else:
                    version_cmd = [command, "--version"]
                
                result = subprocess.run(version_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=3)
                version_output = result.stdout if result.stdout else result.stderr
                first_line = version_output.strip().split('\n')[0]
                print(colored(f"   - Version info: {first_line}", "cyan"))
            except (subprocess.SubprocessError, IndexError, TimeoutError):
                print(colored(f"   - Could not retrieve version info", "yellow"))
            
        else:
            missing_tools.append((tool, package))
            print(colored(f"[✗] {tool} is not installed.", "red"))
    
    print_header("Dependency Check Summary", "cyan")
    print(colored(f"\n[i] Found {len(installed_tools)} of {len(TOOLS)} required tools.", "blue"))
    
    if missing_tools:
        print(colored(f"\n[!] Missing tools: {', '.join([t[0] for t in missing_tools])}", "yellow"))
        
        if install_mode:
            print(colored("\n[i] Updating package repository...", "cyan"))
            try:
                subprocess.run(update_cmd, check=True)
                print(colored("[✓] Repository updated successfully.", "green"))
            except subprocess.SubprocessError as e:
                print(colored(f"[✗] Failed to update repository: {str(e)}", "red"))
                return
            
            for tool, package in missing_tools:
                print(colored(f"\n[i] Installing {tool} ({package})...", "cyan"))
                try:
                    cmd = install_cmd + [package]
                    subprocess.run(cmd, check=True)
                    print(colored(f"[✓] {tool} installed successfully.", "green"))
                except subprocess.SubprocessError as e:
                    print(colored(f"[✗] Failed to install {tool}: {str(e)}", "red"))
        else:
            print(colored("\n[i] To install missing tools, run the script with root privileges and select the install option.", "cyan"))
    else:
        print(colored("\n[✓] All required tools are installed.", "green"))
    
    logging.info(f"Dependency check completed. Installed: {len(installed_tools)}, Missing: {len(missing_tools)}")
    
    if missing_tools:
        print_header("Recommendations", "magenta")
        print(colored("\nTo manually install missing tools:", "cyan"))
        
        if pkg_manager == "apt":
            print(colored(f"\nsudo apt update", "yellow"))
            for tool, package in missing_tools:
                print(colored(f"sudo apt install -y {package}", "yellow"))
        else:  
            print(colored(f"\nsudo pacman -Sy", "yellow"))
            for tool, package in missing_tools:
                print(colored(f"sudo pacman -S --noconfirm {package}", "yellow"))
                
        print(colored("\nSome tools might be available through other sources:", "cyan"))
        print(colored("- For tools not in repositories, check GitHub repositories", "white"))
        print(colored("- Consider using pip: pip install theHarvester", "white"))
        print(colored("- For some tools, you might need to clone and build from source", "white"))
    
def handle_utility_functions():
    """Handle utility functions menu selection"""
    while True:
        clear_screen()
        option = show_utility_menu()
        
        if option == '1':
            import_target_list()
            input(colored("\nPress Enter to continue...", 'cyan'))
        elif option == '2':
            print(colored("\n[i] Export functionality will be implemented in future versions.", 'yellow'))
            input(colored("\nPress Enter to continue...", 'cyan'))
        elif option == '3':
            print(colored("\n[i] Checking dependencies...", 'cyan'))
            check_dependencies()
            input(colored("\nPress Enter to continue...", 'cyan'))
        elif option == 'b':
            break
        else:
            print(colored("\n[!] Invalid option. Please try again.", 'yellow'))
            input(colored("\nPress Enter to continue...", 'cyan'))

def main():
    """Main function to run the interactive menu"""
    os.makedirs("results", exist_ok=True)
    
    available_modules = load_modules()
    
    if not available_modules:
        print(colored("\n[!] No modules found. Please make sure phase*.py files are in the same directory.", 'red'))
        sys.exit(1)
    
    while True:
        clear_screen()
        option = show_main_menu(available_modules)
        
        if option == 'q':
            print(colored("\nExiting Toolkit. Goodbye!", 'cyan'))
            break
        elif option == 'u':
            handle_utility_functions()
        elif option == 'l':
            view_logs()
        elif option == 'c':
            clear_results()
        elif option.isdigit() and 1 <= int(option) <= len(available_modules):
            module_name = list(available_modules.keys())[int(option) - 1]
            module_info = available_modules[module_name]
            
            clear_screen()
            print_header(f"Executing {module_info['title']}", "blue")
            execute_module(module_name, module_info)
            
            input(colored("\nPress Enter to return to main menu...", 'cyan'))
        else:
            print(colored("\n[!] Invalid option. Please try again.", 'yellow'))
            input(colored("\nPress Enter to continue...", 'cyan'))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n\nOperation cancelled by user. Exiting...", 'yellow'))
    except Exception as e:
        logging.critical(f"Unhandled exception: {str(e)}")
        print(colored(f"\n[!] An unexpected error occurred: {str(e)}", 'red'))
        print(colored("Check the log file for more details.", 'red'))