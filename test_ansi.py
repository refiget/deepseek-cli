#!/usr/bin/env python3
"""
Independent test script to verify ANSI color codes work in terminal.
"""

# ANSI color codes
COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m"
}

print("Testing ANSI color codes:")
print("========================")

# Test basic colors
print(f"{COLORS['red']}Red text{COLORS['reset']}")
print(f"{COLORS['green']}Green text{COLORS['reset']}")
print(f"{COLORS['yellow']}Yellow text{COLORS['reset']}")
print(f"{COLORS['blue']}Blue text{COLORS['reset']}")
print(f"{COLORS['magenta']}Magenta text{COLORS['reset']}")
print(f"{COLORS['cyan']}Cyan text{COLORS['reset']}")
print(f"{COLORS['white']}White text{COLORS['reset']}")

print("\nTesting Python syntax highlighting:")
print("===============================")

code = '''def hello():
    # This is a comment
    print("Hello, world!")
    return 42
'''

# Apply simple syntax highlighting
# Strings in yellow
code = code.replace('"Hello, world!"', COLORS['yellow'] + '"Hello, world!"' + COLORS['reset'])
# Comments in magenta
code = code.replace('# This is a comment', COLORS['magenta'] + '# This is a comment' + COLORS['reset'])
# Keywords in cyan
code = code.replace('def', COLORS['cyan'] + 'def' + COLORS['reset'])
code = code.replace('return', COLORS['cyan'] + 'return' + COLORS['reset'])
# Function calls in green
code = code.replace('print', COLORS['green'] + 'print' + COLORS['reset'])
# Numbers in blue
code = code.replace('42', COLORS['blue'] + '42' + COLORS['reset'])


print(code)

print("\nIf you can see different colors above, then ANSI color codes are working in your terminal!")
