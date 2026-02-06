from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme
import logging

# Define a custom theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "yellow",
    "error": "bold red",
    "request": "bold green",
    "response": "bold blue",
    "data": "magenta"
})

# Initialize console with theme
console = Console(theme=custom_theme)

def setup_logger():
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )
    return logging.getLogger("rich")

# Create a global logger instance
log = setup_logger()

def log_request(method, path, addr):
    console.print(f"[request]REQ[/] {method} {path} from {addr}")

def log_response(status_code, content_type, length):
    console.print(f"[response]RES[/] {status_code} ({content_type}) - {length} bytes")
