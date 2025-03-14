"""
代码执行器模块

提供代码执行的抽象接口和具体实现，支持在安全的沙盒环境中执行Python代码。
"""

import asyncio
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import aiofiles
from e2b_code_interpreter import Execution, Sandbox

from .config import get_e2b_api_key, get_e2b_sandbox_id, get_e2b_sandbox_timeout


class CodeExecutor(ABC):
    """代码执行器抽象基类

    定义所有代码执行器必须实现的方法。
    """

    @abstractmethod
    async def connect(self) -> None:
        """连接到代码执行环境"""
        pass

    @abstractmethod
    async def close(self) -> None:
        """关闭代码执行环境连接"""
        pass

    @abstractmethod
    async def run_code(self, code: str) -> dict[str, Any]:
        """
        运行代码片段

        Args:
            code: 要执行的代码字符串

        Returns:
            执行结果，包含输出、错误等信息
        """
        pass

    @abstractmethod
    async def install_package(self, package_name: str) -> dict[str, Any]:
        """
        安装Python包

        Args:
            package_name: 要安装的包名称

        Returns:
            安装结果，包含输出、错误等信息
        """
        pass

    @abstractmethod
    async def list_files(self, path: str = "/") -> list[dict[str, Any]]:
        """
        列出指定目录中的文件

        Args:
            path: 文件目录路径，默认为根目录

        Returns:
            文件列表，包含文件名、大小等信息
        """
        pass

    @abstractmethod
    async def read_file(self, file_path: str) -> bytes:
        """
        读取文件内容

        Args:
            file_path: 文件路径

        Returns:
            文件内容的二进制数据
        """
        pass

    @abstractmethod
    async def write_file(self, file_path: str, content: str | bytes) -> dict[str, Any]:
        """
        写入文件到E2B沙盒

        Args:
            file_path: 文件路径
            content: 文件内容

        Returns:
            操作结果
        """
        pass

    @abstractmethod
    async def upload_file(
        self, local_path: str | Path, remote_path: str | None = None
    ) -> dict[str, Any]:
        """
        上传本地文件到E2B沙盒

        Args:
            local_path: 本地文件路径
            remote_path: 远程文件路径，如果为None则使用本地文件名

        Returns:
            操作结果
        """
        pass

    @abstractmethod
    async def download_file(
        self, remote_path: str, local_path: str | Path
    ) -> dict[str, Any]:
        """
        从E2B沙盒下载文件到本地

        Args:
            remote_path: 远程文件路径
            local_path: 本地保存路径

        Returns:
            操作结果
        """
        pass

    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()


class E2BExecutor(CodeExecutor):
    """E2B代码执行器实现

    使用E2B沙盒实现代码执行功能。
    """

    def __init__(
        self,
        api_key: str | None = None,
        sandbox_id: str | None = None,
        timeout: int | None = None,
    ):
        """
        初始化E2B代码执行器

        Args:
            api_key: E2B API密钥，如果为None则从环境变量读取
            sandbox_id: 沙盒ID，用于连接到已存在的沙盒，如果为None则创建新沙盒
            timeout: 沙盒超时时间（秒），如果为None则使用默认值
        """
        self.api_key = api_key or get_e2b_api_key()
        self.sandbox_id = sandbox_id or get_e2b_sandbox_id()
        self.timeout = timeout or get_e2b_sandbox_timeout()
        self.sandbox = None
        self._connected = False

    async def connect(self) -> None:
        """连接到E2B沙盒"""
        if self._connected:
            return

        os.environ["E2B_API_KEY"] = self.api_key
        self.sandbox = await asyncio.to_thread(
            Sandbox, sandbox_id=self.sandbox_id, timeout=self.timeout
        )
        self._connected = True
        # 注意：E2B的Sandbox对象可能没有id属性，使用我们自己设置的sandbox_id
        sandbox_id = getattr(self.sandbox, "id", self.sandbox_id) or "未知"
        print(f"✅ 已连接到E2B沙盒 (ID: {sandbox_id})")

    async def close(self) -> None:
        """关闭E2B沙盒连接"""
        if not self._connected or not self.sandbox:
            return

        try:
            # E2B的Sandbox对象可能不需要显式关闭
            # 但我们仍将内部状态设为未连接
            self._connected = False
            sandbox_id = getattr(self.sandbox, "id", self.sandbox_id) or "未知"
            print(f"✅ E2B沙盒已关闭 (ID: {sandbox_id})")
        except Exception as e:
            print(f"❌ 关闭E2B沙盒时出错: {str(e)}")

    async def run_code(self, code: str) -> dict[str, Any]:
        """
        在E2B沙盒中运行代码

        Args:
            code: 要执行的Python代码

        Returns:
            Dict包含执行结果
        """
        if not self._connected or not self.sandbox:
            await self.connect()

        try:
            # 执行代码
            execution: Execution = await asyncio.to_thread(self.sandbox.run_code, code)

            # 解析结果
            result = {
                "success": not bool(execution.error),
                "text": execution.text,
                "logs": execution.logs,
                "error": execution.error,
            }

            return result
        except Exception as exc:
            return {
                "success": False,
                "text": "",
                "logs": [],
                "error": str(exc),
            }

    async def install_package(self, package_name: str) -> dict[str, Any]:
        """
        在E2B沙盒中安装Python包

        Args:
            package_name: 要安装的包名称

        Returns:
            Dict包含安装结果
        """
        if not self._connected or not self.sandbox:
            await self.connect()

        pip_command = f"pip install {package_name} -U"
        code = f"""
import subprocess
import sys

try:
    subprocess_result = subprocess.run(
        "{pip_command}",
        shell=True,
        check=True,
        capture_output=True,
        text=True
    )
    print(f"安装成功: {{subprocess_result.stdout}}")
    # 确认已安装
    import importlib
    package_name = "{package_name}".split("[")[0].split("==")[0].strip()
    importlib.import_module(package_name)
    print(f"已成功导入 {{package_name}}")
except subprocess.CalledProcessError as install_error:
    print(f"安装失败: {{install_error.stderr}}")
    sys.exit(1)
except ImportError as import_error:
    print(f"导入失败: {{str(import_error)}}")
    sys.exit(1)
"""
        return await self.run_code(code)

    async def list_files(self, path: str = "/") -> list[dict[str, Any]]:
        """
        列出E2B沙盒中指定目录的文件

        Args:
            path: 目录路径

        Returns:
            文件列表
        """
        if not self._connected or not self.sandbox:
            await self.connect()

        try:
            # 使用E2B的文件列表API
            files = await asyncio.to_thread(self.sandbox.files.list, path)

            # 转换为统一格式
            result = []
            for file in files:
                # 适应E2B的EntryInfo对象结构
                file_info = {
                    "name": file.name,
                    "path": file.path,
                    "is_dir": file.type == "directory"
                    if hasattr(file, "type")
                    else False,
                    "size": file.size if hasattr(file, "size") else None,
                }
                result.append(file_info)

            return result
        except Exception as e:
            print(f"❌ 列出文件时出错: {str(e)}")
            return []

    async def read_file(self, file_path: str) -> bytes:
        """
        读取E2B沙盒中的文件内容

        Args:
            file_path: 文件路径

        Returns:
            文件内容
        """
        if not self._connected or not self.sandbox:
            await self.connect()

        try:
            # 获取文件内容
            content = await asyncio.to_thread(self.sandbox.files.read, file_path)

            # 确保返回bytes
            if isinstance(content, str):
                return content.encode("utf-8")
            return content
        except Exception as e:
            print(f"❌ 读取文件时出错: {str(e)}")
            return b""

    async def write_file(self, file_path: str, content: str | bytes) -> dict[str, Any]:
        """
        写入文件到E2B沙盒

        Args:
            file_path: 文件路径
            content: 文件内容

        Returns:
            操作结果
        """
        if not self._connected or not self.sandbox:
            await self.connect()

        try:
            # 确保内容是正确的类型
            if isinstance(content, str):
                content = content.encode("utf-8")

            # 写入文件 - 根据E2B API文档
            await asyncio.to_thread(self.sandbox.files.write, file_path, content)

            return {
                "success": True,
                "message": f"已成功写入文件: {file_path}",
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"写入文件失败: {str(e)}",
            }

    async def upload_file(
        self, local_path: str | Path, remote_path: str | None = None
    ) -> dict[str, Any]:
        """
        上传本地文件到E2B沙盒

        Args:
            local_path: 本地文件路径
            remote_path: 远程文件路径，如果为None则使用本地文件名

        Returns:
            操作结果
        """
        if not self._connected or not self.sandbox:
            await self.connect()

        try:
            # 标准化路径
            local_path = Path(local_path)

            # 如果未指定远程路径，使用本地文件名
            if remote_path is None:
                remote_path = f"/{local_path.name}"

            # 读取本地文件
            async with aiofiles.open(local_path, "rb") as f:
                content = await f.read()

            # 上传到沙盒 - 根据E2B API文档
            await asyncio.to_thread(self.sandbox.files.write, remote_path, content)

            return {
                "success": True,
                "message": f"已成功上传文件: {local_path} -> {remote_path}",
                "remote_path": remote_path,
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"上传文件失败: {str(e)}",
            }

    async def download_file(
        self, remote_path: str, local_path: str | Path
    ) -> dict[str, Any]:
        """
        从E2B沙盒下载文件到本地

        Args:
            remote_path: 远程文件路径
            local_path: 本地保存路径

        Returns:
            操作结果
        """
        if not self._connected or not self.sandbox:
            await self.connect()

        try:
            # 标准化路径
            local_path = Path(local_path)

            # 确保目标目录存在
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # 从沙盒获取文件内容
            content = await asyncio.to_thread(self.sandbox.files.read, remote_path)

            # 写入本地文件
            async with aiofiles.open(local_path, "wb") as f:
                await f.write(content)

            return {
                "success": True,
                "message": f"已成功下载文件: {remote_path} -> {local_path}",
                "local_path": str(local_path),
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"下载文件失败: {str(e)}",
            }


async def create_code_executor(executor_type: str = "e2b", **kwargs) -> CodeExecutor:
    """
    创建代码执行器实例

    工厂函数，根据类型创建适当的执行器实例。

    Args:
        executor_type: 执行器类型，目前支持 "e2b"
        **kwargs: 传递给执行器的其他参数

    Returns:
        代码执行器实例
    """
    if executor_type.lower() == "e2b":
        executor = E2BExecutor(**kwargs)
        await executor.connect()
        return executor
    else:
        raise ValueError(f"不支持的执行器类型: {executor_type}")
