"""
Browserless 工具类

提供与 Browserless 服务交互的基础工具和辅助函数。
"""

from pathlib import Path
from typing import Any

import aiohttp
import requests
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
            code: 要执行的 JavaScript 代码（传统 JavaScript 语法）
            context: 传递给函数的上下文对象

        Returns:
            函数执行结果
        """
        session = await self._ensure_session()
        api_url = self._get_api_url("function")

        # 传统 JavaScript 函数格式
        payload = {"code": code}

        if context:
            payload["context"] = context

        async with session.post(api_url, json=payload) as response:
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(f"执行函数失败: {response.status} - {error_text}")

            try:
                # 尝试解析JSON响应
                return await response.json()
            except Exception as e:
                # 如果不是JSON，返回原始文本
                return {"text": await response.text(), "error": str(e)}

    async def execute_function_esm(
        self, code: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        执行自定义 ESM 函数（使用 sourceType=module 参数）

        注意：这需要 Browserless 服务器支持 ESM 模块，请确保已配置
             `FUNCTION_ENABLE_ESMODULES=true` 环境变量

        Args:
            code: 要执行的 JavaScript ESM 代码 (使用 import/export 语法)
            context: 传递给函数的上下文对象

        Returns:
            函数执行结果
        """
        session = await self._ensure_session()
        # 添加 sourceType=module 参数以支持 ESM 模块
        api_url = f"{self._get_api_url('function')}&sourceType=module"

        # 两种格式支持：JavaScript 代码或 JSON 格式
        if "import" in code or "export" in code:
            # 对于 ESM 模块格式，直接发送 JavaScript 代码
            headers = {"Content-Type": "application/javascript"}
            async with session.post(api_url, headers=headers, data=code) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise RuntimeError(
                        f"执行 ESM 函数失败: {response.status} - {error_text}"
                    )

                try:
                    # 尝试解析JSON响应
                    return await response.json()
                except Exception as e:
                    # 如果不是JSON，返回原始文本
                    return {"text": await response.text(), "error": str(e)}
        else:
            # 如果是普通代码或需要传递上下文，使用 JSON 格式
            payload = {"code": code}
            if context:
                payload["context"] = context

            async with session.post(api_url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise RuntimeError(
                        f"执行 ESM 函数失败: {response.status} - {error_text}"
                    )

                try:
                    # 尝试解析JSON响应
                    return await response.json()
                except Exception as e:
                    # 如果不是JSON，返回原始文本
                    return {"text": await response.text(), "error": str(e)}

    async def execute_function_with_optimal_format(
        self, code: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        智能选择最适合的函数执行格式

        这个方法会自动检测代码是否包含 ESM 语法（import/export），并使用合适的方法执行，
        如果执行失败，会自动尝试另一种格式。

        Args:
            code: 要执行的 JavaScript 代码
            context: 传递给函数的上下文对象

        Returns:
            函数执行结果
        """
        # 检测是否含有 ESM 语法
        has_esm_syntax = "import" in code or "export" in code

        try:
            # 首先尝试最可能成功的方法
            if has_esm_syntax:
                return await self.execute_function_esm(code, context)
            else:
                return await self.execute_function(code, context)
        except Exception as e:
            # 如果第一种方法失败，尝试另一种
            try:
                if has_esm_syntax:
                    # 从 ESM 转为普通函数格式
                    # 移除 import/export 语句，转为CommonJS格式
                    simplified_code = self._convert_esm_to_commonjs(code)
                    return await self.execute_function(simplified_code, context)
                else:
                    # 尝试使用 ESM 格式
                    return await self.execute_function_esm(code, context)
            except Exception as e2:
                # 如果两种方法都失败，抛出完整错误信息
                raise RuntimeError(
                    f"无法执行函数代码。ESM错误: {e}, 常规错误: {e2}\n代码: {code[:200]}..."
                )

    def _convert_esm_to_commonjs(self, esm_code: str) -> str:
        """
        将 ESM 模块代码转换为 CommonJS 格式

        这是一个简单的转换，不能处理所有复杂情况，但对于简单的代码应该有效

        Args:
            esm_code: ESM 模块格式的代码

        Returns:
            CommonJS 格式的代码
        """
        # 移除导入语句，在函数内使用 require 替代
        import_lines = []
        other_lines = []
        export_default_found = False

        for line in esm_code.split("\n"):
            stripped = line.strip()
            if stripped.startswith("import "):
                # 收集导入语句，但不添加到新代码中
                import_lines.append(line)
            elif stripped.startswith("export default function"):
                # 修改默认导出函数为普通函数
                other_lines.append(
                    line.replace("export default function", "function handler")
                )
                export_default_found = True
            elif stripped.startswith("export default"):
                # 修改默认导出为处理程序
                other_lines.append(line.replace("export default", "const handler ="))
                export_default_found = True
            else:
                other_lines.append(line)

        # 如果没有找到默认导出，添加一个处理函数包装
        if not export_default_found:
            common_js = "function handler(args) {\n"
            common_js += "\n".join(["  " + line for line in other_lines])
            common_js += "\n}"
        else:
            common_js = "\n".join(other_lines)

            # 确保最后有返回处理函数
            if "return handler" not in common_js:
                common_js += "\n\nreturn handler;"

        return common_js

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


async def execute_function_esm(
    code: str,
    context: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    通过 Browserless 的 function API 执行 ESM 模块代码

    根据官方文档，function API 支持两种调用方式：
    1. 直接发送 JavaScript 代码（Content-Type: application/javascript）
    2. 发送包含代码和上下文的 JSON 对象（Content-Type: application/json）

    Args:
        code: 要执行的 JavaScript 代码（ECMAScript 模块格式）
        context: 传递给函数的上下文对象
        headers: 自定义请求头

    Returns:
        函数执行结果
    """
    try:
        # 获取API URL
        base_url = get_browserless_url()
        token = get_browserless_token()

        # 添加sourceType=module参数以支持ESM模块
        api_url = f"{base_url}/function?token={token}&sourceType=module"

        # 根据情况决定请求方式
        if (
            headers
            and "Content-Type" in headers
            and headers["Content-Type"] == "application/javascript"
        ):
            # 方式1: 直接发送JavaScript代码
            response = requests.post(api_url, headers=headers, data=code)
        else:
            # 方式2: 发送JSON对象
            payload = {"code": code}
            if context:
                payload["context"] = context

            response = requests.post(api_url, json=payload)

        # 处理响应
        if response.status_code != 200:
            error_text = response.text
            raise RuntimeError(f"执行函数失败: {response.status_code} - {error_text}")

        # 解析响应
        try:
            result = response.json()
            return result
        except Exception:
            return {"data": response.text, "type": "text/plain"}

    except Exception as e:
        raise e
