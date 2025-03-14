"""
VM 控制工具

提供与VM交互的各种工具和辅助函数。
"""

import os
import tempfile

import vncdotool.api
from PIL import Image

import docker

from .config import get_vnc_password, get_vnc_url


class VMClient:
    """VM 客户端

    提供与VM交互的接口，包括执行鼠标和键盘操作以及获取屏幕截图。
    """

    def __init__(self):
        """初始化VM客户端"""
        self.vnc_url = get_vnc_url()
        self.vnc_password = get_vnc_password()
        self.client = None
        self.docker_client = None
        self.container = None

    async def connect(self) -> vncdotool.api.VNCDoToolClient:
        """连接到VM

        Returns:
            vncdotool.api.VNCDoToolClient: VNC客户端
        """
        if self.client is None:
            self.client = vncdotool.api.connect(f"vnc://{self.vnc_url}")

            # 尝试使用密码进行认证
            if self.vnc_password:
                await self.client.password(self.vnc_password)

        return self.client

    async def connect_docker(self) -> docker.models.containers.Container:
        """连接到VM的Docker容器

        Returns:
            docker.models.containers.Container: Docker容器
        """
        if self.docker_client is None:
            self.docker_client = docker.from_env()

        if self.container is None:
            try:
                self.container = self.docker_client.containers.get(
                    "operatornext-vmhost"
                )
            except docker.errors.NotFound:
                raise RuntimeError("VM容器 'operatornext-vmhost' 未运行")

        return self.container

    async def move_mouse(self, x: int, y: int) -> None:
        """移动鼠标到指定位置

        Args:
            x: 横坐标
            y: 纵坐标
        """
        client = await self.connect()
        await client.mouseMove(x, y)

    async def click(self, button: int = 1) -> None:
        """点击鼠标

        Args:
            button: 鼠标按钮 (1=左键, 2=中键, 3=右键)
        """
        client = await self.connect()
        await client.mousePress(button)

    async def double_click(self, button: int = 1) -> None:
        """双击鼠标

        Args:
            button: 鼠标按钮 (1=左键, 2=中键, 3=右键)
        """
        client = await self.connect()
        await client.mousePress(button)
        await client.mousePress(button)

    async def type_text(self, text: str) -> None:
        """输入文本

        Args:
            text: 要输入的文本
        """
        client = await self.connect()
        await client.type(text)

    async def press_key(self, key: str) -> None:
        """按下键盘按键

        Args:
            key: 要按下的按键名称
        """
        client = await self.connect()
        await client.keyPress(key)

    async def get_screenshot(self, save_path: str | None = None) -> str | Image.Image:
        """获取屏幕截图

        Args:
            save_path: 保存截图的路径，如果为None则返回PIL图像对象

        Returns:
            Union[str, Image.Image]: 图像路径或PIL图像对象
        """
        client = await self.connect()

        # 创建临时文件用于保存截图
        temp_path = None
        if save_path is None:
            temp_fd, temp_path = tempfile.mkstemp(suffix=".png")
            os.close(temp_fd)
            file_path = temp_path
        else:
            file_path = save_path

        # 捕获截图
        await client.captureScreen(file_path)

        # 如果没有提供保存路径，返回PIL图像对象
        if save_path is None:
            img = Image.open(temp_path)
            return img

        return file_path

    async def execute_command(self, command: str) -> str:
        """在VM容器中执行命令

        Args:
            command: 要执行的命令

        Returns:
            str: 命令输出
        """
        container = await self.connect_docker()
        result = container.exec_run(command)
        return result.output.decode("utf-8")

    async def run_xdotool(self, command: str) -> str:
        """运行xdotool命令

        Args:
            command: 要运行的xdotool命令

        Returns:
            str: 命令输出
        """
        full_command = f"DISPLAY=:1 xdotool {command}"
        return await self.execute_command(full_command)

    async def click_at(self, x: int, y: int, button: int = 1) -> None:
        """在指定位置点击

        Args:
            x: 横坐标
            y: 纵坐标
            button: 鼠标按钮 (1=左键, 2=中键, 3=右键)
        """
        await self.move_mouse(x, y)
        await self.click(button)

    async def close(self) -> None:
        """关闭连接"""
        if self.client:
            self.client.close()
            self.client = None

        if self.docker_client:
            self.docker_client.close()
            self.docker_client = None


async def create_vm_client() -> VMClient:
    """创建并初始化VM客户端

    Returns:
        VMClient: VM客户端
    """
    client = VMClient()
    await client.connect()
    return client
