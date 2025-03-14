"""
VM 浏览器自动化示例

这个示例展示了如何使用VM控制模块进行浏览器自动化操作：
1. 打开Firefox浏览器
2. 导航到指定网站
3. 截取网页截图
4. 模拟用户搜索行为
5. 获取搜索结果
"""

import asyncio
import os
import tempfile

# 导入dotenv以加载环境变量
from dotenv import load_dotenv

# 导入VM控制模块
from labs.vm_control import create_vm_client


async def open_firefox(client):
    """打开Firefox浏览器

    Args:
        client: VM客户端
    """
    print("打开Firefox浏览器...")
    # 方法1: 使用xdotool打开Firefox
    await client.execute_command("DISPLAY=:1 firefox -private-window &")

    # 等待浏览器启动
    await asyncio.sleep(5)

    # 将浏览器窗口最大化
    await client.run_xdotool(
        "search --onlyvisible --class Firefox windowactivate key F11"
    )

    # 再等待一会，确保浏览器完全加载
    await asyncio.sleep(2)


async def navigate_to_url(client, url):
    """导航到指定URL

    Args:
        client: VM客户端
        url: 要访问的URL
    """
    print(f"导航到 {url}...")

    # 点击地址栏
    await client.run_xdotool(
        "search --onlyvisible --class Firefox windowactivate key ctrl+l"
    )
    await asyncio.sleep(1)

    # 清除地址栏内容
    await client.run_xdotool("key ctrl+a")
    await asyncio.sleep(0.5)

    # 输入URL
    await client.type_text(url)
    await asyncio.sleep(0.5)

    # 按回车
    await client.press_key("Return")

    # 等待页面加载
    print("等待页面加载...")
    await asyncio.sleep(5)


async def search_on_page(client, search_term):
    """在页面上进行搜索

    Args:
        client: VM客户端
        search_term: 搜索关键词
    """
    print(f"搜索 '{search_term}'...")

    # 激活页面
    await client.run_xdotool("search --onlyvisible --class Firefox windowactivate")

    # 按Ctrl+F打开搜索框
    await client.run_xdotool("key ctrl+f")
    await asyncio.sleep(1)

    # 输入搜索关键词
    await client.type_text(search_term)
    await asyncio.sleep(1)

    # 按回车开始搜索
    await client.press_key("Return")
    await asyncio.sleep(1)


async def close_firefox(client):
    """关闭Firefox浏览器

    Args:
        client: VM客户端
    """
    print("关闭Firefox浏览器...")

    # 激活Firefox窗口
    await client.run_xdotool("search --onlyvisible --class Firefox windowactivate")

    # 按Alt+F4关闭窗口
    await client.run_xdotool("key alt+F4")
    await asyncio.sleep(1)


async def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()

    # 创建VM客户端
    print("初始化VM客户端...")
    client = await create_vm_client()

    try:
        # 打开Firefox浏览器
        await open_firefox(client)

        # 导航到示例网站
        await navigate_to_url(client, "https://www.example.com")

        # 获取网页截图
        print("获取网页截图...")
        screenshot_path = os.path.join(tempfile.gettempdir(), "vm_webpage.png")
        await client.get_screenshot(screenshot_path)
        print(f"网页截图已保存到: {screenshot_path}")

        # 在页面上搜索文本
        await search_on_page(client, "Example Domain")

        # 获取搜索结果截图
        print("获取搜索结果截图...")
        search_screenshot = os.path.join(tempfile.gettempdir(), "vm_search_result.png")
        await client.get_screenshot(search_screenshot)
        print(f"搜索结果截图已保存到: {search_screenshot}")

        # 访问另一个网站
        await navigate_to_url(client, "https://news.ycombinator.com")

        # 获取第二个网页截图
        print("获取第二个网页截图...")
        screenshot2_path = os.path.join(tempfile.gettempdir(), "vm_webpage2.png")
        await client.get_screenshot(screenshot2_path)
        print(f"第二个网页截图已保存到: {screenshot2_path}")

        # 关闭Firefox浏览器
        await close_firefox(client)

        print("演示完成！")

    finally:
        # 确保关闭客户端连接
        await client.close()


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
