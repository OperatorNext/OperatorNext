#!/usr/bin/env python

"""
E2B示例运行器

这个脚本可以列出并运行所有E2B示例。
它会自动处理Python路径，确保示例可以正确导入所需模块。

使用方法:
1. 不带参数运行显示可用示例列表:
   python run_e2b_examples.py

2. 指定示例名称来运行特定示例:
   python run_e2b_examples.py code_team
"""

import argparse
import asyncio
import importlib
import os


def list_examples():
    """列出可用的E2B示例"""
    examples_dir = os.path.join("labs", "e2b", "examples")
    examples = []

    # 确保目录存在
    if not os.path.exists(examples_dir):
        print(f"错误: 找不到示例目录 {examples_dir}")
        return []

    for file in os.listdir(examples_dir):
        if file.endswith(".py") and file != "__main__.py" and not file.startswith("_"):
            example_name = os.path.splitext(file)[0]
            examples.append(example_name)

    return sorted(examples)


def show_examples():
    """显示可用示例列表"""
    examples = list_examples()

    if not examples:
        print("未找到示例文件!")
        return

    print("💻 E2B 示例集")
    print("=" * 50)
    print("可用示例:")

    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example}")

    print("\n运行示例命令:")
    print("  python run_e2b_examples.py <示例名称>")
    print("例如:")
    print("  python run_e2b_examples.py code_team")


async def run_example(example_name):
    """运行指定的示例"""
    try:
        # 导入示例模块
        module_path = f"labs.e2b.examples.{example_name}"
        module = importlib.import_module(module_path)

        # 检查模块是否有main函数
        if hasattr(module, "main"):
            print(f"🚀 运行示例: {example_name}")
            await module.main()
        else:
            print(f"❌ 错误: 示例 {example_name} 没有main函数")

    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print(f"找不到示例: {example_name}")
        print("请检查示例名称是否正确")

    except Exception as e:
        print(f"❌ 运行时错误: {e}")
        import traceback

        traceback.print_exc()


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="E2B示例运行器")
    parser.add_argument("example", nargs="?", help="要运行的示例名称")
    args = parser.parse_args()

    # 如果没有指定示例，显示可用示例列表
    if not args.example:
        show_examples()
        return

    # 获取可用示例列表
    examples = list_examples()

    # 检查指定的示例是否存在
    if args.example not in examples:
        print(f"❌ 错误: 未找到示例 '{args.example}'")
        print("可用示例:")
        for example in examples:
            print(f"  - {example}")
        return

    # 运行指定的示例
    asyncio.run(run_example(args.example))


if __name__ == "__main__":
    main()
