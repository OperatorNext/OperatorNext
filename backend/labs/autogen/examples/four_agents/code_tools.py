"""
代码执行工具函数

提供E2B沙盒代码执行和文件操作相关的工具函数，包括代码运行、包安装、文件操作和数据可视化等。
"""

import os
import sys

# 添加项目根目录到 Python 路径
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
    )
)

from backend.labs.e2b.utils import generate_data_visualization_code

from .sessions import CodeSession


async def run_code(code: str) -> str:
    """
    在E2B沙盒中运行代码并返回结果

    Args:
        code: 要执行的Python代码

    Returns:
        str: 执行结果
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 执行代码
        print("🧪 执行代码...")
        result = await session.executor.run_code(code)

        # 更新文件列表
        try:
            session.current_files = await session.executor.list_files("/")
        except Exception as e:
            print(f"警告: 无法更新文件列表: {str(e)}")

        # 格式化输出
        if result["success"]:
            output = "✅ 代码执行成功:\n\n"

            if result["logs"] and result["logs"].stdout:
                output += (
                    "输出:\n```\n" + "\n".join(result["logs"].stdout) + "\n```\n\n"
                )

            if result["logs"] and result["logs"].stderr:
                output += (
                    "警告/错误:\n```\n" + "\n".join(result["logs"].stderr) + "\n```\n\n"
                )

            output += "当前沙盒中的文件:\n"
            file_list = [f"- {f['name']}" for f in session.current_files]
            output += "\n".join(file_list) if file_list else "- (无文件)"

            return output
        else:
            return f"❌ 代码执行失败:\n\n```\n{result['error']}\n```"

    except Exception as e:
        return f"❌ 运行代码时出错: {str(e)}"


async def install_package(package_name: str) -> str:
    """
    在E2B沙盒中安装Python包

    Args:
        package_name: 要安装的包名称

    Returns:
        str: 安装结果
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 检查包是否已安装
        if package_name in session.installed_packages:
            return f"📦 {package_name} 已经安装"

        # 安装包
        print(f"📦 安装包: {package_name}")
        result = await session.executor.install_package(package_name)

        # 如果安装成功，添加到已安装包集合
        if result["success"]:
            session.installed_packages.add(package_name)

        # 格式化输出
        if result["success"]:
            output = f"✅ 成功安装包: {package_name}\n\n"

            if result["logs"] and result["logs"].stdout:
                output += "安装日志摘要:\n```\n"
                log_lines = "\n".join(result["logs"].stdout)
                # 如果日志太长，只显示前后一部分
                if len(log_lines) > 1000:
                    output += log_lines[:500] + "\n...\n" + log_lines[-500:]
                else:
                    output += log_lines
                output += "\n```"

            return output
        else:
            return f"❌ 安装包失败: {package_name}\n\n```\n{result['error']}\n```"

    except Exception as e:
        return f"❌ 安装包时出错: {str(e)}"


async def list_files(path: str = "/") -> str:
    """
    列出E2B沙盒中的文件

    Args:
        path: 要列出文件的目录路径

    Returns:
        str: 文件列表
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 列出文件
        print(f"📂 列出目录: {path}")
        files = await session.executor.list_files(path)

        # 保存到会话状态
        if path == "/":
            session.current_files = files

        # 格式化输出
        if not files:
            return f"目录 {path} 中没有文件"

        output = f"📂 目录 {path} 中的文件:\n\n"

        # 分别处理目录和文件
        directories = [f for f in files if f["is_dir"]]
        regular_files = [f for f in files if not f["is_dir"]]

        if directories:
            output += "目录:\n"
            for d in directories:
                output += f"- 📁 {d['name']}\n"
            output += "\n"

        if regular_files:
            output += "文件:\n"
            for f in regular_files:
                size_str = f" ({f['size']} 字节)" if f["size"] is not None else ""
                output += f"- 📄 {f['name']}{size_str}\n"

        return output

    except Exception as e:
        return f"❌ 列出文件时出错: {str(e)}"


async def read_file(file_path: str) -> str:
    """
    读取E2B沙盒中的文件内容

    Args:
        file_path: 文件路径

    Returns:
        str: 文件内容
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 读取文件
        print(f"📖 读取文件: {file_path}")
        content = await session.executor.read_file(file_path)

        # 检测文件类型并适当处理
        if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            return f"图像文件 {file_path} 的二进制数据不显示，大小: {len(content)} 字节"

        elif file_path.lower().endswith(
            (".pdf", ".zip", ".gz", ".tar", ".exe", ".bin")
        ):
            return f"二进制文件 {file_path} 的数据不显示，大小: {len(content)} 字节"

        else:
            # 尝试解码为文本
            try:
                text_content = content.decode("utf-8")
                # 如果文件过大，只显示部分内容
                if len(text_content) > 5000:
                    return f"📄 文件 {file_path} 内容 (前5000字符):\n\n```\n{text_content[:5000]}\n...(还有 {len(text_content) - 5000} 字符未显示)...\n```"
                else:
                    return f"📄 文件 {file_path} 内容:\n\n```\n{text_content}\n```"
            except UnicodeDecodeError:
                return (
                    f"二进制文件 {file_path} 无法解码为文本，大小: {len(content)} 字节"
                )

    except Exception as e:
        return f"❌ 读取文件时出错: {str(e)}"


async def write_file(file_path: str, content: str) -> str:
    """
    写入文件到E2B沙盒

    Args:
        file_path: 文件路径
        content: 文件内容

    Returns:
        str: 操作结果
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 写入文件
        print(f"✏️ 写入文件: {file_path}")
        result = await session.executor.write_file(file_path, content)

        # 更新文件列表
        try:
            session.current_files = await session.executor.list_files("/")
        except Exception as e:
            print(f"警告: 无法更新文件列表: {str(e)}")

        # 格式化输出
        if result["success"]:
            return f"✅ 文件已成功写入: {file_path}"
        else:
            return f"❌ 写入文件失败: {result['message']}"

    except Exception as e:
        return f"❌ 写入文件时出错: {str(e)}"


async def generate_chart(data_file: str, chart_type: str = "bar") -> str:
    """
    根据数据文件生成图表

    Args:
        data_file: 数据文件路径
        chart_type: 图表类型，支持 'bar', 'line', 'scatter', 'pie'

    Returns:
        str: 操作结果
    """
    # 获取会话实例
    session = await CodeSession.get_instance()

    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"

        # 检查文件是否存在
        print(f"📊 生成{chart_type}图表，数据文件: {data_file}")

        # 获取可视化代码
        viz_code = generate_data_visualization_code(data_file, chart_type)

        # 执行代码生成图表
        result = await session.executor.run_code(viz_code)

        # 更新文件列表
        session.current_files = await session.executor.list_files("/")

        # 格式化输出
        if result["success"]:
            chart_file = "/chart.png"

            # 检查图表文件是否生成
            if any(f["path"] == chart_file for f in session.current_files):
                return f"✅ 图表生成成功: {chart_file}\n\n图表类型: {chart_type}\n数据源: {data_file}"
            else:
                return f"⚠️ 代码执行成功，但未找到图表文件。日志输出:\n\n```\n{result['logs'].stdout if result['logs'] and result['logs'].stdout else '无输出'}\n```"
        else:
            return f"❌ 生成图表失败:\n\n```\n{result['error']}\n```"

    except Exception as e:
        return f"❌ 生成图表时出错: {str(e)}"
