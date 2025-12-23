#!/usr/bin/env python3

import re
from typing import List, Tuple

# Copy the essential parts from utils.py

# ANSI escape sequences for colors
COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m",
    "dim": "\033[2m",
    "bold": "\033[1m"
}

# Regex patterns for syntax highlighting
STRING_RE = re.compile(r'(".*?"|\'.*?\')', re.DOTALL)
COMMENT_RE = re.compile(r'(#.*$)', re.MULTILINE)
KEYWORD_RE = re.compile(r'\b(def|class|if|elif|else|for|while|try|except|finally|return|import|from|as|with|yield|raise|pass|break|continue|lambda|and|or|not|is|in|None|True|False)\b')

# Mock apply_syntax_highlighting function
def apply_syntax_highlighting(code: str, enable_color: bool = True) -> str:
    """
    Simple syntax highlighting function for testing.
    """
    if not enable_color:
        return code
    
    highlighted_code = code
    
    # Apply highlighting in order of priority
    # 1. Strings
    highlighted_code = STRING_RE.sub(lambda m: f"{COLORS['yellow']}{m.group(1)}{COLORS['reset']}", highlighted_code)
    
    # 2. Comments
    highlighted_code = COMMENT_RE.sub(lambda m: f"{COLORS['magenta']}{m.group(1)}{COLORS['reset']}", highlighted_code)
    
    # 3. Keywords
    highlighted_code = KEYWORD_RE.sub(lambda m: f"{COLORS['cyan']}{m.group(1)}{COLORS['reset']}", highlighted_code)
    
    return highlighted_code

# Test the syntax highlighting
print("Testing syntax highlighting:")
print("=" * 50)

code = '''def add(a, b):
    """This is a docstring."""
    return a + b

result = add(1, 2)
# This is a comment
print(f"Result: {result}")'''

print("Original code:")
print(code)
print("\nWith syntax highlighting:")
print(apply_syntax_highlighting(code, enable_color=True))
print("\nWithout syntax highlighting:")
print(apply_syntax_highlighting(code, enable_color=False))
