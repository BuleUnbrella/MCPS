"""
Shell 脚本分析工具。
"""

import subprocess
from pathlib import Path

from mcps.code_master_mcp.utils.path_utils import resolve_path


def run_shellcheck(file_path: str) -> str:
    """
    对 Shell 脚本运行静态分析。
    
    返回脚本中潜在的语法错误、安全风险和优化建议。
    
    参数:
        file_path: Shell 脚本路径（相对或绝对）
        
    返回:
        包含 shellcheck 结果的字符串
    """
    try:
        path = resolve_path(file_path)
        
        # Check if it's a shell script
        if path.suffix.lower() not in ['.sh', '.bash', '.zsh']:
            # Check shebang
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                if not first_line.startswith('#!'):
                    return "Error: Not a shell script. Expected .sh/.bash/.zsh extension or shebang."
            except:
                return "Error: Could not read file to check shebang."
        
        # Check if shellcheck is installed
        try:
            subprocess.run(["shellcheck", "--version"], capture_output=True, check=True)
        except FileNotFoundError:
            return "Error: shellcheck not found. Please install shellcheck for shell script analysis."
        
        # Run shellcheck
        result = subprocess.run(
            ["shellcheck", "-f", "json", str(path)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            if result.stdout.strip():
                try:
                    # Parse and format JSON output
                    import json
                    issues = json.loads(result.stdout)
                    if issues:
                        formatted = []
                        for issue in issues:
                            formatted.append(
                                f"Line {issue.get('line', '?')}, Column {issue.get('column', '?')}: "
                                f"{issue.get('level', 'error').upper()} - {issue.get('code', '?')}\n"
                                f"  {issue.get('message', 'No message')}\n"
                            )
                        return "Shellcheck issues found:\n\n" + "\n".join(formatted)
                except:
                    return result.stdout
            return "No issues found by shellcheck."
        else:
            if result.stderr:
                return f"Shellcheck error: {result.stderr}"
            return "Shellcheck found issues. Use -f json for detailed output."
    except Exception as e:
        return f"Shellcheck execution failed: {str(e)}"


def analyze_shell_script(file_path: str) -> str:
    """
    Comprehensive shell script analysis.
    
    Args:
        file_path: Path to the shell script
        
    Returns:
        String containing analysis results
    """
    path = resolve_path(file_path)
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = []
        
        # Basic statistics
        lines = content.split('\n')
        analysis.append(f"File: {path.name}")
        analysis.append(f"Total lines: {len(lines)}")
        analysis.append(f"Non-empty lines: {len([l for l in lines if l.strip()])}")
        
        # Check for common issues
        issues = []
        
        # Check for shebang
        if lines and lines[0].startswith('#!'):
            analysis.append(f"Shebang: {lines[0]}")
        else:
            issues.append("No shebang found (not executable as standalone script)")
        
        # Check for common bashisms in sh scripts
        if path.suffix.lower() == '.sh':
            bashisms = ['[[', ']]', '=~', '${VAR//}', '${VAR/#}', '${VAR/%}']
            for i, line in enumerate(lines, 1):
                for bashism in bashisms:
                    if bashism in line:
                        issues.append(f"Line {i}: Possible bashism '{bashism}' in .sh script")
        
        # Check for unquoted variables
        import re
        for i, line in enumerate(lines, 1):
            # Simple pattern for unquoted $variables (not perfect but helpful)
            matches = re.findall(r'\$[A-Za-z_][A-Za-z0-9_]*', line)
            for match in matches:
                # Check if variable is quoted
                if f'"${match[1:]}"' not in line and f"'${match[1:]}'" not in line:
                    issues.append(f"Line {i}: Unquoted variable {match}")
        
        # Run shellcheck if available
        shellcheck_result = run_shellcheck(file_path)
        if "Shellcheck issues found" in shellcheck_result:
            issues.append("Shellcheck found issues (see detailed output)")
        
        # Compile analysis
        analysis.append("\nAnalysis:")
        if issues:
            analysis.append("Potential issues found:")
            for issue in issues[:10]:  # Limit to 10 issues
                analysis.append(f"  • {issue}")
            if len(issues) > 10:
                analysis.append(f"  ... and {len(issues) - 10} more issues")
        else:
            analysis.append("No obvious issues found.")
        
        analysis.append("\nShellcheck results:")
        analysis.append(shellcheck_result)
        
        return "\n".join(analysis)
    except Exception as e:
        return f"Script analysis failed: {str(e)}"