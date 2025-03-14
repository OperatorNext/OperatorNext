"""
E2B实用工具函数

提供各种辅助功能的实用工具函数。
"""

import os
import re
from typing import Any


def sanitize_file_path(path: str) -> str:
    """
    清理文件路径，移除不安全的字符

    Args:
        path: 原始文件路径

    Returns:
        清理后的文件路径
    """
    # 替换所有不安全的字符为下划线
    safe_path = re.sub(r"[^\w\-./]", "_", path)

    # 确保路径不包含../（防止目录遍历）
    while "../" in safe_path:
        safe_path = safe_path.replace("../", "./")

    # 确保路径以/开头，然后去掉多余的/
    if not safe_path.startswith("/"):
        safe_path = "/" + safe_path
    safe_path = re.sub(r"/+", "/", safe_path)

    return safe_path


def format_code_result(result: dict[str, Any]) -> str:
    """
    格式化代码执行结果为可读的字符串

    Args:
        result: 代码执行结果字典

    Returns:
        格式化后的结果字符串
    """
    if not result["success"]:
        return f"执行失败：{result['error']}"

    output = "执行成功：\n"
    if result["text"]:
        output += f"输出结果：\n{result['text']}\n"
    if result["logs"]:
        output += f"日志：\n{', '.join(result['logs'])}\n"

    return output


def ensure_matplotlib_config() -> str:
    """
    生成确保Matplotlib可以在无头环境中工作的代码片段

    Returns:
        配置Matplotlib的代码
    """
    return """
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
"""


def generate_data_visualization_code(data_file: str, chart_type: str = "bar") -> str:
    """
    根据数据文件和图表类型生成数据可视化代码

    Args:
        data_file: 数据文件路径
        chart_type: 图表类型，支持 'bar', 'line', 'scatter', 'pie'

    Returns:
        Python代码字符串
    """
    # Matplotlib配置代码
    matplotlib_config = ensure_matplotlib_config()

    # 基本导入和数据加载代码
    code = f"""
{matplotlib_config}
import pandas as pd
import numpy as np

# 读取{os.path.splitext(data_file)[1][1:].upper()}文件
df = pd.read_csv('{data_file}')
print(f"数据预览：\\n{{df.head()}}\\n")

# 显示基本统计信息
print("数据统计：")
print(df.describe())
print("")

# 检查数据列
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if len(numeric_cols) < 2 and '{chart_type}' not in ['bar', 'pie']:
    print("警告：数值列不足，可能无法生成某些图表")
"""

    # 根据图表类型添加特定代码
    if chart_type == "bar":
        code += """
# 准备数据
if len(df.columns) >= 2:
    # 如果有足够的列，使用第一列作为标签，第二列作为值
    labels = df.iloc[:, 0].tolist()
    values = df.iloc[:, 1].tolist()
else:
    # 否则使用索引作为标签，第一列作为值
    labels = df.index.tolist()
    values = df.iloc[:, 0].tolist()

# 创建柱状图
plt.figure(figsize=(10, 6))
bars = plt.bar(labels, values)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f}', ha='center', va='bottom')

# 添加标题和标签
plt.title('柱状图可视化')
plt.xlabel('类别')
plt.ylabel('值')
plt.xticks(rotation=45)
plt.tight_layout()

# 保存图表
plt.savefig('/chart.png', dpi=300, bbox_inches='tight')
print("已生成柱状图：chart.png")
"""
    elif chart_type == "line":
        code += """
# 检查是否有时间列
time_col = None
for col in df.columns:
    if col.lower() in ['date', 'time', 'datetime', 'timestamp', 'period']:
        time_col = col
        break

# 准备数据
plt.figure(figsize=(12, 6))

if time_col is not None:
    # 如果有时间列，将其转换为索引
    try:
        df[time_col] = pd.to_datetime(df[time_col])
        df.set_index(time_col, inplace=True)
    except:
        pass  # 如果转换失败，继续使用原始数据

# 获取数值列
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# 绘制折线图
for col in numeric_cols[:3]:  # 只绘制前三个数值列
    plt.plot(df.index, df[col], marker='o', linestyle='-', label=col)

# 添加标题和标签
plt.title('时间序列折线图')
plt.xlabel('时间/索引')
plt.ylabel('值')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

# 保存图表
plt.savefig('/chart.png', dpi=300, bbox_inches='tight')
print("已生成折线图：chart.png")
"""
    elif chart_type == "scatter":
        code += """
# 获取数值列
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

if len(numeric_cols) >= 2:
    # 选择前两个数值列作为散点图的x和y
    x_col, y_col = numeric_cols[0], numeric_cols[1]
    
    # 如果有第三个数值列，用它作为点的大小
    size_col = numeric_cols[2] if len(numeric_cols) >= 3 else None
    
    # 创建散点图
    plt.figure(figsize=(10, 8))
    
    if size_col:
        # 归一化大小以便于可视化
        sizes = 20 + 180 * (df[size_col] - df[size_col].min()) / (df[size_col].max() - df[size_col].min() + 0.0001)
        scatter = plt.scatter(df[x_col], df[y_col], s=sizes, alpha=0.6, c=df[size_col], cmap='viridis')
        plt.colorbar(scatter, label=size_col)
    else:
        plt.scatter(df[x_col], df[y_col], alpha=0.6)
    
    # 添加标题和标签
    plt.title(f'{x_col} vs {y_col} 散点图')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
else:
    plt.figure(figsize=(8, 6))
    plt.text(0.5, 0.5, '数据列不足，无法创建散点图', ha='center', va='center', fontsize=12)
    plt.axis('off')

# 保存图表
plt.savefig('/chart.png', dpi=300, bbox_inches='tight')
print("已生成散点图：chart.png")
"""
    elif chart_type == "pie":
        code += """
# 准备数据
if len(df.columns) >= 2:
    # 使用第一列作为标签，第二列作为值
    labels = df.iloc[:, 0].tolist()
    values = df.iloc[:, 1].tolist()
else:
    # 如果只有一列，使用索引作为标签
    labels = df.index.tolist()
    values = df.iloc[:, 0].tolist()

# 确保值为正数
values = [max(0, v) for v in values]

# 创建饼图
plt.figure(figsize=(10, 8))
patches, texts, autotexts = plt.pie(
    values, 
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    shadow=True,
    explode=[0.05] * len(values)  # 略微分离所有部分
)

# 美化
for text in texts:
    text.set_fontsize(12)
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_color('white')

# 添加标题
plt.title('饼图分布')
plt.axis('equal')  # 确保饼图是圆形的
plt.tight_layout()

# 保存图表
plt.savefig('/chart.png', dpi=300, bbox_inches='tight')
print("已生成饼图：chart.png")
"""
    else:
        # 默认为条形图
        code += """
# 不支持的图表类型，使用默认条形图
plt.figure(figsize=(10, 6))
df.iloc[:, 0].plot(kind='bar')
plt.title('默认条形图')
plt.tight_layout()

# 保存图表
plt.savefig('/chart.png', dpi=300, bbox_inches='tight')
print("已生成默认图表：chart.png")
"""

    return code
