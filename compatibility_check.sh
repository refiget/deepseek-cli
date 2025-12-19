#!/bin/bash

# DeepSeek CLI 跨平台兼容性检查脚本
# 用于验证 ds 命令在不同操作系统上的工作情况

echo "========================================"
echo "DeepSeek CLI 跨平台兼容性检查"
echo "========================================"

# 检查操作系统类型
OS_TYPE="$(uname -s)"
echo "当前操作系统: $OS_TYPE"
echo

# 检查 Python 版本
echo "1. 检查 Python 版本:"
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 未安装或不在 PATH 中"
    exit 1
fi
echo "✅ Python 3 已安装"
echo

# 检查 ds 命令是否可用
echo "2. 检查 ds 命令是否可用:"
which ds
if [ $? -ne 0 ]; then
    echo "❌ ds 命令未找到，请确保已安装并在 PATH 中"
    exit 1
fi
echo "✅ ds 命令已找到"
echo

# 测试 ds 版本命令
echo "3. 测试 ds 版本命令:"
ds --version
if [ $? -ne 0 ]; then
    echo "❌ ds --version 命令执行失败"
    exit 1
fi
echo "✅ ds --version 命令执行成功"
echo

# 测试基本聊天功能
echo "4. 测试基本聊天功能:"
echo "Hello" | ds "Say hi back"
if [ $? -ne 0 ]; then
    echo "❌ 基本聊天功能测试失败"
else
    echo "✅ 基本聊天功能测试成功"
fi
echo

# 测试拼写纠正功能
echo "5. 测试拼写纠正功能:"
ds --spell "Ths is a test of the spell checker"
if [ $? -ne 0 ]; then
    echo "❌ 拼写纠正功能测试失败"
else
    echo "✅ 拼写纠正功能测试成功"
fi
echo

# 测试翻译功能
echo "6. 测试翻译功能:"
ds "Hello world" --trans
if [ $? -ne 0 ]; then
    echo "❌ 翻译功能测试失败"
else
    echo "✅ 翻译功能测试成功"
fi
echo

# 检查环境变量设置
echo "7. 检查环境变量设置:"
echo "DEEPSEEK_API_KEY 设置情况: $(if [ -n "$DEEPSEEK_API_KEY" ]; then echo "已设置"; else echo "未设置"; fi)"
echo "DS_NO_COLOR 设置情况: $(if [ -n "$DS_NO_COLOR" ]; then echo "已设置"; else echo "未设置"; fi)"
echo

# 检查虚拟环境
echo "8. 检查虚拟环境:"
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ 正在使用虚拟环境: $VIRTUAL_ENV"
else
    echo "ℹ️  未使用虚拟环境"
fi
echo

# 检查日志文件创建
echo "9. 检查日志文件创建:"
LOG_DIR="$(dirname "$(python3 -c "from pathlib import Path; from ds.config import LOG_FILE; print(LOG_FILE)")")"
echo "日志目录: $LOG_DIR"
mkdir -p "$LOG_DIR"
touch "$LOG_DIR/test.log"
if [ $? -eq 0 ]; then
    echo "✅ 日志目录可写入"
    rm "$LOG_DIR/test.log"
else
    echo "❌ 日志目录不可写入"
fi
echo

# 检查 ANSI 颜色支持
echo "10. 检查 ANSI 颜色支持:"
echo -e "\033[91m红色\033[0m \033[92m绿色\033[0m \033[93m黄色\033[0m \033[94m蓝色\033[0m"
echo "如果您看到彩色文本，则 ANSI 颜色支持正常"
echo

echo "========================================"
echo "兼容性检查完成！"
echo "========================================"
echo
