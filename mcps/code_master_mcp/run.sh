#!/bin/bash

# CodeMaster MCP 运行脚本 - opencode 环境

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 使用优化版的服务器
PYTHON_SCRIPT="$SCRIPT_DIR/server_opencode_optimized.py"

echo "启动 CodeMaster MCP (opencode版)..."
echo "脚本目录: $SCRIPT_DIR"
echo "Python 脚本: $PYTHON_SCRIPT"

# 检查文件是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "错误: 找不到服务器脚本 $PYTHON_SCRIPT"
    echo "请确保部署完整"
    exit 1
fi

# 检查依赖
echo "检查 Python 依赖..."

# 检查 fastmcp
if ! python3 -c "import fastmcp" 2>/dev/null; then
    echo "fastmcp 未安装，尝试安装..."
    pip install fastmcp || {
        echo "错误: 无法安装 fastmcp"
        echo "请手动运行: pip install fastmcp"
        exit 1
    }
fi

# 检查 tree-sitter-languages
if ! python3 -c "import tree_sitter_languages" 2>/dev/null; then
    echo "tree-sitter-languages 未安装，尝试安装..."
    pip install tree-sitter-languages || {
        echo "警告: 无法安装 tree-sitter-languages"
        echo "get_file_structure 功能将受限"
        echo "请手动运行: pip install tree-sitter-languages"
    }
fi

# 设置环境变量
export DEFAULT_REPO_PATH="${DEFAULT_REPO_PATH:-/home/walker/.config/opencode/projects}"
export OPENCODE_MODE="true"

echo "环境配置:"
echo "  - 默认仓库路径: $DEFAULT_REPO_PATH"
echo "  - opencode 模式: $OPENCODE_MODE"
echo "  - Python 路径: $(which python3)"

# 运行服务器
echo "启动 MCP 服务器..."
cd "$SCRIPT_DIR"
exec python3 "$PYTHON_SCRIPT" "$@"