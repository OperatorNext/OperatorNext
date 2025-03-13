"""
Browserless 工具类

提供与 Browserless 服务交互的基础工具和辅助函数。
"""

from pathlib import Path
from typing import Any

import aiohttp
from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from .config import get_browserless_token, get_browserless_url, get_ws_endpoint


class BrowserlessClient:
    """Browserless 客户端"""

    def __init__(self):
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    async def connect(self) -> Browser:
        """连接到 Browserless 服务"""
        if self.browser is None:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.connect_over_cdp(get_ws_endpoint())
        return self.browser

    async def new_context(self, **kwargs) -> BrowserContext:
        """创建新的浏览器上下文"""
        if self.browser is None:
            await self.connect()
        self.context = await self.browser.new_context(**kwargs)
        return self.context

    async def new_page(self) -> Page:
        """创建新的页面"""
        if self.context is None:
            await self.new_context()
        self.page = await self.context.new_page()
        return self.page

    async def close(self):
        """关闭所有连接"""
        if self.page:
            await self.page.close()
            self.page = None

        if self.context:
            await self.context.close()
            self.context = None

        if self.browser:
            await self.browser.close()
            self.browser = None


class HTTPBrowserlessClient:
    """Browserless HTTP API 客户端"""

    def __init__(self):
        self.base_url = get_browserless_url()
        self.token = get_browserless_token()
        self.session = None

    async def _ensure_session(self):
        """确保 HTTP 会话已创建"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    def _get_api_url(self, endpoint: str) -> str:
        """获取完整的 API URL"""
        return f"{self.base_url}/{endpoint}?token={self.token}"

    async def connect(self):
        """创建 HTTP 会话"""
        await self._ensure_session()
        return self

    async def close(self):
        """关闭 HTTP 会话"""
        if self.session:
            await self.session.close()
            self.session = None

    async def get_content(
        self,
        url: str,
        wait_for: dict[str, Any] | None = None,
        goto_options: dict[str, Any] | None = None,
    ) -> str:
        """
        获取网页内容

        Args:
            url: 网页地址
            wait_for: 等待选项，如 {"selector": "h1", "timeout": 5000}
            goto_options: 导航选项，如 {"waitUntil": "networkidle2"}

        Returns:
            网页 HTML 内容
        """
        session = await self._ensure_session()
        api_url = self._get_api_url("content")

        payload = {"url": url}

        # Browserless v2 中 content API 不支持等待选项，直接使用 goto 选项
        if goto_options:
            payload["gotoOptions"] = goto_options

        async with session.post(api_url, json=payload) as response:
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(f"获取内容失败: {response.status} - {error_text}")

            return await response.text()

    async def take_screenshot(
        self,
        url: str,
        output_path: str | Path,
        options: dict[str, Any] | None = None,
        wait_for: dict[str, Any] | None = None,
    ) -> Path:
        """
        网页截图

        Args:
            url: 网页地址
            output_path: 输出文件路径
            options: 截图选项，如 {"fullPage": True, "type": "png"}
            wait_for: 等待选项，如 {"selector": "h1", "timeout": 5000}

        Returns:
            截图保存路径
        """
        session = await self._ensure_session()
        api_url = self._get_api_url("screenshot")

        payload = {"url": url}

        if options:
            payload["options"] = options

        # 截图 API 不支持 waitForSelector，调整为 gotoOptions
        if wait_for and "timeout" in wait_for:
            payload["gotoOptions"] = {
                "waitUntil": "networkidle2",
                "timeout": wait_for["timeout"],
            }

        output_path = Path(output_path)
        output_path.parent.mkdir(exist_ok=True, parents=True)

        async with session.post(api_url, json=payload) as response:
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(f"截图失败: {response.status} - {error_text}")

            with open(output_path, "wb") as f:
                f.write(await response.read())

            return output_path

    async def generate_pdf(
        self,
        url: str,
        output_path: str | Path,
        options: dict[str, Any] | None = None,
        wait_for: dict[str, Any] | None = None,
        goto_options: dict[str, Any] | None = None,
    ) -> Path:
        """
        生成 PDF

        Args:
            url: 网页地址
            output_path: 输出文件路径
            options: PDF 选项，如 {"format": "A4", "printBackground": True}
            wait_for: 等待选项，如 {"selector": "h1", "timeout": 5000}
            goto_options: 导航选项，如 {"waitUntil": "networkidle2"}

        Returns:
            PDF 保存路径
        """
        session = await self._ensure_session()
        api_url = self._get_api_url("pdf")

        payload = {"url": url}

        if options:
            payload["options"] = options

        # 处理导航选项
        if goto_options:
            payload["gotoOptions"] = goto_options
        # PDF API 不支持 waitForTimeout，如果有 wait_for 参数，转为 gotoOptions
        elif wait_for and "timeout" in wait_for:
            payload["gotoOptions"] = {
                "waitUntil": "networkidle2",
                "timeout": wait_for["timeout"],
            }

        output_path = Path(output_path)
        output_path.parent.mkdir(exist_ok=True, parents=True)

        async with session.post(api_url, json=payload) as response:
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(f"生成 PDF 失败: {response.status} - {error_text}")

            with open(output_path, "wb") as f:
                f.write(await response.read())

            return output_path

    async def execute_function(
        self, code: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        执行自定义函数

        Args:
            code: 要执行的 JavaScript 代码
            context: 传递给函数的上下文对象

        Returns:
            函数执行结果
        """
        session = await self._ensure_session()
        api_url = self._get_api_url("function")

        # 函数代码不应包含 import/export 语句，使用 function 函数定义
        # 去掉 ES 模块语法 (export default)
        if "export default" in code:
            code = code.replace("export default", "")

        payload = {"code": code}

        if context:
            payload["context"] = context

        async with session.post(api_url, json=payload) as response:
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(f"执行函数失败: {response.status} - {error_text}")

            return await response.json()

    async def download_file(
        self, code: str, output_path: str | Path, context: dict[str, Any] | None = None
    ) -> Path:
        """
        下载文件

        Args:
            code: 要执行的 JavaScript 代码
            output_path: 输出文件路径
            context: 传递给函数的上下文对象

        Returns:
            文件保存路径
        """
        session = await self._ensure_session()
        api_url = self._get_api_url("download")

        # 函数代码不应包含 import/export 语句，使用 function 函数定义
        # 去掉 ES 模块语法 (export default)
        if "export default" in code:
            code = code.replace("export default", "")

        payload = {"code": code}

        if context:
            payload["context"] = context

        output_path = Path(output_path)
        output_path.parent.mkdir(exist_ok=True, parents=True)

        async with session.post(api_url, json=payload) as response:
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(f"下载文件失败: {response.status} - {error_text}")

            with open(output_path, "wb") as f:
                f.write(await response.read())

            return output_path

    async def unblock(
        self, url: str, options: dict[str, Any] | None = None, proxy: str | None = None
    ) -> dict[str, Any]:
        """
        绕过反爬检测

        Args:
            url: 网页地址
            options: 选项，如 {"browserWSEndpoint": True, "cookies": True,
                               "content": False, "screenshot": False}
            proxy: 代理类型，如 "residential"

        Returns:
            包含解除阻止内容的响应
        """
        session = await self._ensure_session()

        # 使用正确的API端点
        api_url = self._get_api_url("function")  # 使用 function API 来执行反爬代码
        if proxy:
            api_url += f"&proxy={proxy}"

        # 准备请求数据
        payload = {
            "code": """
            async function unblock(context) {
                const { page } = context;
                await page.goto(context.url, { waitUntil: 'networkidle0' });
                return {
                    content: await page.content(),
                    cookies: await page.cookies()
                };
            }
            """,
            "context": {"url": url},
        }

        # 合并选项
        if options:
            payload["context"].update(options)

        # 发送请求
        async with session.post(api_url, json=payload) as response:
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(f"绕过检测失败: {response.status} - {error_text}")

            return await response.json()

    async def scrape(
        self, url: str, options: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        结构化抓取网页内容

        Args:
            url: 网页地址
            options: 抓取选项，如 {
                "elements": [{"selector": "h1"}, {"selector": "p"}],
                "gotoOptions": {"timeout": 10000, "waitUntil": "networkidle2"}
            }

        Returns:
            结构化抓取结果
        """
        session = await self._ensure_session()
        api_url = self._get_api_url("scrape")

        # 准备请求数据
        payload = {"url": url}

        # 合并选项，但移除不支持的waitForSelector
        if options:
            cleaned_options = options.copy()
            if "waitForSelector" in cleaned_options:
                # 将waitForSelector转换为gotoOptions格式
                wait_for = cleaned_options.pop("waitForSelector")
                if "gotoOptions" not in cleaned_options:
                    cleaned_options["gotoOptions"] = {}

                if "timeout" in wait_for:
                    cleaned_options["gotoOptions"]["timeout"] = wait_for["timeout"]

                cleaned_options["gotoOptions"]["waitUntil"] = "networkidle2"

            payload.update(cleaned_options)

        # 发送请求
        async with session.post(api_url, json=payload) as response:
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(f"结构化抓取失败: {response.status} - {error_text}")

            return await response.json()

    async def analyze_performance(
        self, url: str, options: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        分析网站性能

        Args:
            url: 网页地址
            options: 性能分析选项，如 {
                "config": {
                    "extends": "lighthouse:default",
                    "settings": {
                        "onlyCategories": ["performance"]
                    }
                }
            }

        Returns:
            性能分析结果
        """
        session = await self._ensure_session()
        # 使用正确的API端点
        api_url = self._get_api_url("function")  # 使用 function API 来执行 Lighthouse

        # 准备请求数据
        payload = {
            "code": """
            async function analyze(context) {
                const { page } = context;
                await page.goto(context.url, { waitUntil: 'networkidle0' });
                
                // 使用内置的 Lighthouse 进行分析
                const result = await page.evaluate(async () => {
                    const lighthouse = require('lighthouse');
                    const config = {
                        extends: 'lighthouse:default',
                        settings: { onlyCategories: ['performance'] }
                    };
                    return await lighthouse(context.url, config);
                });
                
                return result;
            }
            """,
            "context": {"url": url},
        }

        # 合并选项
        if options:
            payload["context"].update(options)

        # 发送请求
        async with session.post(api_url, json=payload) as response:
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(f"性能分析失败: {response.status} - {error_text}")

            return await response.json()


async def create_browser_client() -> BrowserlessClient:
    """创建并初始化 Browserless 客户端"""
    client = BrowserlessClient()
    await client.connect()
    await client.new_context()
    await client.new_page()
    return client


async def create_http_client() -> HTTPBrowserlessClient:
    """创建并初始化 Browserless HTTP API 客户端"""
    client = HTTPBrowserlessClient()
    await client.connect()
    return client
