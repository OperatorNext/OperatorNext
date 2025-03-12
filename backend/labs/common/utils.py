"""
公共工具函数

这个模块提供了实验室中共用的工具函数
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Any

from .types import JsonDict, Result

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_json_file(file_path: str) -> JsonDict:
    """
    加载JSON文件

    Args:
        file_path: JSON文件路径

    Returns:
        JsonDict: JSON数据
    """
    try:
        with open(file_path, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载JSON文件失败: {e}")
        return {}

def save_json_file(data: JsonDict, file_path: str) -> bool:
    """
    保存JSON文件

    Args:
        data: 要保存的数据
        file_path: 保存路径

    Returns:
        bool: 是否保存成功
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"保存JSON文件失败: {e}")
        return False

def get_project_root() -> Path:
    """
    获取项目根目录

    Returns:
        Path: 项目根目录路径
    """
    return Path(__file__).parent.parent.parent

def create_result(
    success: bool,
    data: Any | None = None,
    error: str | None = None,
    **kwargs
) -> Result:
    """
    创建统一的结果对象

    Args:
        success: 是否成功
        data: 数据
        error: 错误信息
        **kwargs: 其他元数据

    Returns:
        Result: 结果对象
    """
    return Result(
        success=success,
        data=data,
        error=error,
        metadata=kwargs if kwargs else None
    )

def measure_time(func):
    """
    测量函数执行时间的装饰器

    Args:
        func: 要测量的函数

    Returns:
        包装后的函数
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} 执行时间: {end_time - start_time:.2f}秒")
        return result
    return wrapper

def ensure_dir(dir_path: str) -> bool:
    """
    确保目录存在，如果不存在则创建

    Args:
        dir_path: 目录路径

    Returns:
        bool: 是否成功
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"创建目录失败: {e}")
        return False

def get_env_or_default(key: str, default: Any = None) -> Any:
    """
    获取环境变量，如果不存在则返回默认值

    Args:
        key: 环境变量名
        default: 默认值

    Returns:
        环境变量值或默认值
    """
    return os.getenv(key, default) 