#!/bin/bash

# DeepSeek CLI Neovim 模块化安装脚本
# 适用于将 DeepSeek 功能集成到模块化的 Neovim 配置中

# 配置路径（根据用户的实际情况修改）
DEEPSEEK_CLI_PATH="$(pwd)"
DOTFILES_NVIM_PATH="$HOME/dotfiles/nvim"
USER_MODULE_DIR="$DOTFILES_NVIM_PATH/lua/user"

# 确保目录存在
mkdir -p "$USER_MODULE_DIR"

# 复制 deepseek.lua 到 user 目录
cp "$DEEPSEEK_CLI_PATH/deepseek.lua" "$USER_MODULE_DIR/"

echo "✅ 已将 deepseek.lua 复制到 $USER_MODULE_DIR/"
echo ""
echo "请按照以下步骤完成配置："
echo "1. 打开你的 init.lua 文件"
echo "2. 在用户模块加载部分添加：require('user.deepseek')"
echo "3. 重启 Neovim"
echo ""
echo "示例配置："
echo "require('user.core')"
echo "require('user.plugins')"
echo "require('user.keymaps')"
echo "require('user.deepseek')  -- 添加这一行"
echo ""
echo "配置完成后，你可以使用以下按键："
echo "- <leader>dq: 向 DeepSeek 提问"
echo "- <leader>dr: 审查选中的代码（可视模式）"
echo "- <leader>dt: 生成当前缓冲区的 doctest"
