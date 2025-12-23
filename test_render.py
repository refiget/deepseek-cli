#!/usr/bin/env python3
"""
Simple test script to verify color rendering is working.
"""
import sys

# Add the project root to Python path
sys.path.insert(0, '/Users/mac/Projects/Trae-projects/deepseek-cli')

from ds.utils import render_content

# Test with a simple Python code example
test_content = '''这是一段普通文本。

```python
def hello():
    # 这是一个注释
    print("Hello, world!")
    return 42
```

这是另一部分普通文本。'''

# Test with enable_color=True
print("\n--- Testing with enable_color=True ---")
rendered = render_content(test_content, enable_color=True, theme_name='dracula', non_code_style='plain')
print(rendered)

# Test with enable_color=False
print("\n--- Testing with enable_color=False ---")
rendered = render_content(test_content, enable_color=False, theme_name='dracula', non_code_style='plain')
print(rendered)
