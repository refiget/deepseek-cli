#!/usr/bin/env python3
"""
DeepSeek CLI (ds) - A command-line interface for DeepSeek API.

This package provides a modular implementation of the DeepSeek CLI with:
- Interactive and non-interactive modes
- Multiple modes: normal, spell correction, translation
- Dracula theme syntax highlighting for Python code
- ANSI color support with toggle options
- API key validation
- Streaming response support

Version: 1.0.2
"""

from .version import __version__
from .config import load_config
from .chat import chat
from .utils import render_content, strip_ansi

__all__ = [
    "__version__",
    "load_config",
    "chat",
    "render_content",
    "strip_ansi"
]
