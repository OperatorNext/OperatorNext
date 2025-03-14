"""
会话管理器

提供浏览器会话和代码会话的管理类，使用单例模式确保资源共享和一致性。
"""

import os
import sys

import e2b_code_interpreter

# 添加项目根目录到 Python 路径
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
    )
)

from backend.labs.e2b import create_code_executor
from backend.labs.e2b.config import get_e2b_api_key
from backend.labs.selenium.factory import create_browser_controller


class BrowserSession:
    """浏览器会话管理器，维护Selenium浏览器会话状态以支持连续操作"""

    _instance = None

    @classmethod
    async def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = BrowserSession()
            await cls._instance.initialize()
        return cls._instance

    def __init__(self):
        """初始化会话管理器"""
        self.controller = None
        self.current_url = None
        self.current_title = None
        self.initialized = False

    async def initialize(self):
        """初始化Selenium浏览器控制器"""
        if not self.initialized:
            print("🌐 初始化Selenium浏览器会话...")
            options = {
                "headless": False,  # 使用非无头模式，便于调试观察
                "window_size": (1280, 800),  # 设置窗口大小
            }
            self.controller = await create_browser_controller(
                browser="chromium", options=options
            )
            self.initialized = True
            print("✅ Selenium浏览器会话初始化完成")

    async def close(self):
        """关闭浏览器会话"""
        if self.controller:
            print("🔄 关闭Selenium浏览器会话...")
            await self.controller.close()
            self.controller = None
            self.initialized = False
            BrowserSession._instance = None
            print("✅ Selenium浏览器会话已关闭")


class CodeSession:
    """代码会话管理器，维护E2B沙盒会话状态以支持连续操作"""

    _instance = None

    @classmethod
    async def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = CodeSession()
            await cls._instance.initialize()
        return cls._instance

    def __init__(self):
        """初始化会话管理器"""
        self.executor = None
        self.initialized = False
        self.current_files = []
        self.installed_packages = set()

    async def initialize(self):
        """初始化E2B沙盒执行器"""
        if not self.initialized:
            print("🚀 初始化E2B沙盒会话...")
            self.executor = await create_code_executor()
            self.initialized = True
            print("✅ E2B沙盒会话初始化完成")

    async def close(self):
        """关闭沙盒会话"""
        if self.executor:
            print("🔄 关闭E2B沙盒会话...")
            await self.executor.close()
            self.executor = None
            self.initialized = False
            CodeSession._instance = None
            print("✅ E2B沙盒会话已关闭")


async def check_selenium_status() -> tuple[bool, str]:
    """检查Selenium Grid服务是否可用"""
    try:
        import aiohttp
        from backend.labs.selenium.config import get_selenium_url

        selenium_url = get_selenium_url()

        # 将嵌套的async with合并为单一语句
        async with (
            aiohttp.ClientSession() as session,
            session.get(f"{selenium_url}/status") as response,
        ):
            if response.status == 200:
                data = await response.json()
                if data.get("value", {}).get("ready", False):
                    return True, "Selenium Grid服务正常运行"
                else:
                    return False, "Selenium Grid服务已启动，但未就绪"
            else:
                return False, f"Selenium Grid服务返回错误码: {response.status}"
    except Exception as e:
        return False, f"Selenium Grid服务检查失败: {str(e)}"


async def check_e2b_status() -> tuple[bool, str]:
    """检查E2B服务是否可用"""
    try:
        # 尝试创建一个临时执行器来验证E2B API工作正常
        api_key = get_e2b_api_key()
        if not api_key:
            return False, "E2B API密钥未设置，请在.env文件中配置E2B_API_KEY"

        # 检查是否已导入E2B SDK
        if not e2b_code_interpreter:
            return False, "未安装E2B SDK，请执行: pip install e2b_code_interpreter"

        # 创建临时执行器
        executor = await create_code_executor()

        # 执行一个简单的测试
        result = await executor.run_code("print('E2B沙盒测试')")
        await executor.close()

        if result["success"]:
            return True, "E2B服务正常运行"
        else:
            return False, f"E2B服务返回错误: {result['error']}"

    except Exception as e:
        return False, f"E2B服务检查失败: {str(e)}"
