"""
工厂模块

提供创建浏览器驱动和控制器的工厂函数。
"""

from typing import Any

from .config import get_selenium_browser
from .controllers.browser_controller import BrowserController
from .drivers.selenium_driver import SeleniumDriver


async def create_browser_driver(
    browser: str = None, options: dict[str, Any] = None
) -> SeleniumDriver:
    """创建浏览器驱动

    Args:
        browser: 浏览器类型，可选值: chrome, chromium, firefox, edge。在ARM架构上推荐使用chromium代替chrome
        options: 驱动选项

    Returns:
        浏览器驱动实例
    """
    browser = browser or get_selenium_browser()
    options = options or {}

    driver = SeleniumDriver(browser, options)
    await driver.connect()

    return driver


async def create_browser_controller(
    browser: str = None, options: dict[str, Any] = None
) -> BrowserController:
    """创建浏览器控制器

    Args:
        browser: 浏览器类型，可选值: chrome, chromium, firefox, edge。在ARM架构上推荐使用chromium代替chrome
        options: 驱动选项

    Returns:
        浏览器控制器实例
    """
    driver = await create_browser_driver(browser, options)
    controller = BrowserController(driver)

    return controller
