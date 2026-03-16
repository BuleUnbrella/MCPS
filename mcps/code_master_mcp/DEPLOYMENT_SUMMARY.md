# CodeMaster MCP opencode 部署总结

## 🎯 部署完成

CodeMaster MCP 已成功部署到 opencode 环境：

**部署路径**: `/home/walker/.config/opencode/mcps/code_master_mcp`

## 📁 部署结构

```
/home/walker/.config/opencode/
├── mcps/
│   └── code_master_mcp/              # 本部署
│       ├── server_opencode_optimized.py # 主服务器文件（优化版）
│       ├── run.sh                   # 运行脚本
│       ├── test_deploy.sh           # 部署测试脚本
│       ├── deploy.sh                # 部署脚本（用于更新）
│       ├── requirements_opencode.txt # 依赖文件
│       ├── setup_deploy.py          # 部署配置
│       ├── DEPLOYMENT_SUMMARY.md    # 本文件
│       ├── opencode_integration.md  # 集成指南
│       ├── tools/                   # 工具模块
│       │   ├── __init__.py
│       │   ├── code_analysis.py
│       │   ├── git_tools.py
│       │   └── shell_tools.py
│       ├── utils/                   # 工具模块
│       │   ├── __init__.py
│       │   ├── logger.py
│       │   ├── path_utils.py
│       │   └── path_utils_opencode.py
│       └── __init__.py              # 包初始化
└── projects/                        # opencode 项目目录（默认工作区）
```

## 🚀 快速开始

### 1. 启动服务器
```bash
cd /home/walker/.config/opencode/mcps/code_master_mcp
./run.sh
```

### 2. 带参数启动
```bash
./run.sh --log-level DEBUG --repo-path /your/custom/path
```

### 3. 获取帮助
```bash
./run.sh --help
```

## 🔧 可用工具

CodeMaster MCP 提供以下专业代码分析工具：

1. **`read_code_lines`** - 精准读取文件的特定行范围
2. **`get_file_structure`** - 深度分析代码结构（函数、类、结构体）
3. **`get_line_history`** - Git 历史溯源（git blame）
4. **`find_references_refined`** - 全代码库符号引用搜索
5. **`run_shellcheck`** - Shell 脚本静态分析
6. **`get_python_dependencies`** - Python 依赖导入分析

## ⚙️ 配置选项

### 环境变量
```bash
# 设置默认仓库路径
export DEFAULT_REPO_PATH="/home/walker/.config/opencode/projects"

# 启用 opencode 模式
export OPENCODE_MODE="true"
```

### 命令行参数
```bash
--repo-path PATH      # 设置默认仓库路径
--log-level LEVEL     # 设置日志级别 (DEBUG, INFO, WARNING, ERROR)
--help                # 显示帮助信息
```

## 📦 依赖管理

### Python 依赖
```bash
# 安装所有依赖
pip install -r /home/walker/.config/opencode/mcps/code_master_mcp/requirements_opencode.txt

# 或单独安装
pip install fastmcp tree-sitter-languages
```

### 系统工具（推荐）
```bash
# Ubuntu/Debian
sudo apt-get install git ripgrep shellcheck

# macOS
brew install git ripgrep shellcheck
```

## 🧪 测试部署

运行测试脚本验证部署：
```bash
cd /home/walker/.config/opencode/mcps/code_master_mcp
./test_deploy.sh
```

## 🔄 更新部署

如果需要更新部署，使用部署脚本：
```bash
# 从原始项目目录更新
cd /path/to/original/code-master-mcp
./deploy.sh

# 或指定源目录
./deploy.sh /path/to/source
```

## 🛠️ 故障排除

### 常见问题

1. **导入错误**
   ```bash
   # 重新安装依赖
   pip install --upgrade fastmcp tree-sitter-languages
   ```

2. **权限问题**
   ```bash
   chmod +x /home/walker/.config/opencode/mcps/code_master_mcp/*.sh
   ```

3. **tree-sitter 问题**
   ```bash
   # 如果 get_file_structure 失败
   pip install --upgrade tree-sitter-languages
   ```

4. **系统工具缺失**
   ```bash
   # 安装 ripgrep 用于快速搜索
   sudo apt-get install ripgrep
   ```

### 日志查看
```bash
# 启用调试日志
./run.sh --log-level DEBUG
```

## 🌐 集成到 opencode

### 在 opencode 启动脚本中添加
```bash
# ~/.bashrc 或 ~/.zshrc
export CODEMASTER_MCP_PATH="/home/walker/.config/opencode/mcps/code_master_mcp"
export DEFAULT_REPO_PATH="/home/walker/.config/opencode/projects"

# 启动函数
start_codemaster_mcp() {
    if [ -f "$CODEMASTER_MCP_PATH/run.sh" ]; then
        "$CODEMASTER_MCP_PATH/run.sh" &
        echo "CodeMaster MCP 已启动"
    fi
}
```

### 创建别名
```bash
alias codemaster="/home/walker/.config/opencode/mcps/code_master_mcp/run.sh"
```

## 📊 部署验证

✅ **所有测试通过**
- Python 导入成功
- 关键文件存在
- 目录结构完整
- 运行脚本可执行
- opencode 环境就绪
- 核心依赖已安装

## 📞 支持

### 文档
- 项目文档: `/home/walker/.config/opencode/mcps/code_master_mcp/opencode_integration.md`
- 原始文档: 原始项目目录中的 README.md

### 问题排查
1. 运行测试脚本: `./test_deploy.sh`
2. 查看日志: `./run.sh --log-level DEBUG`
3. 检查依赖: `pip list | grep -E "fastmcp|tree-sitter"`

## 🎉 部署完成

CodeMaster MCP 现已完全集成到您的 opencode 环境中，提供专业的代码分析能力。所有工具都已中文化，适合中文开发者使用。

**下一步建议**:
1. 启动服务器测试功能
2. 将 opencode 项目放入 `/home/walker/.config/opencode/projects/`
3. 通过 MCP 协议连接到 Claude Desktop 或其他 AI 助手
4. 开始使用代码分析工具提高开发效率

---
**部署时间**: $(date)
**部署版本**: 1.0.0 (opencode部署版)
**部署路径**: /home/walker/.config/opencode/mcps/code_master_mcp