"""
公共类型定义

这个模块定义了实验室中共用的类型
"""

from enum import Enum
from typing import Any, TypeVar

# 基础类型
JsonDict = dict[str, Any]
ConfigDict = dict[str, Any]

# 枚举类型
class ModelProvider(str, Enum):
    """模型提供商"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"
    LOCAL = "local"

class AgentRole(str, Enum):
    """智能体角色"""
    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"
    CUSTOM = "custom"

# 配置类型
class BaseConfig(TypeVar("BaseConfig")):
    """基础配置类型"""
    model: str
    temperature: float
    max_tokens: int
    top_p: float

class AgentConfig(BaseConfig):
    """智能体配置类型"""
    name: str
    role: AgentRole
    system_message: str | None = None

# 消息类型
class Message(TypeVar("Message")):
    """消息类型"""
    role: AgentRole
    content: str
    timestamp: float
    metadata: JsonDict | None = None

# 结果类型
class Result(TypeVar("Result")):
    """结果类型"""
    success: bool
    data: Any | None = None
    error: str | None = None
    metadata: JsonDict | None = None 