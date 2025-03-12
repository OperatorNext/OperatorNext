"""
简单的 agent 示例

这个示例展示了如何：
1. 使用环境变量配置创建 OpenAI 模型客户端
2. 创建一个带有简单工具的助手 agent
3. 运行对话并处理结果
"""

import asyncio
import os
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv


# 加载环境变量
def load_env():
    """加载环境变量配置"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent.parent.parent
    env_path = project_root / "backend" / ".env"
    
    if not env_path.exists():
        raise FileNotFoundError(f"找不到环境变量文件: {env_path}")
    
    # 加载环境变量
    load_dotenv(env_path)
    
    # 验证必要的环境变量
    required_vars = ["OPENAI_API_KEY", "OPENAI_API_BASE", "OPENAI_MODEL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"缺少必要的环境变量: {', '.join(missing_vars)}")


async def get_weather(city: str, date: str | None = None) -> str:
    """
    获取城市天气信息的示例工具

    Args:
        city: 城市名称
        date: 可选的日期，默认为今天

    Returns:
        str: 天气信息
    """
    # 这里只是一个模拟的返回值
    return f"{city} 今天天气晴朗，温度 25°C，适合外出活动。"


async def create_weather_assistant() -> AssistantAgent:
    """创建天气助手 agent"""
    # 创建 OpenAI 模型客户端
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        base_url=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # 创建助手 agent
    return AssistantAgent(
        name="weather_assistant",  # 使用英文名称
        model_client=model_client,
        tools=[get_weather],
        system_message="你是一个专业的天气助手，可以查询各个城市的天气信息。请用中文回复。",
        model_client_stream=True,  # 启用流式输出
    )


async def main():
    """主函数：运行示例对话"""
    try:
        # 加载环境变量
        load_env()
        
        # 创建助手
        assistant = await create_weather_assistant()

        print("开始与天气助手对话...")
        print("-" * 50)

        # 运行对话并实时显示结果
        await Console(
            assistant.on_messages_stream(
                [TextMessage(content="请告诉我北京的天气如何？", source="user")],
                cancellation_token=CancellationToken(),
            ),
            output_stats=True,  # 显示统计信息
        )

        print("-" * 50)
        
        # 再问一个问题
        await Console(
            assistant.on_messages_stream(
                [TextMessage(content="上海呢？", source="user")],
                cancellation_token=CancellationToken(),
            ),
            output_stats=True,
        )
    
    except FileNotFoundError as e:
        print(f"错误: {e}")
    except ValueError as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")
        raise  # 在开发时显示完整错误堆栈


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main()) 