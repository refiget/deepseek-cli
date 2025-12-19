#!/bin/bash
# DeepSeek CLI 全局包装脚本

# 默认虚拟环境路径
DEFAULT_VENV="/Users/mac/venvs/deepseek-cli"

# 配置文件路径
CONFIG_FILE="$HOME/.config/deepseek-cli/config.env"

# 加载配置文件（如果存在）
if [ -f "$CONFIG_FILE" ]; then
  source "$CONFIG_FILE"
fi

# 控制输出的详细程度：设置 DS_CLI_VERBOSE 时输出额外信息
VERBOSE="${DS_CLI_VERBOSE:-${DS_VERBOSE:-}}"

# 获取虚拟环境路径的优先级顺序：
# 1. 命令行参数 -e/--venv（如果支持）
# 2. 环境变量 DS_CLI_VENV
# 3. 配置文件中的 DEEPSEEK_VENV_PATH
# 4. 环境变量 VIRTUAL_ENV（当前激活的虚拟环境）
# 5. 默认虚拟环境路径

# 解析命令行参数，检查是否有 --venv 或 -e
TEMP_VENV=""
TEMP_ARGS=()
for arg in "$@"; do
  if [ "$PARSE_VENV" = "1" ]; then
    TEMP_VENV="$arg"
    PARSE_VENV="0"
  elif [ "$arg" = "--venv" ] || [ "$arg" = "-e" ]; then
    PARSE_VENV="1"
  else
    TEMP_ARGS+=("$arg")
  fi
done

# 确定最终的虚拟环境路径
VENV_PATH=""

if [ -n "$TEMP_VENV" ]; then
  VENV_PATH="$TEMP_VENV"
elif [ -n "$DS_CLI_VENV" ]; then
  VENV_PATH="$DS_CLI_VENV"
elif [ -n "$DEEPSEEK_VENV_PATH" ]; then
  VENV_PATH="$DEEPSEEK_VENV_PATH"
elif [ -n "$VIRTUAL_ENV" ]; then
  VENV_PATH="$VIRTUAL_ENV"
else
  VENV_PATH="$DEFAULT_VENV"
fi

# 尝试查找 Python 解释器的优先级顺序：
# 1. 虚拟环境中的 Python（如果虚拟环境存在）
# 2. 系统 Python

PYTHON_PATH=""

# 检查虚拟环境是否存在
if [ -d "$VENV_PATH" ]; then
  # 尝试不同的 Python 路径
  PYTHON_CANDIDATES=(
    "$VENV_PATH/bin/python3"
    "$VENV_PATH/bin/python"
    "$VENV_PATH/Scripts/python.exe"  # Windows 支持
  )
  
  for candidate in "${PYTHON_CANDIDATES[@]}"; do
    if [ -x "$candidate" ]; then
      PYTHON_PATH="$candidate"
      break
    fi
  done
  
  # 如果在虚拟环境中找到了 Python
  if [ -n "$PYTHON_PATH" ]; then
    if [ -n "$VERBOSE" ]; then
      echo "使用虚拟环境：$VENV_PATH" >&2
      echo "使用 Python 解释器：$PYTHON_PATH" >&2
    fi
    # 使用虚拟环境中的 Python 运行 DeepSeek CLI
    exec "$PYTHON_PATH" -m ds "${TEMP_ARGS[@]}"
  fi
fi

# 如果没有找到虚拟环境或虚拟环境中的 Python，使用系统 Python
PYTHON_CANDIDATES=(
  "python3"
  "python"
)

for candidate in "${PYTHON_CANDIDATES[@]}"; do
  if command -v "$candidate" >/dev/null 2>&1; then
    PYTHON_PATH="$candidate"
    break
  fi

done

if [ -n "$PYTHON_PATH" ]; then
  if [ -n "$VERBOSE" ]; then
    echo "使用系统 Python 解释器：$PYTHON_PATH" >&2
  fi
  # 使用系统 Python 运行 DeepSeek CLI
  exec "$PYTHON_PATH" -m ds "${TEMP_ARGS[@]}"
else
  echo "错误：未找到 Python 解释器！" >&2
  echo "请安装 Python 3.8 或更高版本，或检查虚拟环境配置。" >&2
  exit 1
fi
