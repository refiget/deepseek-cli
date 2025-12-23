#!/usr/bin/env python3
"""
Debug script to trace the complete flow from chat call to final output.
"""
import sys
import os
import re

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ds.chat import DeepSeekChat
from ds.config import load_config, ENABLE_COLOR
from ds.utils import render_content, strip_ansi
from ds.nvim import clean_output

# Load configuration
load_config()

print(f"ENABLE_COLOR: {ENABLE_COLOR}")
print("=" * 50)

# Test chat call
chat = DeepSeekChat()
query = "Review the following Python code: def add(a, b): return a + b"

print("Calling chat()...")
response = chat.chat(query)

print("\nRaw response from chat():")
print(f"Length: {len(response)}")
print(f"Contains ANSI codes: {len(strip_ansi(response)) != len(response)}")
print(f"Response: {response}")
print("=" * 50)

# Test clean_output with remove_color=False
print("Testing clean_output(remove_color=False):")
cleaned = clean_output(response, remove_color=False)
print(f"Length: {len(cleaned)}")
print(f"Contains ANSI codes: {len(strip_ansi(cleaned)) != len(cleaned)}")
print(f"Cleaned: {cleaned}")
print("=" * 50)

# Test clean_output with remove_color=True
print("Testing clean_output(remove_color=True):")
cleaned_no_color = clean_output(response, remove_color=True)
print(f"Length: {len(cleaned_no_color)}")
print(f"Contains ANSI codes: {len(strip_ansi(cleaned_no_color)) != len(cleaned_no_color)}")
print(f"Cleaned (no color): {cleaned_no_color}")
print("=" * 50)
