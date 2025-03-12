"""
AutoGen 智能体模块

这个模块实现了各种类型的智能体，包括：
- AI助手
- 用户代理
- 自定义智能体
"""

import autogen

from .config import ASSISTANT_CONFIG, USER_PROXY_CONFIG, get_config


def create_assistant(
    name: str | None = None,
    system_message: str | None = None,
    **kwargs
) -> autogen.AssistantAgent:
    """
    创建一个AI助手智能体

    Args:
        name: 助手名称
        system_message: 系统提示信息
        **kwargs: 其他配置参数

    Returns:
        autogen.AssistantAgent: 助手智能体实例
    """
    config = ASSISTANT_CONFIG.copy()
    if name:
        config["name"] = name
    if system_message:
        config["system_message"] = system_message
    config.update(kwargs)
    
    return autogen.AssistantAgent(**config)

def create_user_proxy(
    name: str | None = None,
    human_input_mode: str | None = None,
    **kwargs
) -> autogen.UserProxyAgent:
    """
    创建一个用户代理智能体

    Args:
        name: 代理名称
        human_input_mode: 人类输入模式
        **kwargs: 其他配置参数

    Returns:
        autogen.UserProxyAgent: 用户代理智能体实例
    """
    config = USER_PROXY_CONFIG.copy()
    if name:
        config["name"] = name
    if human_input_mode:
        config["human_input_mode"] = human_input_mode
    config.update(kwargs)
    
    return autogen.UserProxyAgent(**config)

def create_coding_assistant(
    name: str = "代码助手",
    system_message: str | None = None
) -> autogen.AssistantAgent:
    """
    创建一个专门用于编程的助手智能体

    Args:
        name: 助手名称
        system_message: 系统提示信息

    Returns:
        autogen.AssistantAgent: 编程助手智能体实例
    """
    default_message = """你是一个专业的编程助手，擅长：
    1. 编写清晰、简洁的代码
    2. 解决编程问题和调试
    3. 提供最佳实践建议
    4. 优化代码性能
    请用中文回复，并确保代码符合PEP 8规范。
    """
    
    return create_assistant(
        name=name,
        system_message=system_message or default_message,
        llm_config={
            **get_config("base"),
            "temperature": 0.5,  # 降低随机性，提高代码质量
        }
    )

def create_group_chat(
    agents: list,
    max_rounds: int = 10
) -> autogen.GroupChat:
    """
    创建一个群组聊天

    Args:
        agents: 智能体列表
        max_rounds: 最大对话轮数

    Returns:
        autogen.GroupChat: 群组聊天实例
    """
    return autogen.GroupChat(
        agents=agents,
        messages=[],
        max_rounds=max_rounds
    ) 