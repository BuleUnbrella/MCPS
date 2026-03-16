"""
CodeMaster MCP 的路径工具函数。
"""

import os
from pathlib import Path
from typing import Optional


def get_default_repo_path() -> str:
    """
    获取默认仓库路径。
    
    返回:
        来自环境变量或当前目录的默认仓库路径
    """
    default_path = os.getenv("DEFAULT_REPO_PATH")
    if default_path and os.path.exists(default_path):
        return default_path
    return os.getcwd()


def resolve_path(file_path: str, base_path: Optional[str] = None) -> Path:
    """
    将文件路径（相对或绝对）解析为绝对 Path 对象。
    
    参数:
        file_path: 要解析的路径（相对或绝对）
        base_path: 相对路径的基础路径。如果为 None，使用默认仓库路径。
        
    返回:
        解析后的绝对 Path 对象
        
    抛出:
        ValueError: 如果路径无法解析
    """
    path = Path(file_path)
    
    if path.is_absolute():
        return path
    
    # Use provided base path or default
    if base_path:
        base = Path(base_path)
    else:
        base = Path(get_default_repo_path())
    
    # Resolve relative path
    resolved = (base / path).resolve()
    
    # Check if path exists
    if not resolved.exists():
        # Try to find the file in parent directories
        current = base
        while current != current.parent:  # Stop at root
            potential = (current / path).resolve()
            if potential.exists():
                return potential
            current = current.parent
    
    return resolved


def ensure_directory(path: str) -> Path:
    """
    Ensure a directory exists.
    
    Args:
        path: Directory path
        
    Returns:
        Path object for the directory
    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def get_relative_path(absolute_path: str, base_path: Optional[str] = None) -> str:
    """
    Get relative path from absolute path.
    
    Args:
        absolute_path: Absolute path
        base_path: Base path for relativity. If None, uses default repo path.
        
    Returns:
        Relative path string
    """
    if base_path:
        base = Path(base_path)
    else:
        base = Path(get_default_repo_path())
    
    abs_path = Path(absolute_path).resolve()
    try:
        return str(abs_path.relative_to(base.resolve()))
    except ValueError:
        # Path is not relative to base, return absolute path
        return str(abs_path)


def is_within_directory(file_path: str, directory: str) -> bool:
    """
    Check if a file is within a directory.
    
    Args:
        file_path: File path to check
        directory: Directory to check against
        
    Returns:
        True if file is within directory, False otherwise
    """
    try:
        file_path_obj = Path(file_path).resolve()
        directory_obj = Path(directory).resolve()
        return directory_obj in file_path_obj.parents or file_path_obj == directory_obj
    except:
        return False


def find_files(pattern: str, search_path: Optional[str] = None) -> list[str]:
    """
    Find files matching a pattern.
    
    Args:
        pattern: Glob pattern to match
        search_path: Path to search in. If None, uses default repo path.
        
    Returns:
        List of matching file paths
    """
    if search_path:
        base = Path(search_path)
    else:
        base = Path(get_default_repo_path())
    
    return [str(p) for p in base.rglob(pattern) if p.is_file()]


def normalize_path(path: str) -> str:
    """
    Normalize a path string.
    
    Args:
        path: Path to normalize
        
    Returns:
        Normalized path string
    """
    return str(Path(path).resolve())


def get_file_info(file_path: str) -> dict:
    """
    Get information about a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with file information
    """
    path = resolve_path(file_path)
    
    if not path.exists():
        return {"error": "File does not exist"}
    
    stats = path.stat()
    
    return {
        "path": str(path),
        "name": path.name,
        "stem": path.stem,
        "suffix": path.suffix,
        "parent": str(path.parent),
        "size": stats.st_size,
        "modified": stats.st_mtime,
        "created": stats.st_ctime,
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
        "is_symlink": path.is_symlink(),
    }