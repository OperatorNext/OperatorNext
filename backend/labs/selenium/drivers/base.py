"""
浏览器驱动抽象基类

定义所有浏览器驱动必须实现的方法。
"""

from abc import ABC, abstractmethod
from typing import Any


class BrowserDriver(ABC):
    """浏览器驱动抽象基类"""

    @abstractmethod
    async def connect(self) -> None:
        """连接到浏览器服务"""
        pass

    @abstractmethod
    async def close(self) -> None:
        """关闭浏览器连接"""
        pass

    @abstractmethod
    async def navigate(self, url: str) -> None:
        """导航到指定 URL"""
        pass

    @abstractmethod
    async def get_current_url(self) -> str:
        """获取当前 URL"""
        pass

    @abstractmethod
    async def get_title(self) -> str:
        """获取页面标题"""
        pass

    @abstractmethod
    async def find_element(self, selector: str, by: str = "css") -> Any:
        """查找元素

        Args:
            selector: 元素选择器
            by: 选择器类型，可选值: css, xpath, id, name, tag, class, text

        Returns:
            找到的元素
        """
        pass

    @abstractmethod
    async def find_elements(self, selector: str, by: str = "css") -> list[Any]:
        """查找多个元素

        Args:
            selector: 元素选择器
            by: 选择器类型，可选值: css, xpath, id, name, tag, class, text

        Returns:
            找到的元素列表
        """
        pass

    @abstractmethod
    async def click(self, element: Any) -> None:
        """点击元素"""
        pass

    @abstractmethod
    async def type(self, element: Any, text: str) -> None:
        """在元素中输入文本"""
        pass

    @abstractmethod
    async def clear(self, element: Any) -> None:
        """清除元素内容"""
        pass

    @abstractmethod
    async def get_text(self, element: Any) -> str:
        """获取元素文本"""
        pass

    @abstractmethod
    async def get_attribute(self, element: Any, name: str) -> str | None:
        """获取元素属性"""
        pass

    @abstractmethod
    async def is_displayed(self, element: Any) -> bool:
        """检查元素是否可见"""
        pass

    @abstractmethod
    async def is_enabled(self, element: Any) -> bool:
        """检查元素是否启用"""
        pass

    @abstractmethod
    async def is_selected(self, element: Any) -> bool:
        """检查元素是否被选中"""
        pass

    @abstractmethod
    async def execute_script(self, script: str, *args) -> Any:
        """执行 JavaScript 代码"""
        pass

    @abstractmethod
    async def take_screenshot(self) -> bytes:
        """获取屏幕截图"""
        pass

    @abstractmethod
    async def save_screenshot(self, path: str) -> bool:
        """保存屏幕截图"""
        pass

    @abstractmethod
    async def wait_for_element(
        self, selector: str, by: str = "css", timeout: int = 10
    ) -> Any:
        """等待元素出现"""
        pass

    @abstractmethod
    async def wait_for_navigation(self, timeout: int = 30) -> None:
        """等待页面导航完成"""
        pass

    @abstractmethod
    async def get_cookies(self) -> list[dict[str, Any]]:
        """获取所有 Cookie"""
        pass

    @abstractmethod
    async def add_cookie(self, cookie: dict[str, Any]) -> None:
        """添加 Cookie"""
        pass

    @abstractmethod
    async def delete_cookie(self, name: str) -> None:
        """删除指定 Cookie"""
        pass

    @abstractmethod
    async def delete_all_cookies(self) -> None:
        """删除所有 Cookie"""
        pass
