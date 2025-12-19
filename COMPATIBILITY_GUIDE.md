# DeepSeek CLI 跨平台兼容性指南

本文档提供了DeepSeek CLI在Arch Linux和macOS操作系统上的兼容性信息和最佳实践。

## 系统要求

### 共同要求
- Python 3.6 或更高版本
- 有效的 DeepSeek API 密钥
- 网络连接（用于API调用）

### Arch Linux 额外要求
- `python3` 包
- `python3-pip` 包
- `python3-virtualenv` 包（可选，但推荐）

### macOS 额外要求
- Xcode Command Line Tools（推荐安装）

## 安装指南

### 虚拟环境设置

在两个操作系统上，推荐使用相同的虚拟环境结构：

```bash
# 创建虚拟环境（两个平台相同）
mkdir -p ~/venvs
cd ~/venvs
python3 -m venv deepseek-cli

# 激活虚拟环境
# Arch Linux 和 macOS 相同
source ~/venvs/deepseek-cli/bin/activate

# 安装 DeepSeek CLI
cd ~/Projects/Trae-projects/deepseek-cli
pip install -e .
```

## 环境变量

在两个操作系统上设置相同的环境变量：

```bash
# 设置 DeepSeek API 密钥
export DEEPSEEK_API_KEY="your-api-key-here"

# 可选：禁用彩色输出（如果终端不支持）
# export DS_NO_COLOR="1"

# 将环境变量添加到 shell 配置文件
# Arch Linux: ~/.bashrc 或 ~/.zshrc
# macOS: ~/.bash_profile 或 ~/.zshrc
echo 'export DEEPSEEK_API_KEY="your-api-key-here"' >> ~/.zshrc
```

## 兼容性检查

使用提供的兼容性检查脚本验证安装：

```bash
cd ~/Projects/Trae-projects/deepseek-cli
chmod +x compatibility_check.sh
./compatibility_check.sh
```

该脚本将检查：
- Python 版本
- ds 命令可用性
- 基本聊天功能
- 拼写纠正功能
- 翻译功能
- 环境变量设置
- 虚拟环境配置
- 日志文件创建权限
- ANSI 颜色支持

## 已知差异和解决方案

### 文件系统路径

DeepSeek CLI 使用 Python 的 `pathlib` 库处理文件路径，该库在两个平台上表现一致。

### 终端行为

- **Arch Linux**：默认终端通常是 `bash`
- **macOS**：默认终端通常是 `zsh`

确保在相应的 shell 配置文件中设置环境变量。

### 快捷键配置（Neovim）

`keymaps.lua` 文件在两个平台上完全兼容，因为它使用标准的 Neovim API。

## 故障排除

### ds 命令未找到

```bash
# 确保虚拟环境已激活
source ~/venvs/deepseek-cli/bin/activate

# 重新安装 DeepSeek CLI
cd ~/Projects/Trae-projects/deepseek-cli
pip install -e .

# 检查 ds 命令路径
which ds
```

### API 密钥错误

```bash
# 验证 API 密钥是否设置正确
echo $DEEPSEEK_API_KEY

# 重新设置 API 密钥
export DEEPSEEK_API_KEY="your-api-key-here"
```

### Python 版本问题

```bash
# 检查 Python 版本
python3 --version

# 在 Arch Linux 上安装最新 Python
sudo pacman -S python3

# 在 macOS 上安装最新 Python
brew install python3
```

## 性能优化

1. **使用虚拟环境**：隔离依赖，避免版本冲突
2. **设置合理的超时时间**：在 `config.py` 中调整 API 超时设置
3. **清理日志文件**：定期清理日志目录以节省磁盘空间
4. **使用本地缓存**：考虑添加本地缓存机制以减少重复 API 调用

## 结论

DeepSeek CLI 设计为完全跨平台兼容，在 Arch Linux 和 macOS 上提供一致的用户体验。通过遵循本文档中的指南，您可以确保在两个操作系统上获得最佳性能和可靠性。

如果您遇到任何兼容性问题，请使用 `compatibility_check.sh` 脚本进行诊断，并查看项目的 GitHub Issues 页面寻求帮助。
