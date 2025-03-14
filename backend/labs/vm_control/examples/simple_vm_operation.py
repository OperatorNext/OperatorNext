"""
简单的VM操作示例

这个示例展示了如何使用VM控制模块进行基本操作：
1. 连接到VM
2. 获取屏幕截图
3. 移动鼠标和点击
4. 输入文本
5. 运行命令
"""

import asyncio
import os
import tempfile

# 导入dotenv以加载环境变量
from dotenv import load_dotenv

# 导入VM控制模块
from labs.vm_control import create_vm_client, get_vnc_password, get_vnc_url


async def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()

    # 打印VM连接信息
    print(f"连接到VM: {get_vnc_url()}")
    print(f"使用密码: {'*' * len(get_vnc_password()) if get_vnc_password() else '无'}")

    # 创建VM客户端
    print("初始化VM客户端...")
    client = await create_vm_client()

    try:
        # 获取屏幕截图
        print("获取屏幕截图...")
        screenshot_path = os.path.join(tempfile.gettempdir(), "vm_screenshot.png")
        await client.get_screenshot(screenshot_path)
        print(f"截图已保存到: {screenshot_path}")

        # 打开终端
        print("打开终端...")
        await client.run_xdotool("key ctrl+alt+t")
        # 等待终端打开
        await asyncio.sleep(1)

        # 输入文本
        print("输入命令...")
        await client.type_text("echo 'Hello from VM Control!' && date")
        await client.press_key("Return")
        # 等待命令执行
        await asyncio.sleep(1)

        # 获取命令输出的截图
        print("获取命令输出的截图...")
        output_screenshot = os.path.join(tempfile.gettempdir(), "vm_command_output.png")
        await client.get_screenshot(output_screenshot)
        print(f"命令输出截图已保存到: {output_screenshot}")

        # 通过Docker执行命令
        print("直接在VM中执行命令...")
        output = await client.execute_command("ls -la /home/ubuntu")
        print("命令输出:")
        print(output)

        # 关闭终端
        print("关闭终端...")
        await client.run_xdotool("key alt+F4")
        await asyncio.sleep(1)

        print("演示完成！")

    finally:
        # 关闭客户端连接
        await client.close()


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
