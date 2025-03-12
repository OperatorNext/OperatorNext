"""
Browserless 配置管理模块

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
def get_browserless_url():
    """获取 Browserless 服务 URL"""
    return os.getenv("BROWSERLESS_URL", "http://localhost:13000")


def get_browserless_token():
    """获取 Browserless 访问令牌"""
    # 尝试从 BROWSERLESS_TOKEN 获取，如果没有则从 TOKEN 获取
    token = os.getenv("BROWSERLESS_TOKEN") or os.getenv("TOKEN", "browser-token-2024")
    return token


def get_ws_endpoint():
    """获取 WebSocket 连接端点"""
    # 将 http:// 替换为 ws://
    ws_host = get_browserless_url().replace("http://", "ws://")
    # 确保路径以 / 结尾
    if not ws_host.endswith("/"):
        ws_host += "/"
    return f"{ws_host}?token={get_browserless_token()}"


def get_metrics_url():
    """获取性能指标 API 地址"""
    url = get_browserless_url()
    token = get_browserless_token()
    return f"{url}/metrics?token={token}"


# 服务状态检查
async def check_browserless_status():
    """检查 Browserless 服务状态"""
    import requests
    
    try:
        response = requests.get(get_metrics_url())
        
        if response.status_code != 200:
            print(
                f"错误: Browserless 服务未启动或不健康 (状态码: {response.status_code})"
            )
            print(f"响应内容: {response.text}")
            print("请先运行: docker-compose up -d chrome")
            return False, None

        # 解析性能指标
        metrics = response.json()
        return True, metrics
        
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到 Browserless 服务")
        print("请先运行: docker-compose up -d chrome")
        return False, None


# 打印服务状态信息
def print_status_info(metrics):
    """打印服务状态信息"""
    if metrics and len(metrics) > 0:
        latest = metrics[0]
        print(f"CPU 使用率: {latest.get('cpu', 0) * 100:.1f}%")
        print(f"内存使用率: {latest.get('memory', 0) * 100:.1f}%")
        print(f"活跃会话数: {latest.get('maxConcurrent', 0)}") 