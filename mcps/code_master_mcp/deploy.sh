#!/bin/bash

# CodeMaster MCP 部署脚本 - opencode 环境
# 将 CodeMaster MCP 部署到 /home/walker/.config/opencode/mcps/code_master_mcp

set -e  # 遇到错误时退出

echo "=========================================="
echo "CodeMaster MCP opencode 部署脚本"
echo "=========================================="

# 检查目标目录
TARGET_DIR="/home/walker/.config/opencode/mcps/code_master_mcp"
echo "目标目录: $TARGET_DIR"

if [ ! -d "$TARGET_DIR" ]; then
    echo "创建目标目录..."
    mkdir -p "$TARGET_DIR"
fi

# 检查是否在项目目录中
if [ ! -f "setup.py" ] && [ ! -f "server_simple.py" ]; then
    echo "错误: 请在 CodeMaster MCP 项目目录中运行此脚本"
    echo "或者指定源目录: $0 <源目录>"
    exit 1
fi

# 确定源目录
if [ $# -eq 1 ]; then
    SOURCE_DIR="$1"
else
    SOURCE_DIR="."
fi

echo "源目录: $(realpath "$SOURCE_DIR")"

# 复制文件
echo "复制文件到目标目录..."

# 复制核心文件
cp -r "$SOURCE_DIR"/code_master_mcp/* "$TARGET_DIR/" 2>/dev/null || true

# 复制简化版服务器
if [ -f "$SOURCE_DIR/server_simple.py" ]; then
    cp "$SOURCE_DIR/server_simple.py" "$TARGET_DIR/"
fi

# 复制配置文件
if [ -f "$SOURCE_DIR/requirements_opencode.txt" ]; then
    cp "$SOURCE_DIR/requirements_opencode.txt" "$TARGET_DIR/"
fi

if [ -f "$SOURCE_DIR/setup_deploy.py" ]; then
    cp "$SOURCE_DIR/setup_deploy.py" "$TARGET_DIR/"
fi

# 复制文档
if [ -f "$SOURCE_DIR/README.md" ]; then
    cp "$SOURCE_DIR/README.md" "$TARGET_DIR/"
fi

# 设置权限
echo "设置文件权限..."
chmod +x "$TARGET_DIR/deploy.sh" 2>/dev/null || true
chmod +x "$TARGET_DIR/run.sh" 2>/dev/null || true

# 创建运行脚本
echo "创建运行脚本..."
cat > "$TARGET_DIR/run.sh" << 'EOF'
#!/bin/bash

# CodeMaster MCP 运行脚本 - opencode 环境

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/server_simple.py"

echo "启动 CodeMaster MCP (opencode版)..."
echo "脚本目录: $SCRIPT_DIR"

# 检查依赖
echo "检查 Python 依赖..."
python3 -c "import fastmcp" 2>/dev/null || {
    echo "fastmcp 未安装，尝试安装..."
    pip install fastmcp
}

python3 -c "import tree_sitter_languages" 2>/dev/null || {
    echo "tree-sitter-languages 未安装，尝试安装..."
    pip install tree-sitter-languages
}

# 运行服务器
echo "启动 MCP 服务器..."
cd "$SCRIPT_DIR"
exec python3 "$PYTHON_SCRIPT" "$@"
EOF

chmod +x "$TARGET_DIR/run.sh"

# 创建测试脚本
echo "创建测试脚本..."
cat > "$TARGET_DIR/test_deploy.sh" << 'EOF'
#!/bin/bash

# CodeMaster MCP 部署测试脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "测试 CodeMaster MCP 部署..."
echo "目录: $SCRIPT_DIR"

# 测试 Python 导入
echo "1. 测试 Python 导入..."
if python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); from server_simple import CodeMasterMCPopencode; print('✓ 服务器类导入成功')"; then
    echo "✓ Python 导入测试通过"
else
    echo "✗ Python 导入测试失败"
    exit 1
fi

# 测试文件存在性
echo "2. 测试关键文件..."
REQUIRED_FILES=("server_simple.py" "run.sh")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        echo "✓ $file 存在"
    else
        echo "✗ $file 不存在"
        exit 1
    fi
done

# 测试目录结构
echo "3. 测试目录结构..."
REQUIRED_DIRS=("tools" "utils")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$SCRIPT_DIR/$dir" ]; then
        echo "✓ $dir/ 目录存在"
    else
        echo "✗ $dir/ 目录不存在"
        exit 1
    fi
done

# 测试运行脚本
echo "4. 测试运行脚本..."
if [ -x "$SCRIPT_DIR/run.sh" ]; then
    echo "✓ run.sh 可执行"
else
    echo "✗ run.sh 不可执行"
    exit 1
fi

echo "=========================================="
echo "所有测试通过！"
echo "=========================================="
echo ""
echo "使用方法:"
echo "1. 启动服务器: $SCRIPT_DIR/run.sh"
echo "2. 带参数启动: $SCRIPT_DIR/run.sh --log-level DEBUG --repo-path /your/path"
echo "3. 测试部署: $SCRIPT_DIR/test_deploy.sh"
echo ""
echo "opencode 路径: /home/walker/.config/opencode"
echo "MCP 路径: $SCRIPT_DIR"
EOF

chmod +x "$TARGET_DIR/test_deploy.sh"

# 创建 opencode 集成配置
echo "创建 opencode 集成配置..."
cat > "$TARGET_DIR/opencode_integration.md" << 'EOF'
# CodeMaster MCP opencode 集成指南

## 目录结构
```
/home/walker/.config/opencode/
├── mcps/
│   └── code_master_mcp/          # 本部署
│       ├── server_simple.py      # 主服务器文件
│       ├── run.sh               # 运行脚本
│       ├── tools/               # 工具模块
│       ├── utils/               # 工具模块
│       ├── requirements_opencode.txt # 依赖
│       └── ...                  # 其他文件
└── projects/                    # opencode 项目目录（默认工作区）
```

## 快速开始

### 1. 安装依赖
```bash
cd /home/walker/.config/opencode/mcps/code_master_mcp
pip install -r requirements_opencode.txt
```

### 2. 运行服务器
```bash
./run.sh
```

### 3. 测试部署
```bash
./test_deploy.sh
```

## 配置 opencode

### 环境变量
在 opencode 配置中添加：
```bash
export DEFAULT_REPO_PATH="/home/walker/.config/opencode/projects"
export CODEMASTER_MCP_PATH="/home/walker/.config/opencode/mcps/code_master_mcp"
```

### 启动脚本
在 opencode 启动脚本中添加：
```bash
# 启动 CodeMaster MCP
if [ -f "$CODEMASTER_MCP_PATH/run.sh" ]; then
    "$CODEMASTER_MCP_PATH/run.sh" &
    echo "CodeMaster MCP 已启动"
fi
```

## MCP 工具列表

1. `read_code_lines` - 读取文件的特定行范围
2. `get_file_structure` - 分析代码结构
3. `get_line_history` - Git 历史查询
4. `find_references_refined` - 符号引用搜索
5. `run_shellcheck` - Shell 脚本分析
6. `get_python_dependencies` - Python 依赖分析

## 故障排除

### 1. 导入错误
```bash
# 安装缺失的依赖
pip install fastmcp tree-sitter-languages
```

### 2. 系统工具缺失
```bash
# Ubuntu/Debian
sudo apt-get install git ripgrep shellcheck

# macOS
brew install git ripgrep shellcheck
```

### 3. 权限问题
```bash
chmod +x /home/walker/.config/opencode/mcps/code_master_mcp/*.sh
```

## 支持
如有问题，请查看项目文档或提交 issue。
EOF

echo "=========================================="
echo "部署完成！"
echo "=========================================="
echo ""
echo "下一步:"
echo "1. 测试部署: cd $TARGET_DIR && ./test_deploy.sh"
echo "2. 安装依赖: pip install -r $TARGET_DIR/requirements_opencode.txt"
echo "3. 启动服务器: $TARGET_DIR/run.sh"
echo "4. 查看集成指南: cat $TARGET_DIR/opencode_integration.md"
echo ""
echo "部署目录: $TARGET_DIR"
echo "opencode 基础路径: /home/walker/.config/opencode"
echo "默认项目路径: /home/walker/.config/opencode/projects"