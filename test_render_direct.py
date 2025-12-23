#!/usr/bin/env python3

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ds.utils import render_content, strip_ansi

# Test content with code blocks
content = '''
这是一段普通文本。

```python
def add(a, b):
    """This is a docstring."""
    return a + b

result = add(1, 2)
# This is a comment
print(f"Result: {result}")
```

这是另一段普通文本。
'''

print("Testing render_content function directly:")
print("=" * 50)

# Test with color enabled
print("With color enabled:")
print("-" * 30)
rendered = render_content(content, enable_color=True, theme_name="dracula", non_code_style="plain")
print(f"Contains ANSI codes: {len(strip_ansi(rendered)) != len(rendered)}")
print("Rendered content:")
print(rendered)

print("\n" + "=" * 50)

# Test with color disabled
print("With color disabled:")
print("-" * 30)
rendered_no_color = render_content(content, enable_color=False, theme_name="dracula", non_code_style="plain")
print(f"Contains ANSI codes: {len(strip_ansi(rendered_no_color)) != len(rendered_no_color)}")
print("Rendered content:")
print(rendered_no_color)
