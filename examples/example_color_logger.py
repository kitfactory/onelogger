from onelogger import Logger
import os
import sys
import platform

# Enable ANSI colors on Windows
# Windowsの場合、ANSIカラーを有効化
if platform.system() == 'Windows':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Configure environment variables
os.environ.update({
    "LOG_LEVEL": "DEBUG",
    "LOG_OUTPUT": "both",
    "LOG_FILE_PATH": "color_example.log",
    "LOG_FORMAT": "plain",
    "LOG_STRIP_COLORS": "true"  # Strip colors for file output
})

# Get logger instance
logger = Logger.get_logger("color_example")

# Define some ANSI color codes
class Colors:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

    @classmethod
    def init(cls):
        """
        Initialize color support based on platform and environment
        プラットフォームと環境に基づいてカラーサポートを初期化
        """
        # Disable colors if not supported
        if not sys.stdout.isatty() or os.environ.get('NO_COLOR'):
            cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = cls.RESET = ''

# Initialize colors
Colors.init()

# Log messages with colors
logger.info(f"{Colors.GREEN}Success:{Colors.RESET} Operation completed successfully")
logger.warning(f"{Colors.YELLOW}Warning:{Colors.RESET} Resource usage is high")
logger.error(f"{Colors.RED}Error:{Colors.RESET} Failed to connect to server")
logger.info(f"{Colors.BLUE}Info:{Colors.RESET} System status is normal") 