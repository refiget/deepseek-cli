#!/usr/bin/env python3
import argparse
import sys
import os
from pathlib import Path

# Allow running as a standalone script (e.g., `python ds/__main__.py`)
if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    __package__ = "ds"

from ds.version import __version__
from ds.chat import chat
from ds.config import ENABLE_COLOR
from ds.utils import format_error_message


def main():
    """
    Main function for the ds CLI.
    """
    # Create argument parser
    parser = argparse.ArgumentParser(
        prog="ds",
        description="DeepSeek CLI - A command-line interface for DeepSeek API"
    )
    
    # Define arguments
    parser.add_argument("-s", "--spell", action="store_true", help="Spell correction mode")
    parser.add_argument("-t", "--trans", nargs="?", const="Chinese", help="Translation mode (default: Chinese)")
    parser.add_argument("-v", "--version", action="version", version=f"ds v{__version__}")
    parser.add_argument("-nc", "--no-color", action="store_true", help="Disable color output")
    parser.add_argument("-ns", "--no-stream", action="store_true", help="Disable streaming output")
    parser.add_argument("-st", "--stream", action="store_true", help="Enable streaming output")
    parser.add_argument("--theme", choices=["dracula", "monokai", "default"], help="Code highlighting theme")
    parser.add_argument("--non-code-style", choices=["plain", "dim", "highlight"], help="Style for non-code text")
    parser.add_argument("-e", "--venv", help="Specify Python virtual environment path")
    parser.add_argument("query", nargs="+", help="Query for DeepSeek API")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle configuration options that affect environment variables
    config_changes = {
        "DEEPSEEK_VENV_PATH": args.venv,
        "DS_NO_COLOR": "1" if args.no_color else None,
        "DS_NO_STREAM": "1" if args.no_stream else None,
        "DS_STREAM": "1" if args.stream else None,
        "DEEPSEEK_COLOR_SCHEME": args.theme,
        "DEEPSEEK_NON_CODE_STYLE": args.non_code_style
    }
    
    # Apply configuration changes to environment
    config_changed = False
    for key, value in config_changes.items():
        if value is not None:
            os.environ[key] = value
            config_changed = True
    
    # Reload config if any configuration changed
    if config_changed:
        from .config import load_config
        load_config()
    
    # Determine operation mode
    mode = "normal"
    language = "English"
    
    if args.spell:
        mode = "spell"
    elif args.trans is not None:
        mode = "trans"
        # Simplify translation to only support English and Chinese
        if args.trans.lower() in ['en', 'english']:
            language = "English"
        else:
            # Default to Chinese for any other input or when no specific language is provided
            language = "Chinese"
    
    # Join query arguments
    query = " ".join(args.query)
    
    # Execute chat - no need to pass stream explicitly, it will use config
    try:
        chat(query, mode, language)
    except Exception as e:
        error_msg = format_error_message("Error", str(e), ENABLE_COLOR)
        print(error_msg, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
