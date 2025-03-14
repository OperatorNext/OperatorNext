"""
Selenium Grid 持续演示脚本

打开浏览器并持续运行，执行各种可视化操作，便于通过VNC观察浏览器活动。
按Ctrl+C可以终止脚本运行。
"""

import asyncio
import os
import random
import signal
import sys
from datetime import datetime

# 添加父目录到模块搜索路径，以便导入 labs.selenium
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from labs.selenium.factory import create_browser_controller

# 全局变量用于控制程序运行
running = True
browser_type = "chromium"  # 默认使用chromium，可以通过命令行参数更改为firefox


def signal_handler(sig, frame):
    """处理Ctrl+C信号，优雅地终止程序"""
    global running
    print("\n🛑 检测到中断信号，正在优雅终止...")
    running = False


async def visit_website(controller, url, duration=5):
    """访问网站并执行一些操作"""
    print(f"🌐 正在访问: {url}")
    await controller.navigate(url)

    # 获取标题
    title = await controller.get_title()
    print(f"📄 页面标题: {title}")

    # 获取当前URL
    current_url = await controller.get_current_url()
    print(f"🔗 当前URL: {current_url}")

    # 随机滚动页面
    for _i in range(3):
        scroll_y = random.randint(100, 800)
        print(f"⬇️ 向下滚动 {scroll_y}px")
        await controller.scroll_to(0, scroll_y)
        await asyncio.sleep(1)

    # 停留指定时间
    print(f"⏱️ 停留{duration}秒...")
    for _i in range(duration):
        if not running:
            break
        await asyncio.sleep(1)
        print(".", end="", flush=True)
    print()


async def run_continuous_demo():
    """持续运行演示"""
    global running

    # 注册信号处理程序（Ctrl+C）
    signal.signal(signal.SIGINT, signal_handler)

    print(f"🚀 启动持续演示 (浏览器: {browser_type})...")
    print("👁️ 你现在可以通过VNC观察浏览器活动")
    print("💡 按Ctrl+C可随时终止程序")

    try:
        # 创建浏览器控制器，明确设置不使用headless模式
        options = {
            "headless": False,  # 关键配置：关闭headless模式使浏览器可见
            "window_size": (1280, 800),  # 设置窗口大小
        }
        controller = await create_browser_controller(
            browser=browser_type, options=options
        )

        # 网站列表
        websites = [
            "https://www.example.com",
            "https://www.python.org",
            "https://www.selenium.dev",
            "https://news.ycombinator.com",
            "https://github.com",
        ]

        cycle = 1
        while running:
            print(f"\n==== 循环 #{cycle} - {datetime.now().strftime('%H:%M:%S')} ====")

            # 随机选择一个网站访问
            website = random.choice(websites)
            await visit_website(controller, website, duration=10)

            cycle += 1

            # 每完成5个循环，清除浏览器缓存
            if cycle % 5 == 0 and running:
                print("🧹 清除浏览器缓存...")
                await controller.execute_js("window.localStorage.clear();")
                await controller.execute_js("window.sessionStorage.clear();")
                cookies = await controller.execute_js("return document.cookie")
                print(f"🍪 当前cookies: {cookies}")
                await asyncio.sleep(2)

    except Exception as e:
        print(f"❌ 出错: {e}")
    finally:
        if "controller" in locals():
            print("👋 关闭浏览器...")
            await controller.close()
        print("✅ 程序已终止")


if __name__ == "__main__":
    # 解析命令行参数
    if len(sys.argv) > 1:
        browser_arg = sys.argv[1].lower()
        if browser_arg in ["chrome", "chromium", "firefox"]:
            browser_type = browser_arg
            print(f"使用浏览器: {browser_type}")

    # 运行演示
    asyncio.run(run_continuous_demo())
