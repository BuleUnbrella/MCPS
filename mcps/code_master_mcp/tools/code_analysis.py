"""
代码分析工具：用于读取、解析和理解代码结构。
"""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import List, Optional

from tree_sitter_languages import get_language, get_parser

from mcps.code_master_mcp.utils.logger import Logger
from mcps.code_master_mcp.utils.path_utils import resolve_path, get_default_repo_path

logger = Logger()

# 文件扩展名到语言的映射
LANG_MAP = {
    ".py": "python",
    ".c": "c",
    ".h": "cpp",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".js": "javascript",
    ".ts": "typescript",
    ".go": "go",
    ".java": "java",
    ".rs": "rust",
    ".rb": "ruby",
}


def read_code_lines(file_path: str, start_line: int, end_line: int) -> str:
    """
    读取文件的特定行范围。
    
    当代理知道符号位置时，应使用此工具读取上下文，
    避免加载整个大文件。
    
    参数:
        file_path: 文件路径（相对或绝对）
        start_line: 起始行号（1开始）
        end_line: 结束行号（1开始）
        
    返回:
        包含指定行范围的字符串
    """
    try:
        path = resolve_path(file_path)
        
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            
        # 索引从0开始，行号从1开始
        content = lines[max(0, start_line - 1) : end_line]
        return "".join(content) if content else "选择的范围超出文件边界。"
    except FileNotFoundError:
        return f"错误：文件未找到: {file_path}"
    except Exception as e:
        return f"读取文件错误: {str(e)}"


def get_file_structure(file_path: str) -> str:
    """
    深度解析文件以提取函数、类、结构体及其行范围。
    
    用于快速理解文件的逻辑布局。
    
    参数:
        file_path: 文件路径（相对或绝对）
        
    返回:
        包含结构信息的 JSON 字符串
    """
    path = resolve_path(file_path)
    
    lang_name = LANG_MAP.get(path.suffix.lower())
    if not lang_name:
        return f"不支持的语言: {path.suffix}。支持的语言: {', '.join(LANG_MAP.keys())}"
    
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
        
        parser = get_parser(lang_name)
        tree = parser.parse(bytes(code, "utf8"))
        
        # 定义复杂查询：包含结构体和函数
        query_scm = """
            (function_definition name: (identifier) @name) @func
            (class_definition name: (identifier) @name) @class
            (struct_specifier name: (type_identifier) @name) @struct
            (method_definition name: (property_identifier) @name) @method
        """
        
        try:
            query = get_language(lang_name).query(query_scm)
            captures = query.captures(tree.root_node)
            
            results = []
            for node, tag in captures:
                if "name" in tag:
                    results.append({
                        "type": tag.split('.')[0],
                        "name": node.text.decode("utf8"),
                        "start": node.start_point[0] + 1,
                        "end": node.end_point[0] + 1
                    })
            return json.dumps(results, indent=2)
        except Exception as e:
            return f"Query error for language {lang_name}: {str(e)}"
    except Exception as e:
        return f"Parsing error: {str(e)}"


def find_references_refined(symbol: str, max_results: int = 25) -> str:
    """
    在整个代码库中搜索符号引用，自动过滤干扰项。
    
    参数:
        symbol: 要搜索的符号
        max_results: 返回的最大结果数（默认: 25）
        
    返回:
        包含搜索结果的字符串
    """
    logger.info(f"Searching references for: {symbol}")
    
    try:
        # Check if ripgrep is available
        subprocess.run(["rg", "--version"], capture_output=True, check=True)
        
        cmd = [
            "rg", "--vimgrep", "--word-regexp",
            "--glob", "!{.git,node_modules,build,dist,__pycache__,out,obj,target}/*",
            symbol, get_default_repo_path()
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
                # 转换为相对路径以减少 token 消耗
                rel_path = os.path.relpath(parts[0], get_default_repo_path())
                output_lines.append(f"{rel_path}:{parts[1]}: {parts[3].strip()}")
                
        if len(res.stdout.splitlines()) > max_results:
            output_lines.append(f"... 还有 {len(res.stdout.splitlines()) - max_results} 个结果")
            
        return "\n".join(output_lines)
    except FileNotFoundError:
        return "错误: ripgrep (rg) 未找到。请安装 ripgrep 以进行快速搜索。"
    except Exception as e:
        return f"搜索错误: {str(e)}"


def get_python_dependencies(file_path: str) -> str:
    """
    从 Python 文件中提取所有导入语句及其目标。
    
    帮助分析跨文件调用关系。
    
    参数:
        file_path: Python 文件路径（相对或绝对）
        
    返回:
        包含导入信息的 JSON 字符串
    """
    try:
        path = resolve_path(file_path)
        
        if path.suffix.lower() != ".py":
            return "Error: This tool only works with Python files (.py)"
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Improved regex to handle more import patterns
        import_patterns = [
            # Standard imports: import module
            r'^import\s+([\w\.]+(?:\s*,\s*[\w\.]+)*)',
            # From imports: from module import something
            r'^from\s+([\w\.]+)\s+import\s+([\w\*]+(?:\s*,\s*[\w\*]+)*)',
        ]
        
        imports = []
        for pattern in import_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            imports.extend(matches)
            
        # Format results
        formatted_imports = []
        for imp in imports:
            if isinstance(imp, tuple):
                if len(imp) == 2:
                    formatted_imports.append({
                        "type": "from_import",
                        "module": imp[0],
                        "imports": [i.strip() for i in imp[1].split(",")]
                    })
            else:
                formatted_imports.append({
                    "type": "direct_import",
                    "modules": [m.strip() for m in imp.split(",")]
                })
                
        return json.dumps(formatted_imports, indent=2)
    except Exception as e:
        return f"Dependency extraction failed: {str(e)}"