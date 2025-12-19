#!/bin/bash
# 安装脚本：简化 DeepSeek CLI 的安装过程

echo "正在安装DeepSeek CLI (ds)..."
echo ""

# 检查是否在正确的目录
if [ ! -f "setup.py" ]; then
    echo "错误：请在项目根目录下运行此脚本！"
    echo "请先进入deepseek-cli目录，然后执行 ./install.sh"
    exit 1
fi

# 自动检测当前是否在虚拟环境中
CURRENT_VENV=""
if [ -n "$VIRTUAL_ENV" ]; then
    CURRENT_VENV="$VIRTUAL_ENV"
    echo "检测到当前已激活虚拟环境：$CURRENT_VENV"
    echo ""
fi

# 询问是否使用当前虚拟环境或创建新的
if [ -n "$CURRENT_VENV" ]; then
    echo "是否使用当前激活的虚拟环境？(y/n)"
    read -r use_current_venv
    
    if [[ ! $use_current_venv =~ ^[Yy]$ ]]; then
        CURRENT_VENV=""
    fi
fi

# 如果没有使用当前虚拟环境，询问是否创建新的
if [ -z "$CURRENT_VENV" ]; then
    DEFAULT_VENV="$HOME/.deepseek-cli-venv"
    echo "是否要创建新的虚拟环境？(y/n)"
    read -r create_new_venv
    
    if [[ $create_new_venv =~ ^[Yy]$ ]]; then
        echo "请输入虚拟环境路径（默认：$DEFAULT_VENV）："
        read -r new_venv_path
        NEW_VENV="${new_venv_path:-$DEFAULT_VENV}"
        
        echo ""
        echo "正在创建虚拟环境：$NEW_VENV"
        python3 -m venv "$NEW_VENV"
        
        if [ $? -eq 0 ]; then
            CURRENT_VENV="$NEW_VENV"
            echo "✅ 虚拟环境创建成功！"
            echo ""
            
            # 激活虚拟环境
            echo "正在激活虚拟环境..."
            source "$CURRENT_VENV/bin/activate"
            echo "✅ 虚拟环境已激活！"
            echo ""
        else
            echo "❌ 虚拟环境创建失败，请手动创建后重新运行脚本。"
            exit 1
        fi
    else
        echo "将使用系统Python环境进行安装。"
        echo ""
    fi
fi

# 升级pip
echo "正在升级pip..."
pip install --upgrade pip
if [ $? -eq 0 ]; then
    echo "✅ pip升级成功！"
    echo ""
fi

# 执行安装命令
echo "执行安装命令：pip install -e ."
echo "(注：-e 表示可编辑模式，. 表示当前目录)"
echo ""
pip install -e .

# 检查安装结果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ DeepSeek CLI安装成功！"
    echo ""
    
    # 保存虚拟环境路径到配置文件（如果有）
    if [ -n "$CURRENT_VENV" ]; then
        # 确保配置文件目录存在
        CONFIG_DIR="$HOME/.config/deepseek-cli"
        mkdir -p "$CONFIG_DIR"
        
        # 保存虚拟环境路径
        echo "DEEPSEEK_VENV_PATH=$CURRENT_VENV" > "$CONFIG_DIR/config.env"
        echo "已保存虚拟环境配置到：$CONFIG_DIR/config.env"
        echo ""
    fi
    
    # 询问是否安装全局命令
    echo "是否要安装全局命令？(y/n)"
    read -r install_global
    
    if [[ $install_global =~ ^[Yy]$ ]]; then
        # 确保全局包装脚本存在且可执行
        if [ -f "ds_global.sh" ]; then
            chmod +x ds_global.sh
            
            # 如果有虚拟环境，更新ds_global.sh中的默认虚拟环境
            if [ -n "$CURRENT_VENV" ]; then
                echo "正在更新全局脚本的默认虚拟环境..."
                tmpfile="$(mktemp)"
                sed "s|DEFAULT_VENV=.*|DEFAULT_VENV=\"$CURRENT_VENV\"|g" ds_global.sh > "$tmpfile" && mv "$tmpfile" ds_global.sh
            fi
            
            # 复制到 /usr/local/bin
            echo "正在安装全局命令..."
            sudo cp ds_global.sh /usr/local/bin/ds
            
            if [ $? -eq 0 ]; then
                echo "✅ 全局命令安装成功！"
                echo "现在你可以在任何位置使用 'ds' 命令了。"
                echo ""
                echo "配置说明："
                echo "1. 设置API密钥：export DEEPSEEK_API_KEY=your-api-key-here"
                echo "   建议添加到 ~/.bashrc 或 ~/.zshrc 文件中持久化"
                echo ""
                if [ -n "$CURRENT_VENV" ]; then
                    echo "2. 虚拟环境已配置：$CURRENT_VENV"
                    echo "   (可选) 要更改虚拟环境：export DS_CLI_VENV=/path/to/your/venv"
                else
                    echo "2. (可选) 指定虚拟环境：export DS_CLI_VENV=/path/to/your/venv"
                    echo "   如果不指定，默认使用系统Python环境"
                fi
                echo ""
                echo "3. (可选) 指定CLI根目录：export DS_CLI_ROOT=/path/to/deepseek-cli"
            else
                echo "❌ 全局命令安装失败，请检查权限。"
                echo "你可以手动安装：sudo cp ds_global.sh /usr/local/bin/ds"
            fi
        else
            echo "❌ 全局包装脚本不存在，请确保 ds_global.sh 文件在当前目录。"
        fi
    else
        echo "跳过全局命令安装。"
        echo ""
        if [ -n "$CURRENT_VENV" ]; then
            echo "使用方法："
            echo "1. 激活虚拟环境：source $CURRENT_VENV/bin/activate"
            echo "2. 运行ds命令：ds Hello, world!"
        else
            echo "使用方法："
            echo "1. 在项目目录中运行：./ds Hello, world!"
            echo "2. 或使用Python模块方式：python -m ds Hello, world!"
        fi
        echo ""
        echo "配置API密钥：export DEEPSEEK_API_KEY=your-api-key-here"
    fi
    
    echo ""
    echo "使用示例："
    echo "  ds Hello, world!"
    echo "  ds --help  # 查看帮助信息"
    echo "  ds -t 'Hello world'  # 翻译"
    echo ""
    echo "更多功能请查看帮助文档。"
else
    echo ""
    echo "❌ 安装失败，请检查错误信息并尝试解决问题。"
    echo "常见解决方案："
    echo "1. 确保已安装pip和Python 3.8+"
    echo "2. 升级pip：pip install --upgrade pip"
    echo "3. 检查网络连接"
    echo "4. 尝试使用虚拟环境安装"
    exit 1
fi
