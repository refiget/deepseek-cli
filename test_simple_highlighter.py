#!/usr/bin/env python3

# 直接测试ds_highlighter模块，避免加载所有依赖
import sys
import os

# 将ds目录添加到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ds'))

# 直接导入ds_highlighter模块
from ds_highlighter import strip_ansi, highlight, highlight_code, _using_rust, _using_python_fallback

# 测试strip_ansi函数
print("=== 测试 strip_ansi ===")
input_text = "\x1B[31mHello\x1B[0m World"
result = strip_ansi(input_text)
print(f"输入: {input_text}")
print(f"输出: {result}")
print(f"使用Rust实现: {_using_rust}")
print(f"使用Python回退: {_using_python_fallback}")
print()

# 测试highlight_code函数
print("=== 测试 highlight_code ===")
code = '''def hello():
    # This is a comment
    print("Hello World")
    return 42'''
result = highlight_code(code, "dracula")
print(f"原始代码:")
print(code)
print(f"\n高亮代码:")
print(result)
print()

# 测试highlight函数
print("=== 测试 highlight ===")
content = '''Some text
```python
def hello():
    print("Hello")
```
More text'''
result = highlight(content, "monokai")
print(f"原始内容:")
print(content)
print(f"\n高亮内容:")
print(result)
