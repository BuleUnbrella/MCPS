"""
CodeMaster MCP 的日志工具。
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional


class Logger:
    """CodeMaster MCP 的自定义日志记录器。"""
    
    def __init__(self, name: str = "CodeMaster", log_level: Optional[str] = None):
        """
        初始化日志记录器。
        
        参数:
            name: 日志记录器名称
            log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR)
        """
        self.logger = logging.getLogger(name)
        
        # 设置日志级别
        level = log_level or os.getenv("LOG_LEVEL", "INFO").upper()
        self.set_level(level)
        
        # 避免添加多个处理器
        if not self.logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.logger.level)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            
            # Add handler to logger
            self.logger.addHandler(console_handler)
            
            # Optionally add file handler
            log_file = os.getenv("LOG_FILE")
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(self.logger.level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
    
    def set_level(self, level: str):
        """Set the logging level."""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        
        log_level = level_map.get(level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # Update all handlers
        for handler in self.logger.handlers:
            handler.setLevel(log_level)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)
    
    def log_command(self, command: str, description: str = ""):
        """Log command execution."""
        if description:
            self.info(f"Executing: {command} - {description}")
        else:
            self.info(f"Executing: {command}")
    
    def log_result(self, success: bool, message: str = ""):
        """Log command result."""
        if success:
            self.info(f"Success: {message}" if message else "Command completed successfully")
        else:
            self.error(f"Failed: {message}" if message else "Command failed")


# Global logger instance
logger = Logger()


def get_logger(name: str = "CodeMaster") -> Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return Logger(name)