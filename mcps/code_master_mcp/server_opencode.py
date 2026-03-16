#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CodeMaster MCP 服务器 - opencode 部署版。
专为 /home/walker/.config/opencode 环境优化。
"""

import os
import sys
from pathlib import Path
from typing import Optional

# 添加当前目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from fastmcp import FastMCP

# 直接导入函数，避免相对导入问题
try:
    # 尝试从当前目录导入
    from .tools.code_analysis import (
        read_code_lines,
        get_file_structure,
        find_references_refined,
        get_python_dependencies,
    )
    from .tools.git_tools import get_line_history
    from .tools.shell_tools import run_shellcheck
    from .utils.logger import Logger
    from .utils.path_utils_opencode import resolve_path, get_default_repo_path
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from tools.code_analysis import (
        read_code_lines,
        get_file_structure,
        find_references_refined,
        get_python_dependencies,
    )
    from tools.git_tools import get_line_history
    from tools.shell_tools import run_shellcheck
    from utils.logger import Logger
    from utils.path_utils_opencode import resolve_path, get_default_repo_path

logger = Logger("CodeMaster-MCP-opencode")
mcp = FastMCP("CodeMaster-Pro-opencode")

# opencode 环境特定的默认路径 - 直接定义
OPENCODE_BASE_PATH = "/home/walker/.config/opencode"
OPENCODE_PROJECTS_PATH = os.path.join(OPENCODE_BASE_PATH, "projects")
OPENCODE_MCPS_PATH = os.path.join(OPENCODE_BASE_PATH, "mcps")

# 确保目录存在
os.makedirs(OPENCODE_PROJECTS_PATH, exist_ok=True)

# 设置默认仓库路径
DEFAULT_REPO_PATH_OPENCODE = OPENCODE_PROJECTS_PATH


class CodeMasterMCPopencode:
    """CodeMaster MCP 服务器类 - opencode 部署版。"""

    def __init__(self, default_repo_path: Optional[str] = None):
        """
        初始化 CodeMaster MCP 服务器（opencode 版）。

        参数:
            default_repo_path: 相对路径的默认仓库路径。
                               如果为 None，使用 opencode 项目目录。
        """
        # 优先使用传入的路径，然后是环境变量，最后是 opencode 默认路径
        if default_repo_path:
            self.default_repo_path = default_repo_path
        else:
            env_path = os.getenv("DEFAULT_REPO_PATH")
            if env_path and os.path.exists(env_path):
                self.default_repo_path = env_path
            else:
                self.default_repo_path = DEFAULT_REPO_PATH_OPENCODE
        
        # 确保目录存在
        os.makedirs(self.default_repo_path, exist_ok=True)
        
        logger.info(f"CodeMaster MCP (opencode版) 初始化完成")
        logger.info(f"默认仓库路径: {self.default_repo_path}")
        logger.info(f"opencode 基础路径: {OPENCODE_BASE_PATH}")

    def run(self):
        """运行 MCP 服务器。"""
        # 设置环境变量供其他模块使用
        os.environ["DEFAULT_REPO_PATH"] = self.default_repo_path
        os.environ["OPENCODE_MODE"] = "true"
        
        logger.info("启动 CodeMaster MCP 服务器 (opencode版)...")
        mcp.run()


# 注册所有工具到 MCP 服务器
mcp.tool()(read_code_lines)
mcp.tool()(get_file_structure)
mcp.tool()(get_line_history)
mcp.tool()(find_references_refined)
mcp.tool()(run_shellcheck)
mcp.tool()(get_python_dependencies)


def main():
    """MCP 服务器的入口点 (opencode版)。"""
    import argparse

    parser = argparse.ArgumentParser(description="CodeMaster MCP 服务器 (opencode部署版)")
    parser.add_argument(
        "--repo-path",
        type=str,
        default=None,
        help=f"相对路径的默认仓库路径 (默认: {DEFAULT_REPO_PATH_OPENCODE})",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="日志级别",
    )
    parser.add_argument(
        "--opencode-path",
        type=str,
        default=OPENCODE_BASE_PATH,
        help=f"opencode 基础路径 (默认: {OPENCODE_BASE_PATH})",
    )

    args = parser.parse_args()

    # 设置日志级别
    logger.set_level(args.log_level)
    
    # 处理自定义 opencode 路径
    custom_opencode_path = args.opencode_path
    custom_repo_path = args.repo_path
    
    # 如果提供了自定义 opencode 路径，更新相关路径
    if custom_opencode_path and custom_opencode_path != OPENCODE_BASE_PATH:
        custom_projects_path = os.path.join(custom_opencode_path, "projects")
        logger.info(f"使用自定义 opencode 路径: {custom_opencode_path}")
        logger.info(f"自定义项目路径: {custom_projects_path}")
        
        # 如果没有提供 repo-path，使用自定义项目路径
        if not custom_repo_path:
            custom_repo_path = custom_projects_path

    # 创建并运行服务器
    server = CodeMasterMCPopencode(default_repo_path=custom_repo_path)
    server.run()


if __name__ == "__main__":
    main()