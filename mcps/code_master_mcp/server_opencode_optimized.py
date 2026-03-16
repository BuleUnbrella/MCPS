#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CodeMaster MCP 服务器 - opencode 部署版（优化版）。
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

# opencode 环境特定的默认路径 - 直接定义（避免导入问题）
OPENCODE_BASE_PATH = "/home/walker/.config/opencode"
OPENCODE_PROJECTS_PATH = os.path.join(OPENCODE_BASE_PATH, "projects")
OPENCODE_MCPS_PATH = os.path.join(OPENCODE_BASE_PATH, "mcps")

# 确保目录存在
os.makedirs(OPENCODE_PROJECTS_PATH, exist_ok=True)

# 动态导入工具模块
def import_tools():
    """动态导入所有需要的工具模块。"""
    # 导入代码分析工具
    from tools.code_analysis import (
        read_code_lines,
        get_file_structure,
        find_references_refined,
        get_python_dependencies,
    )
    
    # 导入Git工具
    from tools.git_tools import get_line_history
    
    # 导入Shell工具
    from tools.shell_tools import run_shellcheck
    
    # 导入日志工具
    from utils.logger import Logger
    
    return {
        'read_code_lines': read_code_lines,
        'get_file_structure': get_file_structure,
        'find_references_refined': find_references_refined,
        'get_python_dependencies': get_python_dependencies,
        'get_line_history': get_line_history,
        'run_shellcheck': run_shellcheck,
        'Logger': Logger,
    }

# 导入工具
try:
    tools = import_tools()
    logger = tools['Logger']("CodeMaster-MCP-opencode")
    
    # 提取工具函数
    read_code_lines = tools['read_code_lines']
    get_file_structure = tools['get_file_structure']
    find_references_refined = tools['find_references_refined']
    get_python_dependencies = tools['get_python_dependencies']
    get_line_history = tools['get_line_history']
    run_shellcheck = tools['run_shellcheck']
    
except ImportError as e:
    print(f"错误: 无法导入工具模块 - {e}")
    print(f"当前目录: {current_dir}")
    print(f"Python路径: {sys.path}")
    sys.exit(1)

mcp = FastMCP("CodeMaster-Pro-opencode")


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
                self.default_repo_path = OPENCODE_PROJECTS_PATH
        
        # 确保目录存在
        os.makedirs(self.default_repo_path, exist_ok=True)
        
        logger.info(f"CodeMaster MCP (opencode版) 初始化完成")
        logger.info(f"默认仓库路径: {self.default_repo_path}")
        logger.info(f"opencode 基础路径: {OPENCODE_BASE_PATH}")
        logger.info(f"opencode 项目路径: {OPENCODE_PROJECTS_PATH}")
        logger.info(f"opencode MCPs 路径: {OPENCODE_MCPS_PATH}")

    def run(self):
        """运行 MCP 服务器。"""
        # 设置环境变量供其他模块使用
        os.environ["DEFAULT_REPO_PATH"] = self.default_repo_path
        os.environ["OPENCODE_MODE"] = "true"
        os.environ["OPENCODE_BASE_PATH"] = OPENCODE_BASE_PATH
        os.environ["OPENCODE_PROJECTS_PATH"] = OPENCODE_PROJECTS_PATH
        
        logger.info("启动 CodeMaster MCP 服务器 (opencode版)...")
        mcp.run()


# 创建 opencode 专用的工具包装函数
@mcp.tool()
def read_code_lines_opencode(file_path: str, start_line: int, end_line: int) -> str:
    """
    opencode 版的 read_code_lines - 读取文件的特定行范围。
    
    参数:
        file_path: 文件路径（相对或绝对）
        start_line: 起始行号（1开始）
        end_line: 结束行号（1开始）
        
    返回:
        包含指定行范围的字符串
    """
    return read_code_lines(file_path, start_line, end_line)


@mcp.tool()
def get_file_structure_opencode(file_path: str) -> str:
    """
    opencode 版的 get_file_structure - 深度解析文件以提取函数、类、结构体。
    
    参数:
        file_path: 文件路径（相对或绝对）
        
    返回:
        包含结构信息的 JSON 字符串
    """
    return get_file_structure(file_path)


@mcp.tool()
def get_line_history_opencode(file_path: str, line_num: int) -> str:
    """
    opencode 版的 get_line_history - 获取特定行的最后修改信息（Git Blame）。
    
    参数:
        file_path: 文件路径（相对或绝对）
        line_num: 要分析的行号（1开始）
        
    返回:
        包含 git blame 信息的字符串
    """
    return get_line_history(file_path, line_num)


@mcp.tool()
def find_references_refined_opencode(symbol: str, max_results: int = 25) -> str:
    """
    opencode 版的 find_references_refined - 在整个代码库中搜索符号引用。
    
    参数:
        symbol: 要搜索的符号
        max_results: 返回的最大结果数（默认: 25）
        
    返回:
        包含搜索结果的字符串
    """
    import subprocess
    
    try:
        # 检查 ripgrep 是否可用
        subprocess.run(["rg", "--version"], capture_output=True, check=True)
        
        # 使用 opencode 项目路径作为搜索根目录
        search_root = os.getenv("DEFAULT_REPO_PATH", OPENCODE_PROJECTS_PATH)
        
        cmd = [
            "rg", "--vimgrep", "--word-regexp",
            "--glob", "!{.git,node_modules,build,dist,__pycache__,out,obj,target}/*",
            symbol, search_root
        ]
        
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if not res.stdout:
            return f"未找到 '{symbol}' 的使用。"
        
        output_lines = []
        for line in res.stdout.splitlines()[:max_results]:
            parts = line.split(":", 3)
            if len(parts) >= 4:
                # 转换为相对路径
                rel_path = os.path.relpath(parts[0], search_root)
                output_lines.append(f"{rel_path}:{parts[1]}: {parts[3].strip()}")
                
        if len(res.stdout.splitlines()) > max_results:
            output_lines.append(f"... 还有 {len(res.stdout.splitlines()) - max_results} 个结果")
            
        return "\n".join(output_lines)
    except FileNotFoundError:
        return "错误: ripgrep (rg) 未找到。请安装 ripgrep 以进行快速搜索。"
    except Exception as e:
        return f"搜索错误: {str(e)}"


@mcp.tool()
def run_shellcheck_opencode(file_path: str) -> str:
    """
    opencode 版的 run_shellcheck - 对 Shell 脚本运行静态分析。
    
    参数:
        file_path: Shell 脚本路径（相对或绝对）
        
    返回:
        包含 shellcheck 结果的字符串
    """
    return run_shellcheck(file_path)


@mcp.tool()
def get_python_dependencies_opencode(file_path: str) -> str:
    """
    opencode 版的 get_python_dependencies - 从 Python 文件中提取所有导入语句。
    
    参数:
        file_path: Python 文件路径（相对或绝对）
        
    返回:
        包含导入信息的 JSON 字符串
    """
    return get_python_dependencies(file_path)


@mcp.tool()
def get_opencode_info() -> str:
    """
    获取 opencode 环境信息。
    
    返回:
        包含 opencode 环境信息的字符串
    """
    info = {
        "opencode_base_path": OPENCODE_BASE_PATH,
        "opencode_projects_path": OPENCODE_PROJECTS_PATH,
        "opencode_mcps_path": OPENCODE_MCPS_PATH,
        "default_repo_path": os.getenv("DEFAULT_REPO_PATH", OPENCODE_PROJECTS_PATH),
        "current_directory": os.getcwd(),
        "python_version": sys.version,
    }
    
    import json
    return json.dumps(info, indent=2, ensure_ascii=False)


def main():
    """MCP 服务器的入口点 (opencode版)。"""
    import argparse

    parser = argparse.ArgumentParser(description="CodeMaster MCP 服务器 (opencode部署版)")
    parser.add_argument(
        "--repo-path",
        type=str,
        default=None,
        help=f"相对路径的默认仓库路径 (默认: {OPENCODE_PROJECTS_PATH})",
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
        default=None,
        help=f"opencode 基础路径 (默认: {OPENCODE_BASE_PATH})",
    )

    args = parser.parse_args()

    # 设置日志级别
    logger.set_level(args.log_level)
    
    # 处理自定义 opencode 路径
    custom_repo_path = args.repo_path
    
    # 如果提供了自定义 opencode 路径，更新相关路径
    if args.opencode_path:
        custom_base_path = args.opencode_path
        custom_projects_path = os.path.join(custom_base_path, "projects")
        
        logger.info(f"使用自定义 opencode 路径: {custom_base_path}")
        logger.info(f"自定义项目路径: {custom_projects_path}")
        
        # 设置环境变量
        os.environ["OPENCODE_BASE_PATH_CUSTOM"] = custom_base_path
        os.environ["OPENCODE_PROJECTS_PATH_CUSTOM"] = custom_projects_path
        
        # 如果没有提供 repo-path，使用自定义项目路径
        if not custom_repo_path:
            custom_repo_path = custom_projects_path

    # 创建并运行服务器
    server = CodeMasterMCPopencode(default_repo_path=custom_repo_path)
    server.run()


if __name__ == "__main__":
    main()