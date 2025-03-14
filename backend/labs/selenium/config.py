"""
Selenium 配置管理模块

提供统一的配置加载和管理功能，包括：
1. 环境变量加载
2. 服务配置信息获取
3. 通用连接参数
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


# 常用配置参数
def get_selenium_url():
    """获取 Selenium Grid 服务 URL"""
    return os.getenv("SELENIUM_URL", "http://localhost:4444")


def get_selenium_browser():
    """获取默认浏览器类型"""
    return os.getenv("SELENIUM_BROWSER", "chrome").lower()


def get_remote_url():
    """获取 RemoteWebDriver 连接 URL"""
    base_url = get_selenium_url()
    # 确保路径以 / 结尾
    if not base_url.endswith("/"):
        base_url += "/"
    return f"{base_url}wd/hub"


def get_vnc_url(browser=None):
    """获取 VNC 可视化 URL"""
    if browser is None:
        browser = get_selenium_browser()

    port_map = {
        "chrome": "7900",
        "chromium": "7900",  # Chromium使用与Chrome相同的端口
        "firefox": "7901",
        "edge": "7902",
    }
    port = port_map.get(browser.lower(), "7900")

    return f"http://localhost:{port}/?autoconnect=1&resize=scale&password=secret"


# 服务状态检查
def check_selenium_status():
    """检查 Selenium Grid 服务状态"""
    import requests

    try:
        response = requests.get(f"{get_selenium_url()}/status")

        if response.status_code != 200:
            print(
                f"错误: Selenium Grid 服务未启动或不健康 (状态码: {response.status_code})"
            )
            print(f"响应内容: {response.text}")
            print("请先运行: docker-compose up -d selenium-hub selenium-chrome")
            return False, None

        # 解析状态
        status = response.json()
        return True, status

    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到 Selenium Grid 服务")
        print("请先运行: docker-compose up -d selenium-hub selenium-chrome")
        return False, None


# 打印服务状态信息
def print_status_info(status):
    """打印服务状态信息"""
    if status and isinstance(status, dict):
        nodes = status.get("value", {}).get("nodes", [])
        print("Selenium Grid 状态: 运行中")
        print(f"可用节点数: {len(nodes)}")

        for node in nodes:
            slots = node.get("slots", [])
            available = sum(1 for slot in slots if not slot.get("session"))
            total = len(slots)
            print(f"节点 {node.get('id')}: {available}/{total} 可用")
