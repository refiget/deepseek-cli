#!/usr/bin/env python3
"""
DeepSeek CLI Neovim 集成模块
提供 ds-nvim 命令，用于 Neovim 中调用 DeepSeek API
"""

import sys
import argparse
import re
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from ds.chat import DeepSeekChat
from ds.config import load_config, API_KEY, BASE_URL, MODEL, LOG_FILE, ENABLE_COLOR, SPINNER, STREAM

# 确保配置已加载
load_config()

def ds_ask(query: str, concise: bool = True) -> str:
    """
    向 DeepSeek 提问
    
    Args:
        query: 查询内容
        concise: 是否返回简洁结果
        
    Returns:
        DeepSeek 响应内容
    """
    chat = DeepSeekChat()
    
    pass
    
    if concise:
        query = f"请用最简洁的方式回答，直接给答案，不要解释过程，不要用礼貌用语：{query}"
    
    response = chat.chat(query)
    return response

def ds_review_code(code: str, filetype: str = "python") -> str:
    """
    让 DeepSeek 检查代码
    
    Args:
        code: 代码内容
        filetype: 文件类型
        
    Returns:
        DeepSeek 响应内容
    """
    chat = DeepSeekChat()
    
    pass
    
    prompt = [
        f"直接指出以下{filetype}代码的问题，给出修改后的代码。",
        "要求：1. 列出关键问题（不超过3点） 2. 直接给出修改后的代码 3. 不要解释原理",
        "",
        "代码：",
        code,
        "",
        "请按这个格式回答：[问题列表] [修改后的代码]"
    ]
    
    response = chat.chat("\n".join(prompt))
    return response

def ds_generate_doctest(code: str, filetype: str = "python") -> str:
    """
    生成 doctest 示例
    
    Args:
        code: 代码内容
        filetype: 文件类型
        
    Returns:
        DeepSeek 响应内容
    """
    chat = DeepSeekChat()
    
    pass
    
    prompt = [
        f"你是 {filetype} 助教，请基于下面的代码编写 doctest 示例。",
        "只返回 doctest 片段：包含函数调用、输入与预期输出，不要解释，不要其他文字。",
        code,
    ]
    
    response = chat.chat("\n".join(prompt))
    return response

def clean_output(output: str, remove_color: bool = True) -> str:
    """
    清理输出内容，移除不必要的标记
    
    Args:
        output: 原始输出内容
        remove_color: 是否移除 ANSI 颜色代码
        
    Returns:
        清理后的输出内容
    """
    # 根据参数决定是否移除 ANSI 颜色代码
    if remove_color:
        output = re.sub(r'\x1b\[[0-9;]*m', '', output)
    # 移除 Markdown 代码围栏
    output = re.sub(r'^```[a-zA-Z]*\n?', '', output)
    output = re.sub(r'\n?```$', '', output)
    # 移除主题说明
    output = re.sub(r'^\s*\-\-\-.*?\n', '', output, flags=re.MULTILINE)
    # 移除空行
    output = re.sub(r'\n\s*\n', '\n', output)
    # 移除首尾空白
    return output.strip()

def main() -> None:
    """
    主函数，处理命令行参数
    """
    parser = argparse.ArgumentParser(
        prog="ds-nvim",
        description="DeepSeek CLI Neovim 集成工具",
        epilog="使用示例: ds-nvim ask --concise \"你好\""
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, 
                                      help="子命令帮助")
    
    # ask 子命令
    parser_ask = subparsers.add_parser("ask", help="向 DeepSeek 提问")
    parser_ask.add_argument("query", help="查询内容")
    parser_ask.add_argument("--concise", action="store_true", default=True, 
                           help="返回简洁结果（默认开启）")
    parser_ask.add_argument("--verbose", action="store_true", 
                           help="返回详细结果")
    
    # review 子命令
    parser_review = subparsers.add_parser("review", help="让 DeepSeek 检查代码")
    parser_review.add_argument("--code", help="代码内容")
    parser_review.add_argument("--file", help="代码文件路径")
    parser_review.add_argument("--filetype", default="python", 
                              help="代码文件类型（默认：python）")
    
    # doctest 子命令
    parser_doctest = subparsers.add_parser("doctest", 
                                          help="生成 doctest 示例")
    parser_doctest.add_argument("--code", help="代码内容")
    parser_doctest.add_argument("--file", help="代码文件路径")
    parser_doctest.add_argument("--filetype", default="python", 
                               help="代码文件类型（默认：python）")
    
    args = parser.parse_args()
    
    try:
        # 根据命令类型执行不同的函数
        if args.command == "ask":
            # 如果是 ask 命令，直接使用 query 参数
            result = ds_ask(args.query, args.concise and not args.verbose)
        elif args.command == "review":
            # 获取代码内容
            if args.code:
                code = args.code
            elif args.file:
                with open(args.file, "r", encoding="utf-8") as f:
                    code = f.read()
            else:
                print("错误: 必须提供 --code 或 --file 参数", file=sys.stderr)
                sys.exit(1)
            result = ds_review_code(code, args.filetype)
        elif args.command == "doctest":
            # 获取代码内容
            if args.code:
                code = args.code
            elif args.file:
                with open(args.file, "r", encoding="utf-8") as f:
                    code = f.read()
            else:
                print("错误: 必须提供 --code 或 --file 参数", file=sys.stderr)
                sys.exit(1)
            result = ds_generate_doctest(code, args.filetype)
        else:
            print(f"错误: 未知命令 {args.command}", file=sys.stderr)
            sys.exit(1)
        
        # 根据命令类型决定是否移除颜色代码
        # ask和review命令保持染色功能，doctest命令移除颜色
        if args.command == 'doctest':
            print(clean_output(result, remove_color=True))
        else:
            print(clean_output(result, remove_color=False))
        
    except KeyboardInterrupt:
        print("\n操作已取消", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"错误: 文件未找到: {e}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"错误: 权限不足: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()