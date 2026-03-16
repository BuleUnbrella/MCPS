"""
Git 相关工具：用于代码历史分析。
"""

import os
import subprocess
from pathlib import Path

from mcps.code_master_mcp.utils.path_utils import resolve_path, get_default_repo_path


def get_line_history(file_path: str, line_num: int) -> str:
    """
    获取特定行的最后修改信息（Git Blame）。
    
    用于分析代码变更的原因和关联的提交信息。
    
    参数:
        file_path: 文件路径（相对或绝对）
        line_num: 要分析的行号（1开始）
        
    返回:
        包含 git blame 信息的字符串
    """
    try:
        # 获取工作目录
        if os.path.isabs(file_path):
            cwd = os.path.dirname(file_path)
            rel_path = os.path.basename(file_path)
        else:
            cwd = get_default_repo_path()
            rel_path = file_path
        
        # Check if it's a git repository
        git_check = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=cwd,
            capture_output=True,
            text=True
        )
        
        if git_check.returncode != 0:
            return "Git blame failed. Not a git repository."
        
        # Check if file is tracked
        git_ls = subprocess.run(
            ["git", "ls-files", "--error-unmatch", rel_path],
            cwd=cwd,
            capture_output=True,
            text=True
        )
        
        if git_ls.returncode != 0:
            return f"Git blame failed. File '{rel_path}' is not tracked by git."
        
        # Run git blame
        cmd = ["git", "blame", "-L", f"{line_num},{line_num}", "--", rel_path]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode != 0:
            return "Git blame failed. Unknown error."
            
        # Parse and format the output
        lines = result.stdout.strip().split('\n')
        if not lines or lines[0] == '':
            return "No git blame information available."
            
        # Extract commit hash and author
        line = lines[0]
        parts = line.split()
        if len(parts) >= 2:
            commit_hash = parts[0]
            # Try to get more commit info
            try:
                commit_info = subprocess.run(
                    ["git", "show", "--oneline", "-s", commit_hash],
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )
                if commit_info.returncode == 0:
                    return f"Line {line_num}: {commit_info.stdout.strip()}\n\nFull blame:\n{result.stdout}"
            except:
                pass
                
        return result.stdout.strip()
    except Exception as e:
        return f"Git error: {str(e)}"


def get_file_history(file_path: str, limit: int = 10) -> str:
    """
    Get commit history for a specific file.
    
    Args:
        file_path: Path to the file (relative or absolute)
        limit: Maximum number of commits to return
        
    Returns:
        String containing file commit history
    """
    try:
        if os.path.isabs(file_path):
            cwd = os.path.dirname(file_path)
            rel_path = os.path.basename(file_path)
        else:
            cwd = get_default_repo_path()
            rel_path = file_path
        
        cmd = [
            "git", "log",
            f"--max-count={limit}",
            "--pretty=format:%h - %an, %ar : %s",
            "--", rel_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode != 0:
            return "Git log failed. Not a git repository or file not tracked."
            
        if not result.stdout.strip():
            return f"No commit history found for '{rel_path}'."
            
        return f"Recent commits for {rel_path}:\n\n{result.stdout.strip()}"
    except Exception as e:
        return f"Git history error: {str(e)}"