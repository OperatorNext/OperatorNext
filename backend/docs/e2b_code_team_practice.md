# E2B多代理代码沙盒执行团队实践经验

**文档版本**: v1.0  
**创建日期**: 2024-07-01  
**适用环境**: Python 3.11+, AutoGen Swarm, E2B沙盒  

> 本文档详细记录了使用AutoGen的Swarm模式和E2B沙盒创建多代理协作团队的实践经验，包含完整的代码示例、提示词设计、运行方法和最佳实践。

## 目录

- [概述](#概述)
- [关键技术组件](#关键技术组件)
- [运行环境设置](#运行环境设置)
  - [环境准备](#环境准备)
  - [模块导入问题解决](#模块导入问题解决)
  - [参考运行命令](#参考运行命令)
- [代码实现](#代码实现)
  - [E2B代码会话管理器](#1-e2b代码会话管理器)
  - [代码工具函数](#2-代码工具函数)
  - [多代理团队设置](#3-多代理团队设置)
  - [终止条件设置](#4-终止条件设置)
- [代理提示词(Prompts)](#代理提示词prompts)
  - [Planner规划者提示词](#planner规划者提示词)
  - [CodeAgent代码代理提示词](#codeagent代码代理提示词)
  - [AnalystAgent分析师代理提示词](#analystagent分析师代理提示词)
  - [用户任务示例提示词](#用户任务示例提示词)
- [实际执行流程](#实际执行流程)
- [执行结果分析](#执行结果分析)
- [示例数据分析代码](#示例数据分析代码)
- [最佳实践经验](#最佳实践经验)
- [常见问题与排查解决方案](#常见问题与排查解决方案)

## 概述

本文档记录了使用AutoGen的Swarm模式和E2B沙盒创建多代理协作团队的实践经验。通过构建一个由Planner(规划者)、CodeAgent(代码代理)和AnalystAgent(分析师代理)组成的团队，成功实现了完整的数据分析流程自动化执行。

## 关键技术组件

- **AutoGen Swarm模式**：实现多代理协作团队的核心框架
- **E2B沙盒**：提供安全的代码执行环境
- **函数工具注册**：为代理赋能，使其能执行特定操作
- **终止条件**：管理多代理对话的完成标准

## 运行环境设置

### 环境准备

在运行`code_team.py`前，请确保：
1. 已安装所需依赖：`pip install e2b_code_interpreter aiofiles autogen-agentchat`
2. 配置好`.env`文件，设置必要的API密钥（OPENAI_API_KEY、E2B_API_KEY等）

### 模块导入问题解决

在执行脚本时，可能会遇到模块导入错误：
```
ModuleNotFoundError: No module named 'labs'
```

这是因为Python解释器不会自动将当前目录视为包的根目录。以下是几种解决方案：

#### 方案1：通过Python模块方式运行

这是最规范的运行方式：
```bash
# 从backend目录运行
cd /path/to/project/backend
python -m labs.e2b.examples.code_team
```

#### 方案2：使用__main__.py入口点

我们在`labs/e2b/examples`目录下添加了`__main__.py`文件，允许将examples目录作为包运行：
```bash
# 从backend目录运行
cd /path/to/project/backend
python -m labs.e2b.examples
```
这将显示可用示例列表和运行指南。

#### 方案3：使用便捷启动脚本

项目根目录下的`run_e2b_examples.py`提供了更友好的界面：
```bash
# 从backend目录运行
cd /path/to/project/backend
python run_e2b_examples.py code_team
# 或查看所有可用示例
python run_e2b_examples.py
```

### 参考运行命令

以下提供完整的运行命令参考，包括环境变量设置：

```bash
# 设置必要的环境变量(如果未在.env文件中配置)
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_API_BASE="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-4o"
export E2B_API_KEY="your-e2b-api-key"

# 方法1: 使用Python模块方式运行
cd /path/to/project/backend
python -m labs.e2b.examples.code_team

# 方法2: 使用便捷启动脚本
cd /path/to/project/backend
python run_e2b_examples.py code_team

# 自定义任务运行(修改默认任务)
# 可以修改code_team.py文件中的request变量来自定义任务
```

项目根目录的启动脚本(`run_e2b_examples.py`)示例：

```python
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

import os
import sys
import importlib
import asyncio
import argparse


def list_examples():
    """列出可用的E2B示例"""
    examples_dir = os.path.join('labs', 'e2b', 'examples')
    examples = []
    
    # 确保目录存在
    if not os.path.exists(examples_dir):
        print(f"错误: 找不到示例目录 {examples_dir}")
        return []
    
    for file in os.listdir(examples_dir):
        if file.endswith('.py') and file != '__main__.py' and not file.startswith('_'):
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
        if hasattr(module, 'main'):
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

## 代码实现

`code_team.py`脚本实现了一个完整的多代理协作团队。以下是关键代码段及其说明：

### 1. E2B代码会话管理器

```python
class CodeSession:
    """代码会话管理器，维护E2B沙盒会话状态以支持连续操作"""

    _instance = None

    @classmethod
    async def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = CodeSession()
            await cls._instance.initialize()
        return cls._instance

    def __init__(self):
        """初始化会话管理器"""
        self.executor = None
        self.initialized = False
        self.current_files = []
        self.installed_packages = set()

    async def initialize(self):
        """初始化E2B沙盒执行器"""
        if not self.initialized:
            print("🚀 初始化E2B沙盒会话...")
            self.executor = await create_code_executor()
            self.initialized = True
            print("✅ E2B沙盒会话初始化完成")

    async def close(self):
        """关闭沙盒会话"""
        if self.executor:
            print("🔄 关闭E2B沙盒会话...")
            await self.executor.close()
            self.executor = None
            self.initialized = False
            CodeSession._instance = None
            print("✅ E2B沙盒会话已关闭")
```

这个会话管理器采用单例模式，确保在整个执行过程中只有一个E2B沙盒会话实例，提高资源利用效率。

### 2. 代码工具函数

```python
async def run_code(code: str) -> str:
    """在E2B沙盒中运行代码并返回结果"""
    # 获取会话实例
    session = await CodeSession.get_instance()
    try:
        # 确保执行器已初始化
        if not session.executor:
            return "错误: E2B沙盒未初始化"
        # 执行代码
        print("🧪 执行代码...")
        result = await session.executor.run_code(code)
        # 更新文件列表并返回格式化输出
        # ...
    except Exception as e:
        return f"❌ 运行代码时出错: {str(e)}"
```

系列工具函数包括：`run_code`、`install_package`、`list_files`、`read_file`、`write_file`等，为代理提供了与E2B沙盒交互的能力。

### 3. 多代理团队设置

```python
# 1. 创建规划者智能体 - 负责协调整个流程
planner = AssistantAgent(
    name="Planner",
    model_client=model_client,
    # 规划者可以将任务交给代码代理或分析师代理
    handoffs=["CodeAgent", "AnalystAgent"],
    system_message="""你是一个负责协调代码执行和数据分析流程的规划者。
你需要按照以下流程协调团队工作:
1. 首先分析用户的需求，确定需要执行的代码任务
2. 将具体的代码执行任务交给CodeAgent完成
3. 将数据分析和结果解释任务交给AnalystAgent完成
4. 最后总结整个流程，确认完成后输出TERMINATE以结束任务
"""
)

# 2. 创建代码代理 - 专门负责代码执行
code_agent = AssistantAgent(
    name="CodeAgent",
    model_client=model_client,
    # 代码代理只能将任务交回给规划者
    handoffs=["Planner"],
    tools=[run_code, install_package, list_files, read_file, write_file, generate_chart],
    system_message="""你是一个专业的代码执行代理，负责在E2B沙盒中执行Python代码。
你有以下工具可用:
1. run_code(code) - 在沙盒中执行Python代码
2. install_package(package_name) - 安装Python包
3. list_files(path="/") - 列出目录中的文件
4. read_file(file_path) - 读取文件内容
5. write_file(file_path, content) - 写入文件
6. generate_chart(data_file, chart_type="bar") - 生成数据可视化图表

当收到代码执行任务时:
1. 如果需要安装包，使用install_package工具
2. 使用write_file工具创建必要的文件
3. 使用run_code工具执行代码
4. 使用list_files和read_file检查结果
5. 如果需要数据可视化，使用generate_chart工具

执行完任务后:
1. 整理执行结果和文件状态
2. 将完整的执行过程和结果交回给Planner

你应始终遵循以下原则:
- 为代码添加详细注释，确保可读性
- 合理拆分复杂任务为多个步骤
- 始终检查执行结果并报告任何错误
- 在返回前整理和总结执行过程
"""
)

# 3. 创建分析师代理 - 专门负责数据分析
analyst_agent = AssistantAgent(
    name="AnalystAgent",
    model_client=model_client,
    # 分析师代理只能将任务交回给规划者
    handoffs=["Planner"],
    tools=[read_file],  # 分析师只需要读取文件的工具
    system_message="""你是一位数据分析专家，擅长解释代码执行结果和分析数据。
你可以使用read_file工具查看数据文件和结果文件。

当你收到数据分析任务时:
1. 仔细研究代码执行结果和生成的数据
2. 提供专业的数据解读和见解
3. 指出数据中的关键趋势、模式或异常
4. 若有图表，解释图表呈现的信息
5. 提供进一步分析的建议

你的分析应该:
- 专业、深入且客观
- 使用适当的统计术语
- 避免过度解读数据
- 指出数据或方法的局限性
- 在适当的地方提供改进建议

完成分析后，将你的见解交回给Planner。
"""
)
```

每个代理都有明确的职责边界和可用工具，确保了专业分工。

### 4. 终止条件设置

```python
# 设置多种终止条件
# 1. 当Planner输出TERMINATE时终止
text_termination = TextMentionTermination("TERMINATE")

# 2. 最大消息数量限制(防止无限对话)
max_msg_termination = MaxMessageTermination(max_messages=30)

# 3. 对话超时限制(单位：秒)
timeout_termination = TimeoutTermination(timeout_seconds=600)  # 10分钟超时

# 组合终止条件：满足任一条件即终止
combined_termination = text_termination | max_msg_termination | timeout_termination
```

合理的终止条件可以防止对话无限进行，提高系统的可靠性。

## 代理提示词(Prompts)

代理提示词是多代理系统的核心组成部分，它定义了每个代理的行为、职责和协作方式。以下是本系统中各代理的完整提示词：

### Planner规划者提示词

```
你是一个负责协调代码执行和数据分析流程的规划者。
你需要按照以下流程协调团队工作:

1. 首先分析用户的需求，确定需要执行的代码任务
2. 将具体的代码执行任务交给CodeAgent完成
3. 将数据分析和结果解释任务交给AnalystAgent完成
4. 最后总结整个流程，确认完成后输出TERMINATE以结束任务

请确保每次只将任务交给一个代理，并等待其完成后再进行下一步。
当所有任务完成后，请输出TERMINATE。
```

### CodeAgent代码代理提示词

```
你是一个专业的代码执行代理，负责在E2B沙盒中执行Python代码。
你有以下工具可用:
1. run_code(code) - 在沙盒中执行Python代码
2. install_package(package_name) - 安装Python包
3. list_files(path="/") - 列出目录中的文件
4. read_file(file_path) - 读取文件内容
5. write_file(file_path, content) - 写入文件
6. generate_chart(data_file, chart_type="bar") - 生成数据可视化图表

当收到代码执行任务时:
1. 如果需要安装包，使用install_package工具
2. 使用write_file工具创建必要的文件
3. 使用run_code工具执行代码
4. 使用list_files和read_file检查结果
5. 如果需要数据可视化，使用generate_chart工具

执行完任务后:
1. 整理执行结果和文件状态
2. 将完整的执行过程和结果交回给Planner

你应始终遵循以下原则:
- 为代码添加详细注释，确保可读性
- 合理拆分复杂任务为多个步骤
- 始终检查执行结果并报告任何错误
- 在返回前整理和总结执行过程
```

### AnalystAgent分析师代理提示词

```
你是一位数据分析专家，擅长解释代码执行结果和分析数据。
你可以使用read_file工具查看数据文件和结果文件。

当你收到数据分析任务时:
1. 仔细研究代码执行结果和生成的数据
2. 提供专业的数据解读和见解
3. 指出数据中的关键趋势、模式或异常
4. 若有图表，解释图表呈现的信息
5. 提供进一步分析的建议

你的分析应该:
- 专业、深入且客观
- 使用适当的统计术语
- 避免过度解读数据
- 指出数据或方法的局限性
- 在适当的地方提供改进建议

完成分析后，将你的见解交回给Planner。
```

### 用户任务示例提示词

以下是提供给多代理团队的示例任务提示：

```
请帮我执行以下数据分析任务:
1. 生成一个包含100个随机数据点的数据集
2. 计算基本统计信息(均值、标准差、最大值、最小值等)
3. 绘制数据分布的直方图
4. 检测数据中的异常值并分析它们的影响
```

这个任务示例展示了一个完整的数据分析流程，包括数据生成、统计分析、可视化和异常值检测，是测试多代理协作能力的理想任务。

## 实际执行流程

运行`code_team.py`脚本后，执行流程如下：

1. **初始化阶段**
   - E2B沙盒会话初始化
   - 模型客户端连接
   - 多代理团队组建
   - 终止条件设置

2. **任务执行阶段**
   ```
   # 日志节选
   🚀 启动多代理协作团队，执行任务: 请帮我执行以下数据分析任务:
   1. 生成一个包含100个随机数据点的数据集
   2. 计算基本统计信息(均值、标准差、最大值、最小值等)
   3. 绘制数据分布的直方图
   4. 检测数据中的异常值并分析它们的影响

   📝 终止条件设置:
     - Planner输出 "TERMINATE"
     - 最大消息数: 30条
     - 超时时间: 600秒
   ```

3. **Planner规划阶段**
   ```
   # 日志节选
   ---------- Planner ----------
   好的，让我们开始分析用户需求并规划任务：

   ### 用户需求分解及任务规划
   1. **生成随机数据集**：需要运行代码生成一个包含 100 个随机数据点的数据集。
   2. **计算基本统计信息**：包括均值、标准差、最大值、最小值等，需要分析代码生成的数据。
   3. **绘制直方图**：需要基于生成的数据绘制分布图。
   4. **检测异常值并分析影响**：需要检测数据中的异常值（例如，基于某些统计标准），并解释它们如何影响数据。
   ```

4. **CodeAgent执行阶段**
   ```
   # 日志节选
   ---------- CodeAgent ----------
   [写入文件: data_analysis.py]
   ✅ 文件已成功写入: data_analysis.py
   🧪 执行代码...
   ✅ 代码执行成功:
   ```

5. **AnalystAgent分析阶段**
   ```
   # 日志节选
   ---------- AnalystAgent ----------
   ### 数据分析成果解读

   #### 一、基本统计信息
   根据文件 **`data_stats.json`** 提供的内容：
   - 平均值 (**mean**) 为 0.0415，接近于 0，这符合随机数据通常围绕指定均值的特性。
   - 标准差 (**std**) 为 1.0833，表明数据围绕平均值的分散程度略高于默认正态分布标准差 (1)。
   ```

6. **任务完成阶段**
   ```
   # 日志节选
   ---------- Planner ----------
   ### 整体任务总结

   #### 已完成任务：
   1. **生成随机数据集**：通过 CodeAgent 创建了包含 100 个随机数据点的数据集。
   2. **计算基本统计信息**：数据均值、标准差、最大值和最小值已计算完成，存储于 `data_stats.json` 文件。
   3. **绘制数据分布直方图**：图表已成功生成，存储于 `data_histogram.png` 文件。
   4. **检测异常值并分析影响**：检测出一个异常值，并分析了异常值对数据的影响，结果保存在 `outlier_analysis.json` 文件中。

   **TERMINATE**
   ```

## 执行结果分析

整个任务执行用时约54.83秒，成功完成了以下各步骤：

1. **数据生成**：创建了包含100个服从正态分布的随机数据点，保存到`data_points.csv`
2. **统计分析**：计算了基本统计指标(均值=0.0415, 标准差=1.0833, 最大值=3.4427, 最小值=-2.7382)
3. **数据可视化**：生成了数据分布直方图，保存为`data_histogram.png`
4. **异常值检测**：使用Z-score方法检测到一个异常值(3.4427)，分析了其对数据的影响

执行结果完全符合预期，通过多代理协作，成功实现了从数据生成到分析的完整流程自动化。

## 示例数据分析代码

以下是CodeAgent在执行过程中生成并执行的数据分析代码。这个示例展示了AI智能体如何编写Python代码来完成复杂的数据分析任务：

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

# Step 1: Generate Random Data
data = np.random.normal(loc=0, scale=1, size=100)  # Generating 100 random points with normal distribution
np.savetxt("data_points.csv", data, delimiter=",")

# Step 2: Compute Basic Statistics
mean = np.mean(data)
std = np.std(data)
max_val = np.max(data)
min_val = np.min(data)

stats = {
    "mean": mean,
    "std": std,
    "max": max_val,
    "min": min_val
}

with open('data_stats.json', 'w') as f:
    json.dump(stats, f)

# Step 3: Generate Histogram
plt.hist(data, bins=10, edgecolor='black')
plt.title('Data Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.savefig('data_histogram.png')
plt.close()

# Step 4: Detect Outliers Using Z-Score
z_scores = np.abs((data - mean) / std)
outlier_indices = np.where(z_scores > 3)  # Considering Z-score > 3 as outliers
outliers = data[outlier_indices]

outlier_analysis = {
    "outliers": outliers.tolist(),
    "count": len(outliers)
}

with open('outlier_analysis.json', 'w') as f:
    json.dump(outlier_analysis, f)
```

代码亮点：
1. 使用NumPy生成符合正态分布的随机数据
2. 计算并存储基本统计信息为JSON格式，便于后续分析
3. 使用Matplotlib创建数据分布的直方图进行可视化
4. 基于Z-score方法进行异常值检测，阈值设置为3（标准差的3倍）

这个代码示例体现了AI代理生成的代码质量高、注释完善、步骤清晰，适合作为类似数据分析任务的模板参考。

## 最佳实践经验

基于此次实践，总结出以下最佳实践经验：

### 1. 代理职责分明

清晰定义每个代理的职责边界，并通过system_message进行明确指导：
- **Planner**：负责全局协调和任务分配
- **CodeAgent**：专注于代码执行，不负责分析结果
- **AnalystAgent**：专注于数据分析，不参与代码编写

### 2. 资源管理优化

- 使用单例模式管理E2B沙盒会话，避免重复创建资源
- 合理关闭沙盒会话，避免资源泄漏
- 工具函数设计全面异常处理，确保执行稳定性

### 3. 通信机制设计

- 使用handoffs机制明确定义代理间的通信路径和权限
- 规划者(Planner)作为中心枢纽，协调各专业代理的工作
- 使用文件作为数据交换媒介，实现代理间的数据共享

### 4. 终止条件多样化

设置多重终止条件，提高系统可靠性：
- 显式终止指令("TERMINATE")
- 最大消息数限制
- 超时保护机制

### 5. 工具函数设计原则

- **原子性**：每个工具函数专注于单一功能
- **健壮性**：全面的错误处理和状态反馈
- **输出友好**：格式化输出结果，便于其他代理理解和使用

## 总结

E2B多代理代码沙盒执行团队模式是一种强大的自动化数据分析解决方案。通过合理的架构设计和职责划分，可以实现复杂任务的自动化执行，大幅提高效率。

此实践也展示了未来AI协作模式的潜力：专业化的代理各司其职，通过明确的通信机制协同工作，共同完成复杂任务，实现整体能力大于各部分之和。

## 常见问题与排查解决方案

在使用E2B多代理代码沙盒执行团队时，可能会遇到以下常见问题，以下是排查和解决方案：

### 1. E2B沙盒连接问题

**症状**：初始化E2B沙盒时出现连接错误或超时。

**解决方案**：
- 检查E2B_API_KEY是否正确配置在.env文件中
- 确认网络连接稳定，可能需要代理设置
- 验证E2B服务状态：`await check_e2b_status()`

### 2. 模型API调用失败

**症状**：与模型通信时出现错误，如API密钥无效、请求超时等。

**解决方案**：
- 确认OPENAI_API_KEY和OPENAI_API_BASE配置正确
- 检查模型名称是否支持（例如OPENAI_MODEL设置为"gpt-4o"）
- 如果使用代理，确保API请求能正常通过

### 3. 代理协作中断

**症状**：任务执行过程中代理协作中断，例如某个代理无法完成任务或传递错误。

**解决方案**：
- 检查代理定义的handoffs是否正确配置
- 确保每个代理的system_message明确指导其职责和协作方式
- 调整终止条件，延长超时或增加最大消息数

### 4. 沙盒执行权限问题

**症状**：CodeAgent无法在沙盒中执行特定操作，如文件写入、包安装等。

**解决方案**：
- E2B沙盒默认提供大部分Python操作权限
- 对于特殊操作（如网络请求），需确认沙盒环境支持
- 使用try-except处理可能的权限异常，提供友好错误信息

### 5. 性能和资源消耗

**症状**：执行过程缓慢或资源消耗过高。

**解决方案**：
- 使用单例模式管理沙盒会话（已实现）
- 任务完成后显式关闭沙盒会话释放资源
- 避免不必要的文件操作，合并小型操作减少API调用

### 6. 数据可视化问题

**症状**：图表生成失败或无法正确显示。

**解决方案**：
- 确保安装了必要的可视化库（matplotlib, seaborn等）
- 使用适当的文件格式保存图表（PNG通常兼容性最好）
- 检查图表显示设置，确保在无GUI环境下仍能正常工作

实施这些解决方案可以大幅提高E2B多代理代码沙盒执行团队的稳定性和效率。定期检查日志和执行状态，及时发现并解决问题。

---

**相关资源**
- [AutoGen GitHub仓库](https://github.com/microsoft/autogen)
- [E2B代码解释器文档](https://docs.e2b.dev/)
- [Python asyncio文档](https://docs.python.org/3/library/asyncio.html)