# Python包装器，用于Rust实现的染色器

from typing import Optional, Dict, List, Any

# 导入Rust实现的模块
_using_rust = False
_using_python_fallback = False

# 尝试导入Rust实现
try:
    from ._ds_highlighter import strip_ansi_py as strip_ansi
    from ._ds_highlighter import highlight_py as highlight
    from ._ds_highlighter import highlight_code_py as highlight_code
    _using_rust = True
    _using_python_fallback = False
    # print("使用Rust实现的高亮器")
except ImportError:
    # 如果Rust实现不可用，回退到Python实现
    try:
        from .highlighter import strip_ansi, highlight, highlight_code
        _using_rust = False
        _using_python_fallback = True
        # print("使用Python实现的高亮器")
    except ImportError as e:
        # 处理导入失败的情况
        print(f"无法导入任何高亮器实现: {e}")
        raise

# 导出这些函数
__all__ = ['strip_ansi', 'highlight', 'highlight_code', '_using_rust', '_using_python_fallback']

# 如果直接运行此文件，执行测试
if __name__ == "__main__":
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
