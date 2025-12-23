#!/usr/bin/env python3
"""
Test script to verify color rendering is working correctly.
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ds.config import ENABLE_COLOR, COLOR_SCHEME, NON_CODE_STYLE
from ds.utils import render_content, strip_ansi

# Test content with code and non-code parts
test_content = '''这是一段普通文本。

```python
def hello():
    print("Hello, world!")
    return 42
```

这是另一部分普通文本。'''

print(f"ENABLE_COLOR: {ENABLE_COLOR}")
print(f"COLOR_SCHEME: {COLOR_SCHEME}")
print(f"NON_CODE_STYLE: {NON_CODE_STYLE}")
print("-" * 50)

# Test rendering with color enabled
print("Rendering with color enabled:")
rendered = render_content(test_content, enable_color=True, theme_name='dracula', non_code_style='plain')
print(f"Rendered output length: {len(rendered)}")
print(f"Contains ANSI codes: {len(strip_ansi(rendered)) != len(rendered)}")
print(rendered)
print("-" * 50)

# Test rendering with color disabled
print("Rendering with color disabled:")
rendered = render_content(test_content, enable_color=False, theme_name='dracula', non_code_style='plain')
print(f"Rendered output length: {len(rendered)}")
print(f"Contains ANSI codes: {len(strip_ansi(rendered)) != len(rendered)}")
print(rendered)
