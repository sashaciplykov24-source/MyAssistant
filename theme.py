try:
    from colorama import Fore, Style, init

    init()

    USER = Fore.GREEN
    AI = Fore.CYAN
    SYSTEM = Fore.YELLOW
    ERROR = Fore.RED
    RESET = Style.RESET_ALL
except ImportError:
    USER = ""
    AI = ""
    SYSTEM = ""
    ERROR = ""
    RESET = ""
