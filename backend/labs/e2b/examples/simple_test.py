#!/usr/bin/env python

"""
E2B沙盒简单测试

这个脚本提供了E2B沙盒的基本功能测试，包括代码执行、包安装、文件操作和数据可视化。
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent.parent
sys.path.insert(0, str(project_root))

# 导入E2B模块
try:
    from labs.e2b import create_code_executor
    from labs.e2b.utils import generate_data_visualization_code
except ImportError:
    print("尝试不同的导入路径...")
    try:
        from backend.labs.e2b import create_code_executor
        from backend.labs.e2b.utils import generate_data_visualization_code
    except ImportError:
        # 打印更多调试信息
        print(f"当前目录: {os.getcwd()}")
        print(f"项目根目录: {project_root}")
        print(f"Python路径: {sys.path}")
        raise


async def test_basic_operations():
    """测试基本操作"""
    print("\n===== 基本操作测试 =====")

    executor = await create_code_executor()
    try:
        # 测试简单代码执行
        print("\n>> 执行简单代码:")
        result = await executor.run_code("print('Hello, E2B!')")
        print(f"结果: {result}")

        # 测试复杂代码执行
        print("\n>> 执行复杂代码:")
        complex_code = """
import math
import random

def calculate_pi_monte_carlo(n=1000):
    inside_circle = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1:
            inside_circle += 1
    return 4 * inside_circle / n

estimated_pi = calculate_pi_monte_carlo(10000)
print(f"π的蒙特卡洛估计值: {estimated_pi}")
print(f"实际π值: {math.pi}")
print(f"误差: {abs(estimated_pi - math.pi)}")
"""
        result = await executor.run_code(complex_code)
        print(f"结果: {result}")

    finally:
        await executor.close()


async def test_package_installation():
    """测试包安装"""
    print("\n===== 包安装测试 =====")

    executor = await create_code_executor()
    try:
        # 安装pandas包
        print("\n>> 安装pandas包:")
        result = await executor.install_package("pandas")
        print(f"安装结果: {result}")

        # 测试使用pandas
        print("\n>> 测试pandas功能:")
        pandas_code = """
import pandas as pd

# 创建简单的DataFrame
data = {
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 40],
    '工资': [8000, 10000, 15000, 20000]
}
df = pd.DataFrame(data)

# 显示数据
print(df)

# 简单的数据分析
print("\\n基本统计信息:")
print(df.describe())

print("\\n按年龄分组的平均工资:")
print(df.groupby(pd.cut(df['年龄'], bins=[20, 30, 40])).mean())
"""
        result = await executor.run_code(pandas_code)
        print(f"结果: {result}")

    finally:
        await executor.close()


async def test_file_operations():
    """测试文件操作"""
    print("\n===== 文件操作测试 =====")

    executor = await create_code_executor()
    try:
        # 写入文件
        print("\n>> 写入文件:")
        result = await executor.write_file(
            "/test.txt", "这是一个测试文件\n包含多行内容\n你好，世界！"
        )
        print(f"写入结果: {result}")

        # 列出文件
        print("\n>> 列出根目录文件:")
        files = await executor.list_files("/")
        print(f"文件列表: {files}")

        # 读取文件
        print("\n>> 读取文件内容:")
        content = await executor.read_file("/test.txt")
        print(f"文件内容: {content.decode('utf-8')}")

        # 创建目录和多个文件
        print("\n>> 创建目录和多个文件:")
        mkdir_code = """
import os

# 创建目录
os.makedirs("/data", exist_ok=True)

# 创建多个文件
for i in range(3):
    with open(f"/data/file_{i}.txt", "w") as f:
        f.write(f"这是文件 {i} 的内容\\n")

print("已创建目录和文件")
"""
        result = await executor.run_code(mkdir_code)
        print(f"创建结果: {result}")

        # 列出目录内容
        print("\n>> 列出/data目录内容:")
        files = await executor.list_files("/data")
        print(f"文件列表: {files}")

    finally:
        await executor.close()


async def test_data_visualization():
    """测试数据可视化"""
    print("\n===== 数据可视化测试 =====")

    executor = await create_code_executor()
    try:
        # 生成测试数据
        print("\n>> 生成测试数据:")
        data_code = """
import pandas as pd
import numpy as np

# 设置随机种子
np.random.seed(42)

# 创建时间序列数据
dates = pd.date_range('20230101', periods=100)
df = pd.DataFrame({
    '温度': np.random.normal(25, 5, 100), 
    '湿度': np.random.normal(60, 10, 100),
    '风速': np.random.normal(15, 3, 100)
}, index=dates)

# 保存为CSV
df.to_csv('/weather_data.csv')
print('已生成天气数据并保存至 /weather_data.csv')

# 创建分类数据
categories = ['食品', '电子', '服装', '家居', '其他']
values = np.random.randint(1000, 5000, size=len(categories))
sales_df = pd.DataFrame({'类别': categories, '销售额': values})
sales_df.to_csv('/sales_data.csv', index=False)
print('已生成销售数据并保存至 /sales_data.csv')
"""
        result = await executor.run_code(data_code)
        print(f"数据生成结果: {result}")

        # 生成不同类型的图表
        for chart_type in ["bar", "line", "scatter", "pie"]:
            print(f"\n>> 生成{chart_type}图表:")
            # 为不同数据选择适当的图表
            data_file = (
                "/sales_data.csv"
                if chart_type in ["bar", "pie"]
                else "/weather_data.csv"
            )

            # 生成可视化代码
            viz_code = generate_data_visualization_code(data_file, chart_type)
            print(f"生成的代码: {viz_code[:200]}...")  # 只显示代码的前200个字符

            # 执行可视化代码
            result = await executor.run_code(viz_code)
            print(f"可视化执行结果: {result}")

            # 检查图表文件
            files = await executor.list_files("/")
            print(f"根目录文件: {[f['name'] for f in files]}")

            if "/chart.png" in [f["path"] for f in files]:
                print("图表已成功生成！")
            else:
                print("图表生成失败")

    finally:
        await executor.close()


async def main():
    """主函数"""
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python路径: {sys.path}")
    print("开始测试E2B沙盒功能...")

    # 测试基本操作
    await test_basic_operations()

    # 测试包安装
    await test_package_installation()

    # 测试文件操作
    await test_file_operations()

    # 测试数据可视化
    await test_data_visualization()

    print("\n所有测试完成！")


if __name__ == "__main__":
    asyncio.run(main())
