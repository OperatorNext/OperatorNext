"""
Selenium Grid 测试脚本

测试 Selenium Grid 的基本功能，包括 Chromium 和 Firefox 浏览器
"""

import asyncio
import os
import sys

# 添加父目录到模块搜索路径，以便导入 labs.selenium
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from labs.selenium.factory import create_browser_controller


async def test_browser(browser_name):
    """测试浏览器基本功能"""
    print(f"\n=== 测试 {browser_name} 浏览器 ===")
    controller = await create_browser_controller(browser=browser_name)

    try:
        # 访问示例网站
        await controller.navigate("https://www.example.com/")

        # 获取标题
        title = await controller.get_title()
        print(f"页面标题: {title}")

        # 检查标题是否包含"Example"
        if "Example" in title:
            print("✅ 成功: 页面标题包含'Example'")
        else:
            print("❌ 失败: 页面标题不包含'Example'")

        # 获取当前URL
        url = await controller.get_current_url()
        print(f"当前URL: {url}")

        # 截取屏幕截图
        screenshot_path = f"/tmp/{browser_name}_test.png"
        await controller.save_screenshot(screenshot_path)
        print(f"截图已保存到 {screenshot_path}")

        return True
    except Exception as e:
        print(f"❌ 测试 {browser_name} 时出错: {e}")
        return False
    finally:
        await controller.close()


async def main():
    """主函数"""
    print("开始测试 Selenium Grid...")

    # 测试 Chromium
    chromium_result = await test_browser("chromium")

    # 测试 Firefox
    firefox_result = await test_browser("firefox")

    # 输出总结
    print("\n=== 测试结果 ===")
    print(f"Chromium: {'✅ 成功' if chromium_result else '❌ 失败'}")
    print(f"Firefox: {'✅ 成功' if firefox_result else '❌ 失败'}")


if __name__ == "__main__":
    asyncio.run(main())
