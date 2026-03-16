"""
CodeMaster MCP 的命令行接口。
"""

import argparse
import sys
from .server import main as server_main


def main():
    """主 CLI 入口点。"""
    parser = argparse.ArgumentParser(
        description="CodeMaster MCP - 专业代码分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行 MCP 服务器
  code-master-mcp
  
  # 使用自定义仓库路径运行
  code-master-mcp --repo-path /path/to/your/code
  
  # 使用调试日志运行
  code-master-mcp --log-level DEBUG
  
  # 显示版本
  code-master-mcp --version
        """
    )
    
    parser.add_argument(
        "--repo-path",
        type=str,
        default=None,
        help="Default repository path for relative paths"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information"
    )
    
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List available MCP tools"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run self-test"
    )
    
    args = parser.parse_args()
    
    # Handle version flag
    if args.version:
        from . import __version__
        print(f"CodeMaster MCP v{__version__}")
        sys.exit(0)
    
    # Handle list-tools flag
    if args.list_tools:
        print("Available CodeMaster MCP Tools:")
        print("=" * 40)
        print("1. read_code_lines - Read specific line ranges from files")
        print("2. get_file_structure - Extract functions, classes, and structs")
        print("3. get_line_history - Get git blame information")
        print("4. find_references_refined - Search for symbol references")
        print("5. run_shellcheck - Static analysis for shell scripts")
        print("6. get_python_dependencies - Extract import statements")
        print("\nSystem Requirements:")
        print("- git (for git history tools)")
        print("- ripgrep (rg) (for fast searching)")
        print("- shellcheck (for shell script analysis)")
        sys.exit(0)
    
    # Handle test flag
    if args.test:
        print("Running self-test...")
        # Import test modules
        try:
            from .tools.code_analysis import read_code_lines, get_file_structure
            from .utils.path_utils import get_default_repo_path
            
            print(f"✓ Default repo path: {get_default_repo_path()}")
            print("✓ Core modules imported successfully")
            print("\nBasic tests passed!")
        except Exception as e:
            print(f"✗ Test failed: {e}")
            sys.exit(1)
        sys.exit(0)
    
    # Run the MCP server
    try:
        # Set environment variables from CLI args
        if args.repo_path:
            import os
            os.environ["DEFAULT_REPO_PATH"] = args.repo_path
        
        # Run server with parsed args
        sys.argv = [sys.argv[0]]  # Reset argv for server_main
        if args.repo_path:
            sys.argv.extend(["--repo-path", args.repo_path])
        sys.argv.extend(["--log-level", args.log_level])
        
        server_main()
    except KeyboardInterrupt:
        print("\nCodeMaster MCP server stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()