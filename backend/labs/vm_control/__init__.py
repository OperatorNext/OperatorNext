"""
VM 控制模块

提供对虚拟机的控制和交互功能，包括：
1. 连接到虚拟机
2. 执行鼠标和键盘操作
3. 获取屏幕截图
4. 运行自动化任务
"""

from .config import get_vnc_password, get_vnc_url
from .utils import VMClient, create_vm_client

__all__ = [
    "VMClient",
    "create_vm_client",
    "get_vnc_url",
    "get_vnc_password",
]
