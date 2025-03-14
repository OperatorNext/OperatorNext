#!/usr/bin/env python

"""
四代理协作系统 - 网络检索+代码执行+数据分析的协作团队

这个示例展示了如何使用AutoGen的Swarm模式创建一个四代理协作团队:
1. Planner(规划者) - 负责协调整个流程
2. BrowserAgent(浏览器代理) - 负责网络浏览和内容检索
3. CodeAgent(代码代理) - 负责代码执行和文件处理
4. AnalystAgent(分析师代理) - 负责数据分析和结果解释

团队可以处理需要网络检索+代码执行+数据分析的复杂任务，例如：
- 从网络获取数据后进行分析
- 基于网络信息编写和执行代码
- 对编程问题进行在线搜索并实现解决方案
- 综合分析互联网上的数据集

使用多种终止条件控制对话流程，确保任务能够可靠完成。
"""

import asyncio
import os
import sys
import traceback

# 添加项目根目录到 Python 路径
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
    )
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

# 导入会话管理模块和工具函数
from .browser_tools import (
    execute_js,
    get_page_content,
    open_website,
    screenshot,
    search_on_web,
    type_text,
)
from .code_tools import (
    generate_chart,
    install_package,
    list_files,
    read_file,
    run_code,
    write_file,
)
from .sessions import (
    BrowserSession,
    CodeSession,
    check_e2b_status,
    check_selenium_status,
)


async def main():
    """主函数：运行四代理协作系统"""
    try:
        # 加载环境变量
        load_dotenv()

        # 检查服务状态
        browser_success, browser_message = await check_selenium_status()
        code_success, code_message = await check_e2b_status()

        if not browser_success:
            print(f"❌ 浏览器服务检查失败: {browser_message}")
            print(
                "请先运行: docker-compose up -d selenium-hub selenium-chromium selenium-firefox"
            )
            return

        if not code_success:
            print(f"❌ 代码执行服务检查失败: {code_message}")
            print("请确保已安装必要的包: pip install e2b_code_interpreter aiofiles")
            return

        print(f"✅ 浏览器服务: {browser_message}")
        print(f"✅ 代码执行服务: {code_message}")

        # 从环境变量获取OpenAI配置
        openai_api_base = os.getenv("OPENAI_API_BASE")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")  # 默认使用gpt-4o

        print(f"🔑 使用API Base: {openai_api_base or 'OpenAI默认'}")
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
            # 规划者可以将任务交给所有专业代理
            handoffs=["BrowserAgent", "CodeAgent", "AnalystAgent"],
            system_message="""你是一个高级项目规划者，负责协调由网络检索、代码执行和数据分析组成的复杂任务。
你的团队包括三位专业代理:

1. BrowserAgent - 负责网络浏览和内容检索
   - 能够访问网站、执行搜索、提取网页内容
   - 使用Selenium自动化技术与网页交互

2. CodeAgent - 负责代码执行和文件处理
   - 能在安全沙盒中执行Python代码
   - 安装第三方软件包
   - 对数据进行处理和可视化

3. AnalystAgent - 负责数据分析与结果解释
   - 提供对数据集的专业分析
   - 解释执行结果和数据可视化
   - 提供统计洞察和建议

工作流程:
1. 首先分析用户的需求，设计解决方案
2. 将网络检索任务交给BrowserAgent(如需网络数据)
3. 将代码执行任务交给CodeAgent(如需代码处理)
4. 将数据分析任务交给AnalystAgent(如需专业解读)
5. 最后总结整个流程，确认完成后输出TERMINATE以结束任务

请确保:
- 每次只将任务交给一个代理，等待其完成后再进行下一步
- 根据任务性质选择合适的专业代理
- 跟踪任务进度，确保所有步骤都得到妥善处理
- 当所有任务完成后，输出TERMINATE以结束流程""",
        )

        # 2. 创建浏览器代理 - 专门负责网络浏览和内容检索
        browser_agent = AssistantAgent(
            name="BrowserAgent",
            model_client=model_client,
            # 浏览器代理只能将任务交回给规划者
            handoffs=["Planner"],
            tools=[
                open_website,
                search_on_web,
                screenshot,
                type_text,
                execute_js,
                get_page_content,
            ],  # 注册浏览器工具
            system_message="""你是一个专业的网络浏览代理，负责网络信息检索和网页交互。
你使用Selenium自动化技术操作浏览器，可以访问网站、搜索信息、提取内容。

你有以下工具可用:
1. open_website(url, wait_for_load=True) - 打开指定网站并获取页面内容
2. search_on_web(query, search_engine="bing") - 在搜索引擎上执行搜索
3. screenshot(selector=None, filename=None) - 对整个页面或特定元素进行截图
4. type_text(selector, text) - 在指定元素中输入文本
5. execute_js(script, selector=None) - 执行JavaScript代码
6. get_page_content(content_type="both") - 获取当前页面的HTML源码和文本内容

处理网页交互时的最佳实践：
1. 在尝试与页面元素交互前，务必先使用get_page_content获取页面内容，分析页面结构
2. 当遇到"element not interactable"错误时：
   - 使用get_page_content查看页面HTML，找出元素的实际ID、class或其他选择器
   - 尝试使用execute_js执行JavaScript来模拟点击或获取信息
   - 考虑等待页面加载(等待1-3秒)或使用JavaScript检查元素是否可见

搜索引擎使用技巧：
1. 打开搜索引擎网站(open_website)
2. 使用get_page_content分析搜索框位置和ID
3. 使用type_text或execute_js填入搜索内容
4. 使用execute_js模拟回车键提交搜索: execute_js("document.querySelector('你的选择器').form.submit()")
5. 等待结果加载后，再次使用get_page_content获取搜索结果

当收到网络检索任务时:
1. 根据任务需求选择合适的工具
2. 通过页面分析确保正确找到并操作元素
3. 提取关键信息，过滤无关内容，生成简洁的摘要
4. 如果内容过多，关注最重要、最相关的部分
5. 整理内容后交回给Planner

你应当:
- 关注事实和客观信息
- 提供内容的来源出处
- 规避不适当或有害内容
- 注意区分广告内容和实际结果
- 不要尝试编写代码或进行数据分析，那些是其他代理的工作""",
        )

        # 3. 创建代码代理 - 专门负责代码执行和文件处理
        code_agent = AssistantAgent(
            name="CodeAgent",
            model_client=model_client,
            # 代码代理只能将任务交回给规划者
            handoffs=["Planner"],
            tools=[
                run_code,
                install_package,
                list_files,
                read_file,
                write_file,
                generate_chart,
            ],  # 注册E2B工具
            system_message="""你是一个专业的代码执行代理，负责在安全沙盒中执行Python代码。
你有以下工具可用:
1. run_code(code) - 在沙盒中执行Python代码
2. install_package(package_name) - 安装Python包
3. list_files(path="/") - 列出目录中的文件
4. read_file(file_path) - 读取文件内容
5. write_file(file_path, content) - 写入文件
6. generate_chart(data_file, chart_type="bar") - 生成数据可视化图表

当收到代码执行任务时:
1. 分析任务需求，规划代码执行流程
2. 如果需要依赖包，使用install_package安装
3. 使用write_file创建必要的文件
4. 使用run_code执行代码
5. 使用list_files和read_file检查结果
6. 如果需要数据可视化，使用generate_chart生成图表

你应遵循以下原则:
- 编写清晰、注释详尽的代码
- 代码应包含错误处理
- 合理拆分复杂任务为多个步骤
- 确保环境清理和资源释放
- 检查执行结果并报告任何错误
- 代码应该是可重现的
- 代码输出应该是信息丰富且易于理解的""",
        )

        # 4. 创建分析师代理 - 专门负责数据分析与结果解释
        analyst_agent = AssistantAgent(
            name="AnalystAgent",
            model_client=model_client,
            # 分析师代理只能将任务交回给规划者
            handoffs=["Planner"],
            tools=[read_file],  # 分析师只需要读取文件的工具
            system_message="""你是一位专业的数据分析师，擅长解释代码执行结果和分析数据。
你可以使用read_file工具查看数据文件和结果文件。

当收到数据分析任务时:
1. 仔细研究代码执行结果和生成的数据
2. 提供专业的数据解读和见解
3. 指出数据中的关键趋势、模式或异常
4. 若有图表，解释图表呈现的信息
5. 评估结果的可靠性和局限性
6. 提供进一步分析的建议

你的分析应该具备以下特点:
- 专业、深入且客观
- 使用适当的统计术语和概念
- 避免过度解读数据
- 清晰区分事实与推测
- 考虑潜在的误差和偏差
- 适当引用相关理论或研究
- 使用清晰的语言解释复杂的概念
- 在适当的地方提供改进建议和后续步骤

完成分析后，将你的专业见解交回给Planner。""",
        )

        # 设置多种终止条件
        # 1. 当Planner输出TERMINATE时终止
        text_termination = TextMentionTermination("TERMINATE")

        # 2. 最大消息数量限制(防止无限对话)
        max_msg_termination = MaxMessageTermination(max_messages=40)

        # 3. 对话超时限制(单位：秒)
        timeout_termination = TimeoutTermination(timeout_seconds=900)  # 15分钟超时

        # 组合终止条件：满足任一条件即终止
        combined_termination = (
            text_termination | max_msg_termination | timeout_termination
        )

        # 创建Swarm团队
        team = Swarm(
            participants=[planner, browser_agent, code_agent, analyst_agent],
            termination_condition=combined_termination,
        )

        # 示例任务
        request = """请帮我完成以下任务:
1. 使用搜索引擎查找"Python pandas数据分析最佳实践"，获取相关信息
2. 基于搜索结果，创建一个包含示例数据的CSV文件
3. 使用pandas进行数据清洗和基本分析
4. 生成数据可视化图表
5. 提供专业的数据分析报告和最佳实践建议
"""

        # 运行团队
        print(f"\n🚀 启动四代理协作团队，执行任务:\n{request}\n")

        # 打印终止条件信息
        print("📝 终止条件设置:")
        print('  - Planner输出 "TERMINATE"')
        print("  - 最大消息数: 40条")
        print("  - 超时时间: 900秒 (15分钟)")

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

        # 关闭会话
        browser_session = await BrowserSession.get_instance()
        code_session = await CodeSession.get_instance()

        await browser_session.close()
        await code_session.close()

    except Exception as e:
        print(f"发生错误: {e}")
        traceback.print_exc()  # 打印完整的错误堆栈，方便调试

        # 确保关闭会话
        try:
            browser_session = await BrowserSession.get_instance()
            code_session = await CodeSession.get_instance()

            await browser_session.close()
            await code_session.close()
        except Exception as e:
            print(f"关闭会话时出错: {e}")


# 允许直接运行此文件
if __name__ == "__main__":
    asyncio.run(main())
