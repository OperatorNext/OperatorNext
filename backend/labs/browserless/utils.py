"""
Browserless 工具类

提供与 Browserless 服务交互的基础工具和辅助函数。
"""

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from .config import get_ws_endpoint


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
            self.browser = await playwright.chromium.connect_over_cdp(
                get_ws_endpoint()
            )
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


async def create_browser_client() -> BrowserlessClient:
    """创建并初始化 Browserless 客户端"""
    client = BrowserlessClient()
    await client.connect()
    await client.new_context()
    await client.new_page()
    return client 