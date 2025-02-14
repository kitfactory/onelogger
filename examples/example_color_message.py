from onelogger import Logger
import os

# Configure environment variables
os.environ.update({
    "LOG_LEVEL": "DEBUG",
    "LOG_OUTPUT": "both",
    "LOG_FILE_PATH": "color_message.log",
    "LOG_FORMAT": "plain",
    "LOG_STRIP_COLORS": "true"  # Strip colors for file output
})

# Get logger instance
logger = Logger.get_logger("color_message")

# Define ANSI color codes
class Colors:
    # Basic colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    
    # Styles
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
    # Background colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    
    # Reset
    RESET = "\033[0m"

# Example usage with different color combinations
logger.info(f"{Colors.GREEN}✔ Success:{Colors.RESET} Operation completed")
logger.warning(f"{Colors.YELLOW}⚠ Warning:{Colors.RESET} Disk usage is {Colors.BOLD}85%{Colors.RESET}")
logger.error(f"{Colors.RED}✖ Error:{Colors.RESET} Connection failed")

# Using background colors
logger.info(f"{Colors.BG_RED}{Colors.WHITE}CRITICAL{Colors.RESET} System update required")

# Using multiple styles
logger.info(f"{Colors.BLUE}{Colors.BOLD}Notice:{Colors.RESET} "
           f"New version {Colors.BRIGHT_GREEN}2.0.0{Colors.RESET} is available")

# Using colors in status messages
status_msg = (
    f"{Colors.CYAN}Status Report:{Colors.RESET}\n"
    f"  {Colors.GREEN}✔{Colors.RESET} Database: Connected\n"
    f"  {Colors.RED}✖{Colors.RESET} Cache: Offline\n"
    f"  {Colors.YELLOW}⚠{Colors.RESET} Memory: 75% used"
)
logger.info(status_msg)

# Progress indication
logger.info(f"{Colors.BRIGHT_BLUE}Processing...{Colors.RESET} "
           f"[{Colors.BRIGHT_GREEN}==================>{Colors.RESET}] "
           f"{Colors.BOLD}90%{Colors.RESET}") 