#!/usr/bin/env python3

# 直接测试Rust编译的模块
import sys
import os

# 将ds目录添加到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ds'))

try:
    # 直接导入Rust编译的模块
    import _ds_highlighter
    print("成功导入Rust模块")
    
    # 测试strip_ansi函数
    print("\n=== 测试 strip_ansi ===")
    input_text = "\x1B[31mHello\x1B[0m World"
    result = _ds_highlighter.strip_ansi_py(input_text)
    print(f"输入: {input_text}")
    print(f"输出: {result}")
    
    # 测试highlight_code函数
    print("\n=== 测试 highlight_code ===")
    code = '''def hello():
    # This is a comment
    print("Hello World")
    return 42'''
    result = _ds_highlighter.highlight_code_py(code, "dracula")
    print(f"原始代码:")
    print(code)
    print(f"\n高亮代码:")
    print(result)
    
    # 测试highlight函数
    print("\n=== 测试 highlight ===")
    content = '''Some text
```python
def hello():
    print("Hello")
```
More text'''
    result = _ds_highlighter.highlight_py(content, "monokai")
    print(f"原始内容:")
    print(content)
    print(f"\n高亮内容:")
    print(result)
    
except ImportError as e:
    print(f"导入Rust模块失败: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"测试过程中出错: {e}")
    import traceback
    traceback.print_exc()
