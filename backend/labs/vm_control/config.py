"""
VM 控制模块配置

提供VM控制模块的配置参数和辅助函数。
"""

import os
from urllib.parse import urlparse

# 默认VNC连接信息
DEFAULT_VNC_HOST = "localhost"
DEFAULT_VNC_PORT = 15900
DEFAULT_VNC_PASSWORD = "vncpassword"


# 从环境变量获取VNC连接URL
def get_vnc_url():
    """获取VNC服务器URL

    格式: "host:port"

    Returns:
        str: VNC服务器URL
    """
    # 优先使用环境变量中的配置
    env_url = os.getenv("VM_VNC_URL")

    if env_url:
        # 如果环境变量包含完整URL，解析主机和端口
        if "://" in env_url:
            parsed = urlparse(env_url)
            host = parsed.hostname or DEFAULT_VNC_HOST
            port = parsed.port or DEFAULT_VNC_PORT
        else:
            # 否则假定格式为 "host:port"
            parts = env_url.split(":")
            host = parts[0] if parts[0] else DEFAULT_VNC_HOST
            port = int(parts[1]) if len(parts) > 1 and parts[1] else DEFAULT_VNC_PORT
    else:
        # 使用默认配置
        host = DEFAULT_VNC_HOST
        port = DEFAULT_VNC_PORT

    return f"{host}:{port}"


# 从环境变量获取VNC密码
def get_vnc_password():
    """获取VNC服务器密码

    Returns:
        str: VNC服务器密码
    """
    return os.getenv("VM_VNC_PASSWORD", DEFAULT_VNC_PASSWORD)


# 检查VM服务状态
def check_vm_status():
    """检查VM服务状态

    Returns:
        tuple: (成功状态, 错误信息)
    """
    import socket

    host, port_str = get_vnc_url().split(":")
    port = int(port_str)

    try:
        # 尝试连接到VNC服务器
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((host, port))
        return True, None
    except Exception as e:
        return False, str(e)
