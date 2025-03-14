"""
工具函数模块

提供各种辅助功能。
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from .config import (
    check_selenium_status,
    get_selenium_url,
    get_vnc_url,
    print_status_info,
)


async def check_status() -> bool:
    """检查 Selenium Grid 服务状态

    Returns:
        服务是否正常运行
    """
    success, status = check_selenium_status()
    if success:
        print_status_info(status)
        print(f"Selenium Grid 地址: {get_selenium_url()}")
        print(f"VNC 可视化界面: {get_vnc_url()}")
        return True
    return False


def save_cookies_to_file(cookies: list[dict[str, Any]], file_path: str) -> bool:
    """将 Cookie 保存到文件

    Args:
        cookies: Cookie 列表
        file_path: 文件路径

    Returns:
        是否成功保存
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存 Cookie 失败: {e}")
        return False


def load_cookies_from_file(file_path: str) -> list[dict[str, Any]]:
    """从文件加载 Cookie

    Args:
        file_path: 文件路径

    Returns:
        Cookie 列表
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载 Cookie 失败: {e}")
        return []


def ensure_dir_exists(path: str) -> bool:
    """确保目录存在

    Args:
        path: 目录路径

    Returns:
        是否成功创建或已存在
    """
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False


async def wait_for_service_ready(timeout: int = 60) -> bool:
    """等待 Selenium Grid 服务就绪

    Args:
        timeout: 超时时间（秒）

    Returns:
        服务是否就绪
    """
    start_time = asyncio.get_event_loop().time()
    while (asyncio.get_event_loop().time() - start_time) < timeout:
        success, _ = check_selenium_status()
        if success:
            print("Selenium Grid 服务已就绪")
            return True
        print("等待 Selenium Grid 服务就绪...")
        await asyncio.sleep(2)

    print(f"等待 Selenium Grid 服务超时（{timeout}秒）")
    return False
