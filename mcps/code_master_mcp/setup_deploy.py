#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CodeMaster MCP 部署配置 - 专为 opencode 环境设计。
"""

from setuptools import setup, find_packages
import os

# 读取 README.md 作为长描述
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "CodeMaster MCP - 专业代码分析工具"

setup(
    name="code-master-mcp-deploy",
    version="1.0.0",
    author="CodeMaster Team",
    author_email="contact@example.com",
    description="Professional MCP tools for code analysis and understanding (opencode部署版)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code-master-mcp",
    packages=find_packages(include=["code_master_mcp", "code_master_mcp.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastmcp>=1.0.0",
        "tree-sitter-languages>=1.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "code-master-mcp-deploy=code_master_mcp.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "code_master_mcp": ["py.typed"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/code-master-mcp/issues",
        "Source": "https://github.com/yourusername/code-master-mcp",
        "Documentation": "https://github.com/yourusername/code-master-mcp/wiki",
    },
)