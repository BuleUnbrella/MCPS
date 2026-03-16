"""
CodeMaster MCP 服务器主实现。
"""

import os
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

from .tools.code_analysis import (
    read_code_lines,
    get_file_structure,
    find_references_refined,
    get_python_dependencies,
)
from .tools.git_tools import get_line_history
from .tools.shell_tools import run_shellcheck
from .utils.logger import Logger
from .utils.path_utils import resolve_path

logger = Logger()
mcp = FastMCP("CodeMaster-Pro")


class CodeMasterMCP:
    """CodeMaster 工具的主 MCP 服务器类。"""

    def __init__(self, default_repo_path: Optional[str] = None):
        """
        初始化 CodeMaster MCP 服务器。

        参数:
            default_repo_path: 相对路径的默认仓库路径。
                               如果为 None，使用环境变量 DEFAULT_REPO_PATH
                               或当前工作目录。
        """
        self.default_repo_path = default_repo_path or os.getenv(
            "DEFAULT_REPO_PATH", os.getcwd()
        )
        logger.info(f"CodeMaster MCP initialized with repo path: {self.default_repo_path}")

    def run(self):
        """运行 MCP 服务器。"""
        mcp.run()


# Register all tools with the MCP server
mcp.tool()(read_code_lines)
mcp.tool()(get_file_structure)
mcp.tool()(get_line_history)
mcp.tool()(find_references_refined)
mcp.tool()(run_shellcheck)
mcp.tool()(get_python_dependencies)


def main():
    """MCP 服务器的入口点。"""
    import argparse

    parser = argparse.ArgumentParser(description="CodeMaster MCP 服务器")
    parser.add_argument(
        "--repo-path",
        type=str,
        default=None,
        help="相对路径的默认仓库路径",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="日志级别",
    )

    args = parser.parse_args()

    # Set log level
    logger.set_level(args.log_level)

    # Create and run server
    server = CodeMasterMCP(default_repo_path=args.repo_path)
    server.run()


if __name__ == "__main__":
    main()