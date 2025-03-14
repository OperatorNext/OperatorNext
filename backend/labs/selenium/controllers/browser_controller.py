"""
浏览器控制器

提供高级的浏览器操作接口，使用底层驱动实现。
"""

from typing import Any

from ..drivers.base import BrowserDriver


class BrowserController:
    """浏览器控制器类

    提供更高级的浏览器操作抽象，使用底层驱动实现具体功能。
    """

    def __init__(self, driver: BrowserDriver):
        """初始化控制器

        Args:
            driver: 浏览器驱动实例
        """
        self.driver = driver

    async def connect(self) -> None:
        """连接到浏览器"""
        await self.driver.connect()

    async def close(self) -> None:
        """关闭浏览器"""
        await self.driver.close()

    async def navigate(self, url: str) -> None:
        """导航到指定 URL"""
        await self.driver.navigate(url)

    async def get_current_url(self) -> str:
        """获取当前 URL"""
        return await self.driver.get_current_url()

    async def get_title(self) -> str:
        """获取页面标题"""
        return await self.driver.get_title()

    # 便捷的元素查找方法
    async def find_element_by_css(self, selector: str) -> Any:
        """使用 CSS 选择器查找元素"""
        return await self.driver.find_element(selector, "css")

    async def find_element_by_xpath(self, xpath: str) -> Any:
        """使用 XPath 查找元素"""
        return await self.driver.find_element(xpath, "xpath")

    async def find_element_by_id(self, id: str) -> Any:
        """通过 ID 查找元素"""
        return await self.driver.find_element(id, "id")

    async def find_element_by_name(self, name: str) -> Any:
        """通过 name 属性查找元素"""
        return await self.driver.find_element(name, "name")

    async def find_element_by_class(self, class_name: str) -> Any:
        """通过 class 查找元素"""
        return await self.driver.find_element(class_name, "class")

    async def find_element_by_tag(self, tag_name: str) -> Any:
        """通过标签名查找元素"""
        return await self.driver.find_element(tag_name, "tag")

    async def find_element_by_text(self, text: str) -> Any:
        """通过链接文本查找元素"""
        return await self.driver.find_element(text, "text")

    async def find_elements_by_css(self, selector: str) -> list[Any]:
        """使用 CSS 选择器查找多个元素"""
        return await self.driver.find_elements(selector, "css")

    # 元素操作方法
    async def click(self, element: Any) -> None:
        """点击元素"""
        await self.driver.click(element)

    async def type_text(self, element: Any, text: str) -> None:
        """在元素中输入文本"""
        await self.driver.clear(element)
        await self.driver.type(element, text)

    async def get_text(self, element: Any) -> str:
        """获取元素文本"""
        return await self.driver.get_text(element)

    async def get_attribute(self, element: Any, name: str) -> str | None:
        """获取元素属性值"""
        return await self.driver.get_attribute(element, name)

    # 高级操作方法
    async def fill_form(self, form_data: dict[str, str]) -> None:
        """填充表单

        Args:
            form_data: 表单数据，格式为 {选择器: 值}
        """
        for selector, value in form_data.items():
            element = await self.find_element_by_css(selector)
            await self.type_text(element, value)

    async def click_button(self, text: str, tag_name: str = "button") -> None:
        """点击指定文本的按钮

        Args:
            text: 按钮文本
            tag_name: 按钮标签名，默认为 button
        """
        # 尝试通过文本内容查找按钮
        xpath = f"//{tag_name}[contains(text(), '{text}')]"
        try:
            button = await self.find_element_by_xpath(xpath)
            await self.click(button)
        except Exception:
            # 尝试通过值属性查找
            xpath = f"//{tag_name}[@value='{text}']"
            button = await self.find_element_by_xpath(xpath)
            await self.click(button)

    async def submit_form(
        self, form_data: dict[str, str], submit_selector: str
    ) -> None:
        """填充并提交表单

        Args:
            form_data: 表单数据，格式为 {选择器: 值}
            submit_selector: 提交按钮的选择器
        """
        await self.fill_form(form_data)
        submit_button = await self.find_element_by_css(submit_selector)
        await self.click(submit_button)

    async def wait_and_click(
        self, selector: str, by: str = "css", timeout: int = 10
    ) -> None:
        """等待元素出现并点击

        Args:
            selector: 元素选择器
            by: 选择器类型
            timeout: 超时时间（秒）
        """
        element = await self.driver.wait_for_element(selector, by, timeout)
        if element:
            await self.click(element)

    async def take_screenshot(self, path: str) -> bool:
        """获取屏幕截图并保存

        Args:
            path: 截图保存路径

        Returns:
            是否成功保存
        """
        return await self.driver.save_screenshot(path)

    async def save_screenshot(self, path: str) -> bool:
        """保存屏幕截图

        Args:
            path: 截图保存路径

        Returns:
            是否成功保存
        """
        return await self.driver.save_screenshot(path)

    async def execute_js(self, script: str, *args) -> Any:
        """执行 JavaScript 代码

        Args:
            script: JavaScript 代码
            args: 参数

        Returns:
            执行结果
        """
        return await self.driver.execute_script(script, *args)

    async def scroll_to(self, x: int, y: int) -> None:
        """滚动到指定位置

        Args:
            x: 横坐标
            y: 纵坐标
        """
        await self.execute_js(f"window.scrollTo({x}, {y});")

    async def scroll_into_view(self, element: Any) -> None:
        """滚动使元素可见

        Args:
            element: 元素
        """
        await self.execute_js(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element,
        )

    async def wait_for_navigation(self, timeout: int = 30) -> None:
        """等待页面导航完成

        Args:
            timeout: 超时时间（秒）
        """
        await self.driver.wait_for_navigation(timeout)

    async def switch_to_frame(self, frame_reference: int | str | Any) -> None:
        """切换到 iframe

        Args:
            frame_reference: iframe 引用，可以是索引、名称或元素
        """
        if isinstance(frame_reference, int):
            await self.execute_js(
                "window.top.frames[arguments[0]].focus()", frame_reference
            )
        elif isinstance(frame_reference, str):
            element = await self.find_element_by_css(frame_reference)
            await self.execute_js("arguments[0].contentWindow.focus()", element)
        else:
            await self.execute_js("arguments[0].contentWindow.focus()", frame_reference)

    async def switch_to_default_content(self) -> None:
        """切换到默认内容"""
        await self.execute_js("window.top.focus()")

    async def open_new_tab(self, url: str = None) -> None:
        """打开新标签页

        Args:
            url: 可选的 URL
        """
        if url:
            await self.execute_js(f"window.open('{url}', '_blank');")
        else:
            await self.execute_js("window.open('about:blank', '_blank');")

    async def switch_to_tab(self, index: int) -> None:
        """切换到指定索引的标签页

        Args:
            index: 标签页索引
        """
        handles = await self.execute_js(
            "return window.top.getBrowser().tabContainer.childNodes;"
        )
        if index < len(handles):
            await self.execute_js(
                "window.top.getBrowser().tabContainer.selectedIndex = arguments[0];",
                index,
            )

    async def get_page_source(self) -> str:
        """获取页面源代码

        Returns:
            页面源代码
        """
        return await self.execute_js("return document.documentElement.outerHTML;")

    async def get_cookies(self) -> list[dict[str, Any]]:
        """获取所有 Cookie

        Returns:
            Cookie 列表
        """
        return await self.driver.get_cookies()

    async def add_cookie(self, cookie: dict[str, Any]) -> None:
        """添加 Cookie

        Args:
            cookie: Cookie 数据
        """
        await self.driver.add_cookie(cookie)

    async def delete_cookie(self, name: str) -> None:
        """删除指定 Cookie

        Args:
            name: Cookie 名称
        """
        await self.driver.delete_cookie(name)

    async def delete_all_cookies(self) -> None:
        """删除所有 Cookie"""
        await self.driver.delete_all_cookies()
