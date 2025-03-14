#!/usr/bin/env python

"""
E2B代码团队示例启动脚本

这个脚本负责设置正确的Python路径环境，并运行code_team.py示例。
可以从任何位置调用此脚本，不会遇到模块导入错误。
"""

import asyncio
import os
import sys

# 将backend目录添加到Python路径
current_file_path = os.path.abspath(__file__)
examples_dir = os.path.dirname(current_file_path)
e2b_dir = os.path.dirname(examples_dir)
labs_dir = os.path.dirname(e2b_dir)
backend_dir = os.path.dirname(labs_dir)

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
    print(f"✅ 已添加项目根目录到Python路径: {backend_dir}")

# 导入并运行code_team.py中的main函数
try:
    from labs.e2b.examples.code_team import main

    print("🚀 启动E2B代码团队示例...")
    asyncio.run(main())

except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保已安装所有必要的依赖: pip install -r requirements.txt")

except Exception as e:
    print(f"❌ 运行时错误: {e}")
    import traceback

    traceback.print_exc()
