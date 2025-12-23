#!/usr/bin/env python3

# ANSI escape sequences for colors
COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "reset": "\033[0m"
}

# Test each color
print("Testing ANSI colors:")
print("=" * 30)

for color_name, color_code in COLORS.items():
    if color_name != "reset":
        print(f"{color_code}{color_name}{COLORS['reset']} text")

# Test syntax highlighting elements
print("\nTesting syntax highlighting elements:")
print("=" * 30)

# String
print(f"String: {COLORS['yellow']}\"Hello World\"{COLORS['reset']}")

# Comment
print(f"Comment: {COLORS['magenta']}# This is a comment{COLORS['reset']}")

# Keyword
print(f"Keyword: {COLORS['cyan']}def{COLORS['reset']} function_name():")

# Function call
print(f"Function: {COLORS['green']}print{COLORS['reset']}({COLORS['yellow']}\"Hello\"{COLORS['reset']})")

# Number
print(f"Number: {COLORS['blue']}42{COLORS['reset']}")

# Test a complete Python line
print("\nTesting complete Python line:")
print("=" * 30)

python_line = f"{COLORS['cyan']}def{COLORS['reset']} {COLORS['green']}add{COLORS['reset']}(a, b):"
python_line += f" {COLORS['cyan']}return{COLORS['reset']} a {COLORS['red']}+{COLORS['reset']} b"
print(python_line)
