import sys
from ds.utils import render_content, strip_ansi

# Test content with both code and non-code parts
test_content = '''Here's a simple Python function to add two numbers:

```python
def add_numbers(a, b):
    """Return the sum of two numbers."""
    return a + b
```

Usage example:
```python
result = add_numbers(5, 3)
print(result)  # Output: 8
```
'''

# Render content with color
rendered_content = render_content(test_content, enable_color=True)

print("Rendered content (with ANSI codes):")
print(repr(rendered_content))
print()
print("Rendered content (displayed):")
print(rendered_content)
print()
print("Content without ANSI codes:")
print(strip_ansi(rendered_content))