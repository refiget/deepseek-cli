#!/bin/bash
# 安装脚本：使用 pipx 安装 DeepSeek CLI

echo "正在安装 DeepSeek CLI (ds)..."
echo ""

# 检查是否在正确的目录
if [ ! -f "setup.py" ]; then
    echo "错误：请在项目根目录下运行此脚本！"
    echo "请先进入 deepseek-cli 目录，然后执行 ./install.sh"
    exit 1
fi

# 检查 pipx 是否已安装
if ! command -v pipx &> /dev/null; then
    echo "正在安装 pipx..."
    pip install --user pipx
    pipx ensurepath
    echo "pipx 安装完成！"
    echo ""
    echo "请重新打开终端或执行 source ~/.bashrc（或 ~/.zshrc）后重试安装！"
    exit 1
fi

# 使用 pipx 安装项目
echo "正在使用 pipx 安装 DeepSeek CLI..."
pipx install -e . --verbose

if [ $? -eq 0 ]; then
    echo ""
    echo "DeepSeek CLI 安装成功！"
    echo ""
    echo "使用说明："
    echo "1. 首先设置 API Key 环境变量："
    echo "   export DEEPSEEK_API_KEY='your_api_key_here'"
    echo "   （建议添加到 ~/.bashrc 或 ~/.zshrc 中持久化）"
    echo ""
    echo "2. 使用 ds 命令："
    echo "   ds ask "你的问题""
    echo ""
    echo "3. 使用 ds-nvim 命令（Neovim 集成）："
    echo "   ds-nvim ask "你的问题""
    echo ""
    echo "如需添加额外依赖，可以使用 pipx inject："
    echo "   pipx inject ds-cli <dependency>"
    echo ""
else
    echo ""
    echo "安装失败！请检查错误信息并重试。"
    exit 1
fi