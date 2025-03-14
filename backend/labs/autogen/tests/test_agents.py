"""
智能体测试模块

测试智能体的创建和基本功能
"""

from unittest.mock import patch

import pytest

import autogen
from labs.autogen.src.agents import (
    create_assistant,
    create_coding_assistant,
    create_group_chat,
    create_user_proxy,
)
from labs.autogen.src.config import get_config


def test_create_assistant():
    """测试创建助手智能体"""
    name = "测试助手"
    message = "测试系统消息"

    assistant = create_assistant(name=name, system_message=message)

    assert isinstance(assistant, autogen.AssistantAgent)
    assert assistant.name == name
    assert assistant.system_message == message


def test_create_user_proxy():
    """测试创建用户代理"""
    name = "测试用户"
    mode = "TERMINATE"

    user = create_user_proxy(name=name, human_input_mode=mode)

    assert isinstance(user, autogen.UserProxyAgent)
    assert user.name == name
    assert user.human_input_mode == mode


def test_create_coding_assistant():
    """测试创建编程助手"""
    assistant = create_coding_assistant()

    assert isinstance(assistant, autogen.AssistantAgent)
    assert "编程助手" in assistant.name
    assert "编程" in assistant.system_message


def test_create_group_chat():
    """测试创建群组聊天"""
    agents = [create_assistant(), create_user_proxy()]
    max_rounds = 5

    chat = create_group_chat(agents, max_rounds)

    assert isinstance(chat, autogen.GroupChat)
    assert len(chat.agents) == len(agents)
    assert chat.max_rounds == max_rounds


@pytest.mark.asyncio
async def test_assistant_response():
    """测试助手响应"""
    assistant = create_assistant()
    message = "你好"

    # 模拟 LLM 响应
    with patch("autogen.AssistantAgent._process_received_message") as mock_process:
        mock_process.return_value = "你好！我是AI助手。"

        response = await assistant.generate_response(message)
        assert isinstance(response, str)
        assert len(response) > 0


def test_config_loading():
    """测试配置加载"""
    base_config = get_config("base")
    assistant_config = get_config("assistant")
    user_config = get_config("user_proxy")

    assert isinstance(base_config, dict)
    assert isinstance(assistant_config, dict)
    assert isinstance(user_config, dict)

    assert "model" in base_config
    assert "name" in assistant_config
    assert "human_input_mode" in user_config
