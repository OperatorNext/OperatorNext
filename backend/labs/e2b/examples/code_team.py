#!/usr/bin/env python

"""
多代理代码沙盒执行团队 (E2B版)

这个示例展示了如何使用AutoGen的Swarm模式创建一个多代理协作团队:
1. Planner(规划者) - 负责协调整个流程
2. CodeAgent(代码代理) - 负责使用E2B沙盒执行代码
3. AnalystAgent(分析师代理) - 负责分析数据和结果

使用多种终止条件控制对话流程。
"""

import asyncio
import os
import traceback

import e2b_code_interpreter
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

from labs.e2b import create_code_executor
from labs.e2b.config import get_e2b_api_key
from labs.e2b.utils import generate_data_visualization_code


# E2B代码会话管理器
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


# 代码工具函数
async def run_code(code: str) -> str:
    """
    在E2B沙盒中运行代码并返回结果

    Args:
        code: 要执行的Python代码

    Returns:
        str: 执行结果
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 执行代码
        print("🧪 执行代码...")
        result = await session.executor.run_code(code)

        # 更新文件列表
        try:
            session.current_files = await session.executor.list_files("/")
        except Exception as e:
            print(f"警告: 无法更新文件列表: {str(e)}")

        # 格式化输出
        if result["success"]:
            output = "✅ 代码执行成功:\n\n"

            if result["logs"] and result["logs"].stdout:
                output += (
                    "输出:\n```\n" + "\n".join(result["logs"].stdout) + "\n```\n\n"
                )

            if result["logs"] and result["logs"].stderr:
                output += (
                    "警告/错误:\n```\n" + "\n".join(result["logs"].stderr) + "\n```\n\n"
                )

            output += "当前沙盒中的文件:\n"
            file_list = [f"- {f['name']}" for f in session.current_files]
            output += "\n".join(file_list) if file_list else "- (无文件)"

            return output
        else:
            return f"❌ 代码执行失败:\n\n```\n{result['error']}\n```"

    except Exception as e:
        return f"❌ 运行代码时出错: {str(e)}"


async def install_package(package_name: str) -> str:
    """
    在E2B沙盒中安装Python包

    Args:
        package_name: 要安装的包名称

    Returns:
        str: 安装结果
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 检查包是否已安装
        if package_name in session.installed_packages:
            return f"📦 {package_name} 已经安装"

        # 安装包
        print(f"📦 安装包: {package_name}")
        result = await session.executor.install_package(package_name)

        # 如果安装成功，添加到已安装包集合
        if result["success"]:
            session.installed_packages.add(package_name)

        # 格式化输出
        if result["success"]:
            output = f"✅ 成功安装包: {package_name}\n\n"

            if result["logs"] and result["logs"].stdout:
                output += "安装日志摘要:\n```\n"
                log_lines = "\n".join(result["logs"].stdout)
                # 如果日志太长，只显示前后一部分
                if len(log_lines) > 1000:
                    output += log_lines[:500] + "\n...\n" + log_lines[-500:]
                else:
                    output += log_lines
                output += "\n```"

            return output
        else:
            return f"❌ 安装包失败: {package_name}\n\n```\n{result['error']}\n```"

    except Exception as e:
        return f"❌ 安装包时出错: {str(e)}"


async def list_files(path: str = "/") -> str:
    """
    列出E2B沙盒中的文件

    Args:
        path: 要列出文件的目录路径

    Returns:
        str: 文件列表
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 列出文件
        print(f"📂 列出目录: {path}")
        files = await session.executor.list_files(path)

        # 保存到会话状态
        if path == "/":
            session.current_files = files

        # 格式化输出
        if not files:
            return f"目录 {path} 中没有文件"

        output = f"📂 目录 {path} 中的文件:\n\n"

        # 分别处理目录和文件
        directories = [f for f in files if f["is_dir"]]
        regular_files = [f for f in files if not f["is_dir"]]

        if directories:
            output += "目录:\n"
            for d in directories:
                output += f"- 📁 {d['name']}\n"
            output += "\n"

        if regular_files:
            output += "文件:\n"
            for f in regular_files:
                size_str = f" ({f['size']} 字节)" if f["size"] is not None else ""
                output += f"- 📄 {f['name']}{size_str}\n"

        return output

    except Exception as e:
        return f"❌ 列出文件时出错: {str(e)}"


async def read_file(file_path: str) -> str:
    """
    读取E2B沙盒中的文件内容

    Args:
        file_path: 文件路径

    Returns:
        str: 文件内容
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 读取文件
        print(f"📖 读取文件: {file_path}")
        content = await session.executor.read_file(file_path)

        # 检测文件类型并适当处理
        if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            return f"图像文件 {file_path} 的二进制数据不显示，大小: {len(content)} 字节"

        elif file_path.lower().endswith(
            (".pdf", ".zip", ".gz", ".tar", ".exe", ".bin")
        ):
            return f"二进制文件 {file_path} 的数据不显示，大小: {len(content)} 字节"

        else:
            # 尝试解码为文本
            try:
                text_content = content.decode("utf-8")
                # 如果文件过大，只显示部分内容
                if len(text_content) > 5000:
                    return f"📄 文件 {file_path} 内容 (前5000字符):\n\n```\n{text_content[:5000]}\n...(还有 {len(text_content) - 5000} 字符未显示)...\n```"
                else:
                    return f"📄 文件 {file_path} 内容:\n\n```\n{text_content}\n```"
            except UnicodeDecodeError:
                return (
                    f"二进制文件 {file_path} 无法解码为文本，大小: {len(content)} 字节"
                )

    except Exception as e:
        return f"❌ 读取文件时出错: {str(e)}"


async def write_file(file_path: str, content: str) -> str:
    """
    写入文件到E2B沙盒

    Args:
        file_path: 文件路径
        content: 文件内容

    Returns:
        str: 操作结果
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 写入文件
        print(f"✏️ 写入文件: {file_path}")
        result = await session.executor.write_file(file_path, content)

        # 更新文件列表
        try:
            session.current_files = await session.executor.list_files("/")
        except Exception as e:
            print(f"警告: 无法更新文件列表: {str(e)}")

        # 格式化输出
        if result["success"]:
            return f"✅ 文件已成功写入: {file_path}"
        else:
            return f"❌ 写入文件失败: {result['message']}"

    except Exception as e:
        return f"❌ 写入文件时出错: {str(e)}"


async def generate_chart(data_file: str, chart_type: str = "bar") -> str:
    """
    根据数据文件生成图表

    Args:
        data_file: 数据文件路径
        chart_type: 图表类型，支持 'bar', 'line', 'scatter', 'pie'

    Returns:
        str: 操作结果
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 检查文件是否存在
        print(f"📊 生成{chart_type}图表，数据文件: {data_file}")

        # 获取可视化代码
        viz_code = generate_data_visualization_code(data_file, chart_type)

        # 执行代码生成图表
        result = await session.executor.run_code(viz_code)

        # 更新文件列表
        session.current_files = await session.executor.list_files("/")

        # 格式化输出
        if result["success"]:
            chart_file = "/chart.png"

            # 检查图表文件是否生成
            if any(f["path"] == chart_file for f in session.current_files):
                return f"✅ 图表生成成功: {chart_file}\n\n图表类型: {chart_type}\n数据源: {data_file}"
            else:
                return f"⚠️ 代码执行成功，但未找到图表文件。日志输出:\n\n```\n{result['logs'].stdout if result['logs'] and result['logs'].stdout else '无输出'}\n```"
        else:
            return f"❌ 生成图表失败:\n\n```\n{result['error']}\n```"

    except Exception as e:
        return f"❌ 生成图表时出错: {str(e)}"


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


async def main():
    """主函数：运行多代理代码沙盒执行团队"""
    try:
        # 加载环境变量
        load_dotenv()

        # 检查E2B服务状态
        success, message = await check_e2b_status()
        if not success:
            print(f"错误：{message}")
            print("请确保已安装必要的包: pip install e2b_code_interpreter aiofiles")
            return

        print(f"✅ {message}")

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
            # 规划者可以将任务交给代码代理或分析师代理
            handoffs=["CodeAgent", "AnalystAgent"],
            system_message="""你是一个负责协调代码执行和数据分析流程的规划者。
你需要按照以下流程协调团队工作:

1. 首先分析用户的需求，确定需要执行的代码任务
2. 将具体的代码执行任务交给CodeAgent完成
3. 将数据分析和结果解释任务交给AnalystAgent完成
4. 最后总结整个流程，确认完成后输出TERMINATE以结束任务

请确保每次只将任务交给一个代理，并等待其完成后再进行下一步。
当所有任务完成后，请输出TERMINATE。""",
        )

        # 2. 创建代码代理 - 专门负责代码执行
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
            system_message="""你是一个专业的代码执行代理，负责在E2B沙盒中执行Python代码。
你有以下工具可用:
1. run_code(code) - 在沙盒中执行Python代码
2. install_package(package_name) - 安装Python包
3. list_files(path="/") - 列出目录中的文件
4. read_file(file_path) - 读取文件内容
5. write_file(file_path, content) - 写入文件
6. generate_chart(data_file, chart_type="bar") - 生成数据可视化图表

当收到代码执行任务时:
1. 如果需要安装包，使用install_package工具
2. 使用write_file工具创建必要的文件
3. 使用run_code工具执行代码
4. 使用list_files和read_file检查结果
5. 如果需要数据可视化，使用generate_chart工具

执行完任务后:
1. 整理执行结果和文件状态
2. 将完整的执行过程和结果交回给Planner

你应始终遵循以下原则:
- 为代码添加详细注释，确保可读性
- 合理拆分复杂任务为多个步骤
- 始终检查执行结果并报告任何错误
- 在返回前整理和总结执行过程""",
        )

        # 3. 创建分析师代理 - 专门负责数据分析
        analyst_agent = AssistantAgent(
            name="AnalystAgent",
            model_client=model_client,
            # 分析师代理只能将任务交回给规划者
            handoffs=["Planner"],
            tools=[read_file],  # 分析师只需要读取文件的工具
            system_message="""你是一位数据分析专家，擅长解释代码执行结果和分析数据。
你可以使用read_file工具查看数据文件和结果文件。

当你收到数据分析任务时:
1. 仔细研究代码执行结果和生成的数据
2. 提供专业的数据解读和见解
3. 指出数据中的关键趋势、模式或异常
4. 若有图表，解释图表呈现的信息
5. 提供进一步分析的建议

你的分析应该:
- 专业、深入且客观
- 使用适当的统计术语
- 避免过度解读数据
- 指出数据或方法的局限性
- 在适当的地方提供改进建议

完成分析后，将你的见解交回给Planner。""",
        )

        # 设置多种终止条件
        # 1. 当Planner输出TERMINATE时终止
        text_termination = TextMentionTermination("TERMINATE")

        # 2. 最大消息数量限制(防止无限对话)
        max_msg_termination = MaxMessageTermination(max_messages=30)

        # 3. 对话超时限制(单位：秒)
        timeout_termination = TimeoutTermination(timeout_seconds=600)  # 10分钟超时

        # 组合终止条件：满足任一条件即终止
        combined_termination = (
            text_termination | max_msg_termination | timeout_termination
        )

        # 创建Swarm团队
        team = Swarm(
            participants=[planner, code_agent, analyst_agent],
            termination_condition=combined_termination,
        )

        # 示例任务
        request = """请帮我执行以下数据分析任务:
1. 生成一个包含100个随机数据点的数据集
2. 计算基本统计信息(均值、标准差、最大值、最小值等)
3. 绘制数据分布的直方图
4. 检测数据中的异常值并分析它们的影响
"""

        # 运行团队
        print(f"\n🚀 启动多代理协作团队，执行任务: {request}\n")

        # 打印终止条件信息
        print("📝 终止条件设置:")
        print('  - Planner输出 "TERMINATE"')
        print("  - 最大消息数: 30条")
        print("  - 超时时间: 600秒")

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

        # 关闭沙盒会话
        session = await CodeSession.get_instance()
        await session.close()

    except Exception as e:
        print(f"发生错误: {e}")
        traceback.print_exc()  # 打印完整的错误堆栈，方便调试

        # 确保关闭沙盒会话
        try:
            session = await CodeSession.get_instance()
            await session.close()
        except Exception as e:
            print(f"关闭沙盒会话时出错: {e}")


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())
