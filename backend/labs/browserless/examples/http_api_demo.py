"""
Browserless HTTP API 示例索引

选择演示不同类型的 Browserless HTTP API：
1. 基本内容 API (content, screenshot, pdf)
2. 高级功能 API (unblock, scrape, performance)
"""

import asyncio
import sys

from ..config import check_browserless_status, print_status_info


def print_banner():
    """显示欢迎横幅"""
    print("\n" + "=" * 70)
    print(" " * 20 + "Browserless HTTP API 演示程序")
    print("=" * 70)


def print_menu():
    """显示菜单选项"""
    print("\n请选择要演示的 API 类型:")
    print("1. 基本内容 API (content, screenshot, pdf)")
    print("2. 高级功能 API (unblock, scrape, performance)")
    print("3. 退出程序")
    return input("\n请输入选项 [1-3]: ").strip()


async def run_demo(demo_type):
    """运行选定的演示"""
    # 确保 Browserless 服务已启动
    success, metrics = await check_browserless_status()
    if not success:
        return

    print("Browserless 服务健康检查通过!")
    print_status_info(metrics)

    if demo_type == 1:
        # 导入并运行基本内容 API 演示
        try:
            from .content_demo import demo_basic_apis

            await demo_basic_apis()
        except ImportError as e:
            print(f"无法导入基本 API 演示模块: {e}")
            print("请确认 content_demo.py 文件存在并且没有语法错误")
    else:
        # 导入并运行高级功能 API 演示
        try:
            from .advanced_demo import demo_advanced_apis

            await demo_advanced_apis()
        except ImportError as e:
            print(f"无法导入高级 API 演示模块: {e}")
            print("请确认 advanced_demo.py 文件存在并且没有语法错误")


async def main():
    """主函数"""
    print_banner()

    while True:
        choice = print_menu()

        if choice == "1":
            print("\n开始运行基本内容 API 演示...")
            await run_demo(1)
        elif choice == "2":
            print("\n开始运行高级功能 API 演示...")
            await run_demo(2)
        elif choice == "3":
            print("\n感谢使用 Browserless HTTP API 演示程序！再见！")
            break
        else:
            print("\n无效的选择，请重新输入！")

        # 在每次演示后询问是否继续
        if choice in ["1", "2"]:
            input("\n按 Enter 键返回主菜单...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n程序被手动中断。感谢使用！")
        sys.exit(0)
