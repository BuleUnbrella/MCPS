#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CodeMaster MCP 路径工具函数 - opencode 部署版。
专为 /home/walker/.config/opencode 环境优化。
"""

import os
from pathlib import Path
from typing import Optional

# opencode 环境特定的路径
OPENCODE_BASE_PATH = "/home/walker/.config/opencode"
OPENCODE_PROJECTS_PATH = os.path.join(OPENCODE_BASE_PATH, "projects")
OPENCODE_MCPS_PATH = os.path.join(OPENCODE_BASE_PATH, "mcps")


def get_default_repo_path() -> str:
    """
    获取默认仓库路径 (opencode版)。
    
    返回:
        来自环境变量、opencode 项目目录或当前目录的默认仓库路径
    """
    # 1. 检查环境变量
    default_path = os.getenv("DEFAULT_REPO_PATH")
    if default_path and os.path.exists(default_path):
        return default_path
    
    # 2. 检查 opencode 项目目录
    if os.path.exists(OPENCODE_PROJECTS_PATH):
        return OPENCODE_PROJECTS_PATH
    
    # 3. 回退到当前目录
    return os.getcwd()


def get_opencode_base_path() -> str:
    """
    获取 opencode 基础路径。
    
    返回:
        opencode 基础路径
    """
    return OPENCODE_BASE_PATH


def get_opencode_projects_path() -> str:
    """
    获取 opencode 项目目录路径。
    
    返回:
        opencode 项目目录路径
    """
    return OPENCODE_PROJECTS_PATH


def get_opencode_mcps_path() -> str:
    """
    获取 opencode MCPs 目录路径。
    
    返回:
        opencode MCPs 目录路径
    """
    return OPENCODE_MCPS_PATH


def resolve_path(file_path: str, base_path: Optional[str] = None) -> Path:
    """
    将文件路径（相对或绝对）解析为绝对 Path 对象 (opencode版)。
    
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
    
    # 使用提供的基础路径或默认值
    if base_path:
        base = Path(base_path)
    else:
        base = Path(get_default_repo_path())
    
    # 解析相对路径
    resolved = (base / path).resolve()
    
    # 检查路径是否存在
    if not resolved.exists():
        # 尝试在 opencode 项目目录中查找
        if OPENCODE_PROJECTS_PATH and os.path.exists(OPENCODE_PROJECTS_PATH):
            potential = Path(OPENCODE_PROJECTS_PATH) / path
            if potential.exists():
                return potential.resolve()
        
        # 尝试在当前目录的父目录中查找
        current = base
        while current != current.parent:  # 在根目录停止
            potential = (current / path).resolve()
            if potential.exists():
                return potential
            current = current.parent
    
    return resolved


def ensure_opencode_directories() -> dict:
    """
    确保所有 opencode 目录存在。
    
    返回:
        包含目录路径的字典
    """
    directories = {
        "base": OPENCODE_BASE_PATH,
        "projects": OPENCODE_PROJECTS_PATH,
        "mcps": OPENCODE_MCPS_PATH,
    }
    
    for name, path in directories.items():
        os.makedirs(path, exist_ok=True)
    
    return directories


def is_within_opencode(file_path: str) -> bool:
    """
    检查文件是否在 opencode 目录结构内。
    
    参数:
        file_path: 要检查的文件路径
        
    返回:
        如果文件在 opencode 目录内返回 True，否则返回 False
    """
    try:
        file_path_obj = Path(file_path).resolve()
        opencode_base = Path(OPENCODE_BASE_PATH).resolve()
        
        # 检查文件是否在 opencode 基础目录或其子目录中
        return opencode_base in file_path_obj.parents or file_path_obj == opencode_base
    except:
        return False


def get_relative_to_opencode(absolute_path: str) -> str:
    """
    获取相对于 opencode 基础路径的相对路径。
    
    参数:
        absolute_path: 绝对路径
        
    返回:
        相对于 opencode 基础路径的相对路径
    """
    abs_path = Path(absolute_path).resolve()
    opencode_base = Path(OPENCODE_BASE_PATH).resolve()
    
    try:
        return str(abs_path.relative_to(opencode_base))
    except ValueError:
        # 路径不相对与 opencode 基础路径，返回绝对路径
        return str(abs_path)


def find_opencode_projects() -> list:
    """
    查找 opencode 项目目录中的所有项目。
    
    返回:
        项目路径列表
    """
    projects = []
    
    if os.path.exists(OPENCODE_PROJECTS_PATH):
        for item in os.listdir(OPENCODE_PROJECTS_PATH):
            item_path = os.path.join(OPENCODE_PROJECTS_PATH, item)
            if os.path.isdir(item_path):
                # 检查是否是项目目录（包含 .git 或其他项目文件）
                if (os.path.exists(os.path.join(item_path, ".git")) or
                    os.path.exists(os.path.join(item_path, "package.json")) or
                    os.path.exists(os.path.join(item_path, "requirements.txt")) or
                    os.path.exists(os.path.join(item_path, "pyproject.toml"))):
                    projects.append(item_path)
    
    return projects


def get_file_info_opencode(file_path: str) -> dict:
    """
    获取文件信息 (opencode版)。
    
    参数:
        file_path: 文件路径
        
    返回:
        包含文件信息的字典
    """
    path = resolve_path(file_path)
    
    if not path.exists():
        return {"error": "文件不存在"}
    
    stats = path.stat()
    
    info = {
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
        "within_opencode": is_within_opencode(str(path)),
    }
    
    # 如果是 opencode 内的文件，添加相对路径
    if info["within_opencode"]:
        info["relative_to_opencode"] = get_relative_to_opencode(str(path))
    
    return info