#!/bin/bash

# CodeMaster MCP 部署测试脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "测试 CodeMaster MCP 部署..."
echo "目录: $SCRIPT_DIR"
echo "opencode 路径: /home/walker/.config/opencode"
echo ""

# 测试 Python 导入
echo "1. 测试 Python 导入..."
if python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
try:
    from server_simple import CodeMasterMCPopencode
    print('✓ 服务器类导入成功')
except ImportError as e:
    print(f'✗ 导入失败: {e}')
    sys.exit(1)
"; then
    echo "✓ Python 导入测试通过"
else
    echo "✗ Python 导入测试失败"
    exit 1
fi

# 测试文件存在性
echo ""
echo "2. 测试关键文件..."
REQUIRED_FILES=("server_simple.py" "run.sh" "requirements_opencode.txt")
ALL_PASS=true

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        echo "  ✓ $file 存在"
    else
        echo "  ✗ $file 不存在"
        ALL_PASS=false
    fi
done

# 测试目录结构
echo ""
echo "3. 测试目录结构..."
REQUIRED_DIRS=("tools" "utils")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$SCRIPT_DIR/$dir" ]; then
        echo "  ✓ $dir/ 目录存在"
        # 检查目录内容
        file_count=$(find "$SCRIPT_DIR/$dir" -name "*.py" | wc -l)
        echo "     包含 $file_count 个 Python 文件"
    else
        echo "  ✗ $dir/ 目录不存在"
        ALL_PASS=false
    fi
done

# 测试运行脚本
echo ""
echo "4. 测试运行脚本..."
if [ -f "$SCRIPT_DIR/run.sh" ]; then
    if [ -x "$SCRIPT_DIR/run.sh" ]; then
        echo "  ✓ run.sh 可执行"
    else
        echo "  ✗ run.sh 不可执行"
        ALL_PASS=false
    fi
else
    echo "  ✗ run.sh 不存在"
    ALL_PASS=false
fi

# 测试 opencode 目录结构
echo ""
echo "5. 测试 opencode 目录结构..."
OPENCODE_BASE="/home/walker/.config/opencode"
if [ -d "$OPENCODE_BASE" ]; then
    echo "  ✓ opencode 基础目录存在: $OPENCODE_BASE"
    
    # 检查 projects 目录
    if [ -d "$OPENCODE_BASE/projects" ]; then
        echo "  ✓ opencode 项目目录存在"
    else
        echo "  ⚠ opencode 项目目录不存在，将自动创建"
        mkdir -p "$OPENCODE_BASE/projects"
    fi
    
    # 检查 mcps 目录
    if [ -d "$OPENCODE_BASE/mcps" ]; then
        echo "  ✓ opencode MCPs 目录存在"
    else
        echo "  ⚠ opencode MCPs 目录不存在"
    fi
else
    echo "  ⚠ opencode 基础目录不存在: $OPENCODE_BASE"
    echo "    请确保 opencode 环境正确配置"
fi

# 测试依赖
echo ""
echo "6. 测试 Python 依赖..."
DEPENDENCIES=("fastmcp" "tree_sitter_languages")
for dep in "${DEPENDENCIES[@]}"; do
    if python3 -c "import $dep" 2>/dev/null; then
        echo "  ✓ $dep 已安装"
    else
        echo "  ⚠ $dep 未安装"
        echo "    运行: pip install $dep"
        ALL_PASS=false
    fi
done

# 测试系统工具
echo ""
echo "7. 测试系统工具（可选）..."
SYSTEM_TOOLS=("git" "rg" "shellcheck")
for tool in "${SYSTEM_TOOLS[@]}"; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "  ✓ $tool 已安装"
    else
        echo "  ⚠ $tool 未安装（某些功能可能受限）"
    fi
done

echo ""
echo "=========================================="
if [ "$ALL_PASS" = true ]; then
    echo "所有测试通过！"
    echo ""
    echo "部署状态: ✅ 成功"
    echo ""
    echo "使用方法:"
    echo "  启动服务器: $SCRIPT_DIR/run.sh"
    echo "  带参数启动: $SCRIPT_DIR/run.sh --log-level DEBUG --repo-path /your/path"
    echo "  获取帮助: $SCRIPT_DIR/run.sh --help"
else
    echo "部分测试失败，请检查上述问题。"
    echo ""
    echo "部署状态: ⚠ 需要修复"
    echo ""
    echo "常见问题解决:"
    echo "  1. 安装依赖: pip install -r $SCRIPT_DIR/requirements_opencode.txt"
    echo "  2. 设置权限: chmod +x $SCRIPT_DIR/*.sh"
    echo "  3. 检查目录: ls -la $SCRIPT_DIR/"
fi
echo "=========================================="
echo ""
echo "opencode 集成信息:"
echo "  - MCP 路径: $SCRIPT_DIR"
echo "  - 项目路径: /home/walker/.config/opencode/projects"
echo "  - 默认仓库: $DEFAULT_REPO_PATH"
echo ""
echo "MCP 工具列表:"
echo "  1. read_code_lines - 读取文件的特定行范围"
echo "  2. get_file_structure - 分析代码结构"
echo "  3. get_line_history - Git 历史查询"
echo "  4. find_references_refined - 符号引用搜索"
echo "  5. run_shellcheck - Shell 脚本分析"
echo "  6. get_python_dependencies - Python 依赖分析"