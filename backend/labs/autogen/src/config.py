"""
AutoGen 配置模块

这个模块包含了 AutoGen 实验的配置设置，包括：
- 模型配置
- 对话参数
- 智能体设置
"""

import os
from typing import Any

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 基础配置
BASE_CONFIG: dict[str, Any] = {
    "model": "gpt-4o",  # 默认模型
    "temperature": 0.7,  # 温度参数
    "max_tokens": 2000,  # 最大token数
    "top_p": 0.9,  # 采样参数
}

# 助手配置
ASSISTANT_CONFIG: dict[str, Any] = {
    "name": "AI助手",
    "system_message": "你是一个有帮助的AI助手，专注于提供准确和有用的回答。",
    "human_input_mode": "NEVER",  # 不需要人类输入
    "llm_config": {
        **BASE_CONFIG,
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
}

# 用户代理配置
USER_PROXY_CONFIG: dict[str, Any] = {
    "name": "用户代理",
    "human_input_mode": "TERMINATE",  # 终止时需要人类输入
    "max_consecutive_auto_reply": 10,  # 最大连续自动回复次数
}

# 对话配置
CONVERSATION_CONFIG: dict[str, Any] = {
    "max_turns": 10,  # 最大对话轮数
    "code_execution": True,  # 允许代码执行
}


def get_config(config_type: str = "base") -> dict[str, Any]:
    """
    获取指定类型的配置

    Args:
        config_type: 配置类型，可选值：base, assistant, user_proxy, conversation

    Returns:
        Dict[str, Any]: 配置字典
    """
    config_map = {
        "base": BASE_CONFIG,
        "assistant": ASSISTANT_CONFIG,
        "user_proxy": USER_PROXY_CONFIG,
        "conversation": CONVERSATION_CONFIG,
    }
    return config_map.get(config_type, BASE_CONFIG)
