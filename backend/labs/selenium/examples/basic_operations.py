"""
基本操作示例

演示如何使用浏览器控制器进行基本操作。
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到系统路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from backend.labs.selenium.factory import create_browser_controller
from backend.labs.selenium.utils import check_status


async def basic_operations_demo():
    """基本操作示例"""
    # 检查服务状态
    if not await check_status():
        print("Selenium Grid 服务未启动，请先启动服务：")
        print("docker-compose up -d selenium-hub selenium-chrome")
        return

    print("开始演示基本操作...")

    # 创建浏览器控制器（默认使用 Chrome）
    controller = await create_browser_controller()

    try:
        # 打开网页
        print("打开网页...")
        await controller.navigate("https://www.example.com")

        # 获取页面标题
        title = await controller.get_title()
        print(f"页面标题: {title}")

        # 获取当前 URL
        url = await controller.get_current_url()
        print(f"当前 URL: {url}")

        # 查找元素
        print("查找元素...")
        h1 = await controller.find_element_by_css("h1")

        # 获取元素文本
        text = await controller.get_text(h1)
        print(f"H1 文本: {text}")

        # 查找链接
        links = await controller.find_elements_by_css("a")
        print(f"发现 {len(links)} 个链接")

        if links:
            # 点击第一个链接
            print("点击第一个链接...")
            await controller.click(links[0])

            # 等待导航完成
            await controller.wait_for_navigation()

            # 获取新页面标题
            new_title = await controller.get_title()
            print(f"新页面标题: {new_title}")

        # 执行 JavaScript
        print("执行 JavaScript...")
        user_agent = await controller.execute_js("return navigator.userAgent;")
        print(f"用户代理: {user_agent}")

        # 滚动页面
        print("滚动页面...")
        await controller.scroll_to(0, 100)

        # 截图
        print("保存截图...")
        screenshots_dir = Path(__file__).parent.parent / "screenshots"
        screenshots_dir.mkdir(exist_ok=True)
        screenshot_path = screenshots_dir / "example.png"

        await controller.save_screenshot(str(screenshot_path))
        print(f"截图已保存到: {screenshot_path}")

        # 获取 Cookie
        cookies = await controller.get_cookies()
        print(f"Cookie 数量: {len(cookies)}")

        print("基本操作演示完成！")

    finally:
        # 关闭浏览器
        await controller.close()


if __name__ == "__main__":
    asyncio.run(basic_operations_demo())
