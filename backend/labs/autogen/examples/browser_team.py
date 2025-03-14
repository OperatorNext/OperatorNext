"""
多代理浏览器诗歌创作团队 (Selenium版)

这个示例展示了如何使用AutoGen的Swarm模式创建一个多代理协作团队:
1. Planner(规划者) - 负责协调整个流程
2. BrowserAgent(浏览器代理) - 负责使用Selenium访问网站获取内容
3. PoetAgent(诗人代理) - 负责将网站内容转化为诗歌

使用多种终止条件控制对话流程。
"""

import asyncio
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import (
    MaxMessageTermination,
    TextMentionTermination,
    TimeoutTermination,
)
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

from labs.selenium.config import get_selenium_url

# 导入Selenium相关模块
from labs.selenium.factory import create_browser_controller


# Selenium浏览器会话管理器
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


# 浏览器工具函数
async def open_website(url: str, wait_for_load: bool = True) -> str:
    """
    使用Selenium在会话中打开网站并获取内容

    Args:
        url: 要访问的网站URL
        wait_for_load: 是否等待页面完全加载，默认为True

    Returns:
        str: 操作结果描述和页面内容
    """
    # 获取或创建浏览器会话
    session = await BrowserSession.get_instance()

    try:
        # 确保控制器已初始化
        if not session.controller:
            return "错误: Selenium浏览器未初始化"

        # 访问网页
        print(f"🌐 正在访问网站: {url}")
        await session.controller.navigate(url)

        # 更新会话状态
        session.current_url = await session.controller.get_current_url()

        # 获取页面标题
        session.current_title = await session.controller.get_title()
        print(f"📄 页面标题: {session.current_title}")

        # 等待额外加载
        if wait_for_load:
            # 等待2秒让页面完全加载
            await asyncio.sleep(2)
            print("✅ 页面加载完成")

        # 获取页面文本内容
        body_text = await session.controller.execute_js(
            "return document.body.innerText;"
        )

        # 构建结果消息
        result = (
            f"成功访问网站: {url}\n"
            f"页面标题: {session.current_title}\n\n"
            f"页面文本内容:\n{body_text[:5000]}..."
            if len(body_text) > 5000
            else body_text
        )

        return result

    except Exception as e:
        error_msg = f"访问网站时出错: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


async def type_text(selector: str, text: str) -> str:
    """
    在指定元素中输入文本

    Args:
        selector: CSS选择器，用于定位要输入文本的元素
        text: 要输入的文本内容

    Returns:
        str: 操作结果描述
    """
    # 获取当前浏览器会话
    session = await BrowserSession.get_instance()

    try:
        # 确保控制器已初始化
        if not session.controller:
            return "错误: Selenium浏览器未初始化"

        # 查找元素
        print(f"🔍 查找元素: {selector}")
        element = await session.controller.find_element_by_css(selector)

        if not element:
            return f"错误: 未找到元素 {selector}"

        # 输入文本
        print(f"⌨️ 在 {selector} 中输入文本: {text}")
        await session.controller.type_text(element, text)

        # 获取元素相关信息
        element_info = await session.controller.execute_js(
            f"const el = document.querySelector('{selector}'); "
            + "return { tag: el.tagName, id: el.id, class: el.className };"
        )

        return f"已成功在 {selector} 中输入文本: '{text}'\n元素信息: {element_info}"

    except Exception as e:
        error_msg = f"输入文本时出错: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


async def execute_js(script: str, selector: str = None) -> str:
    """
    执行JavaScript代码

    Args:
        script: 要执行的JavaScript代码
        selector: 可选的CSS选择器，如果提供，将在该元素上下文中执行脚本

    Returns:
        str: 操作结果描述和脚本执行结果
    """
    # 获取当前浏览器会话
    session = await BrowserSession.get_instance()

    try:
        # 确保控制器已初始化
        if not session.controller:
            return "错误: Selenium浏览器未初始化"

        # 准备执行脚本
        print(
            f"🔧 执行JavaScript代码{' (针对选择器: ' + selector + ')' if selector else ''}"
        )

        # 实际执行脚本
        if selector:
            # 首先查找元素
            element = await session.controller.find_element_by_css(selector)
            if not element:
                return f"错误: 未找到元素 {selector}"

            # 在元素上下文中执行脚本
            modified_script = f"const el = arguments[0]; {script}"
            result = await session.controller.execute_js(modified_script, element)
        else:
            # 在页面上下文中执行脚本
            result = await session.controller.execute_js(script)

        # 更新URL和标题，以防脚本导航到新页面
        session.current_url = await session.controller.get_current_url()
        session.current_title = await session.controller.get_title()

        return f"已成功执行JavaScript代码\n执行结果: {result}"

    except Exception as e:
        error_msg = f"执行JavaScript代码时出错: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


async def check_selenium_status() -> tuple[bool, str]:
    """检查Selenium Grid服务是否可用"""
    try:
        import aiohttp

        from labs.selenium.config import get_selenium_url

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


async def main():
    """主函数：运行多代理浏览器诗歌创作团队"""
    try:
        # 加载环境变量
        load_dotenv()

        # 检查Selenium服务状态
        success, message = await check_selenium_status()
        if not success:
            print(f"错误：{message}")
            print(
                "请先运行: docker-compose up -d selenium-hub selenium-chromium selenium-firefox"
            )
            return

        print(f"✅ {message}，地址: {get_selenium_url()}")

        # 从环境变量获取OpenAI配置
        openai_api_base = os.getenv("OPENAI_API_BASE")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")  # 默认使用gpt-4o

        print(f"🔑 使用API Base: {openai_api_base}")
        print(f"🤖 使用模型: {openai_model}")

        # 创建模型客户端，使用环境变量中的配置
        model_client = OpenAIChatCompletionClient(
            model=openai_model,  # 使用.env中的模型名称
            api_key=openai_api_key,  # 使用.env中的API密钥
            base_url=openai_api_base,  # 使用.env中的API基础URL
            parallel_tool_calls=False,  # 禁用并行工具调用
        )

        # 1. 创建规划者智能体 - 负责协调整个流程
        planner = AssistantAgent(
            name="Planner",
            model_client=model_client,
            # 规划者可以将任务交给浏览器代理或诗人代理
            handoffs=["BrowserAgent", "PoetAgent"],
            system_message="""你是一个负责协调网页诗歌创作流程的规划者。
你需要按照以下流程协调团队工作:
1. 首先让BrowserAgent使用Selenium访问指定网站并获取内容
2. 然后让PoetAgent将网站内容转化为优美的诗歌
3. 最后检查诗歌，确认完成后输出TERMINATE以结束任务

请确保每次只将任务交给一个代理，并等待其完成后再进行下一步。
请检查诗歌质量，如果满意则输出TERMINATE。""",
        )

        # 2. 创建浏览器代理 - 专门负责访问网站
        browser_agent = AssistantAgent(
            name="BrowserAgent",
            model_client=model_client,
            # 浏览器代理只能将任务交回给规划者
            handoffs=["Planner"],
            tools=[open_website, type_text, execute_js],  # 注册Selenium浏览器工具
            system_message="""你是一个专业的网页浏览器代理，负责使用Selenium访问网站并执行各种浏览器操作。
你有以下工具可用:
1. open_website(url, wait_for_load=True) - 打开指定网站并获取页面内容
2. type_text(selector, text) - 在指定元素中输入文本
3. execute_js(script, selector=None) - 执行JavaScript代码

当收到访问网站的请求时:
1. 使用open_website工具访问指定网站
2. 如果需要在输入框中输入文本，使用type_text工具
3. 如果需要点击元素或执行其他操作，使用execute_js工具
4. 提取并整理页面的关键内容，生成简洁的摘要
5. 整理内容后交回给Planner

当需要搜索内容时的一般操作流程:
1. 打开搜索引擎，如: await open_website("https://www.bing.com")
2. 在搜索框输入文本，如: await type_text("#sb_form_q", "要搜索的内容")
3. 执行搜索按钮点击，如: await execute_js("document.querySelector('.search-button').click()")
4. 获取搜索结果并整理

不要尝试创作诗歌，这是PoetAgent的任务。你的职责是获取和整理网站内容。""",
        )

        # 3. 创建诗人代理 - 专门负责创作诗歌
        poet_agent = AssistantAgent(
            name="PoetAgent",
            model_client=model_client,
            # 诗人代理只能将任务交回给规划者
            handoffs=["Planner"],
            system_message="""你是一位才华横溢的诗人，擅长将网页内容转化为优美的诗歌。
当你收到网页内容时:
1. 仔细分析内容的主题和情感
2. 创作一首优美、富有意境的诗歌，反映网站的核心内容
3. 确保诗歌有适当的结构和韵律
4. 将完成的诗歌交回给Planner

你的诗歌应该具有独特的风格和深度，能够打动读者。""",
        )

        # 设置多种终止条件
        # 1. 当Planner输出TERMINATE时终止
        text_termination = TextMentionTermination("TERMINATE")

        # 2. 最大消息数量限制(防止无限对话)
        max_msg_termination = MaxMessageTermination(max_messages=15)

        # 3. 对话超时限制(单位：秒)
        timeout_termination = TimeoutTermination(timeout_seconds=180)  # 3分钟超时

        # 组合终止条件：满足任一条件即终止
        combined_termination = (
            text_termination | max_msg_termination | timeout_termination
        )

        # 创建Swarm团队
        team = Swarm(
            participants=[planner, browser_agent, poet_agent],
            termination_condition=combined_termination,
        )

        # 改为使用Bing搜索的创作任务
        request = "请使用Bing搜索'人工智能诗歌创作'，然后根据搜索结果创作一首诗歌"

        # 运行团队
        print(f"\n🚀 启动多代理协作团队，执行任务: {request}\n")

        # 打印终止条件信息
        print("📝 终止条件设置:")
        print('  - Planner输出 "TERMINATE"')
        print("  - 最大消息数: 15条")
        print("  - 超时时间: 180秒")

        # 使用Console UI显示对话流程
        start_time = asyncio.get_event_loop().time()
        result = await Console(
            team.run_stream(
                task=TextMessage(content=request, source="user"),
                cancellation_token=CancellationToken(),
            )
        )
        end_time = asyncio.get_event_loop().time()

        # 打印执行统计信息
        print("\n✅ 任务完成!")
        print(f"⏱️ 总耗时: {end_time - start_time:.2f}秒")
        print(f"📊 终止原因: {result.stop_reason}")

        # 关闭浏览器会话
        session = await BrowserSession.get_instance()
        await session.close()

    except Exception as e:
        print(f"发生错误: {e}")
        import traceback

        traceback.print_exc()  # 打印完整的错误堆栈，方便调试

        # 确保关闭浏览器会话
        try:
            session = await BrowserSession.get_instance()
            await session.close()
        except Exception as e:
            print(f"关闭浏览器会话时出错: {e}")


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())
