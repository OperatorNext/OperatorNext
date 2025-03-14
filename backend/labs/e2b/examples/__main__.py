#!/usr/bin/env python

"""
E2B示例包主入口

此文件允许将examples目录作为包运行:
python -m labs.e2b.examples

它会显示可用示例列表并提供运行说明。
"""

import os


def list_examples():
    """列出可用的示例"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    examples = []

    for file in os.listdir(current_dir):
        if file.endswith(".py") and file != "__main__.py" and not file.startswith("_"):
            example_name = os.path.splitext(file)[0]
            examples.append(example_name)

    return sorted(examples)


def show_help():
    """显示帮助信息"""
    examples = list_examples()

    print("E2B示例集")
    print("=" * 50)
    print("可用示例:")

    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example}")

    print("\n运行示例方法:")
    print("  python -m labs.e2b.examples.示例名称")
    print("例如:")
    print("  python -m labs.e2b.examples.code_team")
    print("\n提示: 请确保从项目根目录(backend)运行命令")


if __name__ == "__main__":
    show_help()
