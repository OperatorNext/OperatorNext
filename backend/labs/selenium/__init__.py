"""
Selenium 模块

提供基于 Selenium Grid 的浏览器自动化能力，使用桥接模式设计。
"""

from .factory import create_browser_controller

__all__ = ["create_browser_controller"]
