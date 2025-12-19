import os
import sys
from pathlib import Path

def _default_log_file() -> Path:
    """
    Determine a writable default log file location.
    Prefer project root (alongside this file) when writable; otherwise fall back to XDG state.
    """
    repo_root = Path(__file__).resolve().parent.parent
    project_log = repo_root / "chat_history.jsonl"
    if project_log.parent.exists() and os.access(project_log.parent, os.W_OK):
        return project_log
    state_home = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
    return state_home / "deepseek-cli" / "chat_history.jsonl"


# Default configuration values
DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_LOG_FILE = _default_log_file()
DEFAULT_ENABLE_COLOR = sys.stdout.isatty()
DEFAULT_ENABLE_SPINNER = sys.stdout.isatty()
DEFAULT_STREAM = True  # Enable streaming by default
DEFAULT_VERSION = "1.0.2"
DEFAULT_VENV_PATH = None  # Default to system Python

# Color scheme configuration
# Available schemes: 'dracula', 'monokai', 'default'
DEFAULT_COLOR_SCHEME = "dracula"
# Available non-code color styles: 'plain', 'dim', 'highlight'
DEFAULT_NON_CODE_STYLE = "plain"

# Global configuration variables
SCRIPT_DIR = Path(__file__).resolve().parent
API_KEY = None
BASE_URL = None
MODEL = None
LOG_FILE = None
ENABLE_COLOR = None
SPINNER = None
STREAM = None
VENV_PATH = None
COLOR_SCHEME = None
NON_CODE_STYLE = None


def load_config(env=None):
    """
    Load configuration from environment variables with sensible defaults.
    
    Args:
        env (dict, optional): Environment variables to use for testing purposes.
    """
    global API_KEY, BASE_URL, MODEL, LOG_FILE, ENABLE_COLOR, SPINNER, STREAM, VENV_PATH, COLOR_SCHEME, NON_CODE_STYLE
    
    # Use provided environment or system environment
    env_vars = env if env is not None else os.environ
    
    # Load API key from environment
    API_KEY = env_vars.get("DEEPSEEK_API_KEY")
    
    # Load base URL from environment or use default
    BASE_URL = env_vars.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL)
    
    # Load model from environment or use default
    MODEL = env_vars.get("DEEPSEEK_MODEL", DEFAULT_MODEL)
    
    # Load log file path from environment or use default
    log_path = env_vars.get("DEEPSEEK_LOG_FILE")
    LOG_FILE = Path(log_path).expanduser() if log_path else SCRIPT_DIR.parent / DEFAULT_LOG_FILE
    
    # Load venv path from environment
    venv_path = env_vars.get("DEEPSEEK_VENV_PATH")
    VENV_PATH = Path(venv_path).expanduser() if venv_path else DEFAULT_VENV_PATH
    
    # Check if color output is disabled via environment variable
    ENABLE_COLOR = not bool(env_vars.get("DS_NO_COLOR")) and DEFAULT_ENABLE_COLOR
    SPINNER = not bool(env_vars.get("DS_NO_SPINNER")) and DEFAULT_ENABLE_SPINNER
    if env_vars.get("DS_SPINNER"):
        SPINNER = True
    
    # Load streaming preference from environment
    if env_vars.get("DS_NO_STREAM"):
        STREAM = False
    elif env_vars.get("DS_STREAM"):
        STREAM = True
    else:
        STREAM = DEFAULT_STREAM
    
    # Load color scheme from environment
    COLOR_SCHEME = env_vars.get("DEEPSEEK_COLOR_SCHEME", DEFAULT_COLOR_SCHEME)
    
    # Load non-code style from environment
    NON_CODE_STYLE = env_vars.get("DEEPSEEK_NON_CODE_STYLE", DEFAULT_NON_CODE_STYLE)


# Load configuration on import
load_config()
