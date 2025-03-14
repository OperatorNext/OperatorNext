"""
E2B配置管理模块

提供统一的配置加载和管理功能，包括：
1. 环境变量加载
2. API密钥获取
3. 沙盒配置参数
"""

import os
from pathlib import Path

import dotenv


# 初始化配置
def load_config():
    """加载环境变量和配置"""
    # 从项目根目录加载 .env 文件
    project_root = Path(__file__).parent.parent.parent.parent
    env_path = project_root / "backend" / ".env"
    dotenv.load_dotenv(env_path)


# 提前加载配置
load_config()


# E2B API密钥
def get_e2b_api_key():
    """获取 E2B API 密钥"""
    return os.getenv("E2B_API_KEY", "e2b_78b7cc907859a3f76023207cf3e7aa981cb265e2")


# 沙盒配置参数
def get_e2b_sandbox_timeout():
    """获取沙盒超时时间（秒）"""
    timeout = os.getenv("E2B_SANDBOX_TIMEOUT", "300")
    return int(timeout)


def get_e2b_sandbox_id():
    """获取沙盒ID（如果需要连接到已存在的沙盒）"""
    return os.getenv("E2B_SANDBOX_ID", None)
