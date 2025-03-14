"""
Selenium 驱动实现

使用 Selenium WebDriver 实现浏览器驱动接口。
"""

import asyncio
import base64
from telnetlib import EC
from typing import Any

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

from ..config import get_remote_url, get_selenium_browser
from .base import BrowserDriver


class SeleniumDriver(BrowserDriver):
    """Selenium WebDriver 实现"""

    def __init__(self, browser: str = None, options: dict[str, Any] = None):
        """初始化 Selenium 驱动

        Args:
            browser: 浏览器类型，可选值: chrome, firefox, edge
            options: 驱动选项
        """
        self.browser_type = browser or get_selenium_browser()
        self.options = options or {}
        self.driver = None
        self.wait = None
        self.default_timeout = self.options.get("timeout", 10)

    async def connect(self) -> None:
        """连接到 Selenium Grid"""
        # 在事件循环中运行以防阻塞
        self.driver = await asyncio.get_event_loop().run_in_executor(
            None, self._create_remote_driver
        )

        # 设置 WebDriverWait
        self.wait = WebDriverWait(self.driver, self.default_timeout)

        # 设置窗口大小
        if "window_size" in self.options:
            width, height = self.options["window_size"]
            self.driver.set_window_size(width, height)

        # 设置隐式等待
        if "implicit_wait" in self.options:
            self.driver.implicitly_wait(self.options["implicit_wait"])

    def _create_remote_driver(self):
        """创建远程 WebDriver 连接"""
        remote_url = get_remote_url()
        browser_options = self._get_browser_options()

        capabilities = {
            "browserName": self.browser_type,
            "platformName": "ANY",
        }

        # 合并其他选项
        if "capabilities" in self.options:
            capabilities.update(self.options["capabilities"])

        # 创建远程 WebDriver
        return webdriver.Remote(command_executor=remote_url, options=browser_options)

    def _get_browser_options(self):
        """根据浏览器类型获取选项"""
        headless = self.options.get("headless", True)

        if self.browser_type == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            return options

        elif self.browser_type == "chromium":
            # Chromium 使用与Chrome相同的选项类
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            return options

        elif self.browser_type == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            return options

        elif self.browser_type == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            return options

        else:
            # 默认使用 Chrome/Chromium
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            return options

    async def close(self) -> None:
        """关闭浏览器连接"""
        if self.driver:
            await asyncio.get_event_loop().run_in_executor(None, self.driver.quit)
            self.driver = None
            self.wait = None

    async def navigate(self, url: str) -> None:
        """导航到指定 URL"""
        await asyncio.get_event_loop().run_in_executor(None, self.driver.get, url)

    async def get_current_url(self) -> str:
        """获取当前 URL"""
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.driver.current_url
        )

    async def get_title(self) -> str:
        """获取页面标题"""
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.driver.title
        )

    async def find_element(self, selector: str, by: str = "css") -> Any:
        """查找元素"""
        by_method = self._get_by_method(by)
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.driver.find_element(by_method, selector)
        )

    async def find_elements(self, selector: str, by: str = "css") -> list[Any]:
        """查找多个元素"""
        by_method = self._get_by_method(by)
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.driver.find_elements(by_method, selector)
        )

    async def click(self, element: Any) -> None:
        """点击元素"""
        await asyncio.get_event_loop().run_in_executor(None, element.click)

    async def type(self, element: Any, text: str) -> None:
        """在元素中输入文本"""
        await asyncio.get_event_loop().run_in_executor(None, element.send_keys, text)

    async def clear(self, element: Any) -> None:
        """清除元素内容"""
        await asyncio.get_event_loop().run_in_executor(None, element.clear)

    async def get_text(self, element: Any) -> str:
        """获取元素文本"""
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: element.text
        )

    async def get_attribute(self, element: Any, name: str) -> str | None:
        """获取元素属性"""
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: element.get_attribute(name)
        )

    async def is_displayed(self, element: Any) -> bool:
        """检查元素是否可见"""
        return await asyncio.get_event_loop().run_in_executor(
            None, element.is_displayed
        )

    async def is_enabled(self, element: Any) -> bool:
        """检查元素是否启用"""
        return await asyncio.get_event_loop().run_in_executor(None, element.is_enabled)

    async def is_selected(self, element: Any) -> bool:
        """检查元素是否被选中"""
        return await asyncio.get_event_loop().run_in_executor(None, element.is_selected)

    async def execute_script(self, script: str, *args) -> Any:
        """执行 JavaScript 代码"""
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.driver.execute_script(script, *args)
        )

    async def take_screenshot(self) -> bytes:
        """获取屏幕截图"""
        screenshot_base64 = await asyncio.get_event_loop().run_in_executor(
            None, self.driver.get_screenshot_as_base64
        )
        return base64.b64decode(screenshot_base64)

    async def save_screenshot(self, path: str) -> bool:
        """保存屏幕截图"""
        return await asyncio.get_event_loop().run_in_executor(
            None, self.driver.save_screenshot, path
        )

    async def wait_for_element(
        self, selector: str, by: str = "css", timeout: int = 10
    ) -> Any:
        """等待元素出现"""
        by_method = self._get_by_method(by)
        try:
            element = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by_method, selector))
                ),
            )
            return element
        except TimeoutException:
            return None

    async def wait_for_navigation(self, timeout: int = 30) -> None:
        """等待页面导航完成"""
        # 检查页面已加载完成（document.readyState === 'complete'）
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: WebDriverWait(self.driver, timeout).until(
                    lambda d: d.execute_script("return document.readyState")
                    == "complete"
                ),
            )
        except TimeoutException as e:
            print(f"等待页面导航完成超时: {e}")
            pass  # 超时也继续执行

    async def get_cookies(self) -> list[dict[str, Any]]:
        """获取所有 Cookie"""
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.driver.get_cookies()
        )

    async def add_cookie(self, cookie: dict[str, Any]) -> None:
        """添加 Cookie"""
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.driver.add_cookie(cookie)
        )

    async def delete_cookie(self, name: str) -> None:
        """删除指定 Cookie"""
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.driver.delete_cookie(name)
        )

    async def delete_all_cookies(self) -> None:
        """删除所有 Cookie"""
        await asyncio.get_event_loop().run_in_executor(
            None, self.driver.delete_all_cookies
        )

    def _get_by_method(self, by: str) -> str:
        """获取选择器方法"""
        by_map = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "tag": By.TAG_NAME,
            "class": By.CLASS_NAME,
            "text": By.LINK_TEXT,
            "partial_text": By.PARTIAL_LINK_TEXT,
        }
        return by_map.get(by.lower(), By.CSS_SELECTOR)
