# E2B沙盒集成指南

本文档介绍了在OperatorNext项目中集成E2B沙盒的详细过程、设计思路、实现细节和注意事项。

## 1. 背景

OperatorNext项目已经具备了多种浏览器自动化能力：
- Browserless服务：基于Chrome的无头浏览器服务
- Selenium Grid：支持多种浏览器的自动化测试工具
- VM虚拟机服务：通过VNC远程控制虚拟机中的浏览器

为了进一步增强项目的代码执行能力，特别是支持安全地执行用户生成的Python代码（如数据分析、图表生成等），我们引入了E2B沙盒。

## 2. 设计思路

### 2.1 混合式设计模式

本次集成采用了混合式设计模式，在简洁实现的同时保留了扩展性：

```
+---------------------+                 +------------------------+
|   CodeExecutor      |                 |    AutoGen多智能体      |
| (简化的抽象接口)      |<----------------|    (CodeAgent)        |
+---------------------+                 +------------------------+
        |                                        ^
        |                                        |
        v                                        |
+---------------------+                 +------------------------+
|   E2BExecutor       |---------------->|      执行结果/文件      |
| (具体实现，预留扩展)  |                 +------------------------+
+---------------------+
```

这种设计具有以下优势：
- **简洁实现**：相比完全的桥接模式，实现更加简单直接
- **良好扩展性**：预留了接口，未来可以支持其他代码执行后端
- **功能完整**：支持代码执行、包安装、文件操作和数据可视化等核心功能
- **对应用透明**：上层应用使用统一的接口，不需要关心底层实现细节

### 2.2 异步设计

考虑到代码执行和文件操作通常涉及网络请求和I/O操作，我们采用了异步编程模型，基于Python的asyncio实现：
- 所有代码执行和文件操作都是异步方法，返回协程（coroutine）
- 使用`asyncio.to_thread()`将同步的E2B SDK API封装为异步操作
- 避免阻塞主线程，提高性能和响应性

## 3. 实现细节

### 3.1 模块结构

E2B集成模块的文件结构如下：
```
backend/labs/e2b/
├── __init__.py          # 模块初始化文件
├── config.py            # 配置管理
├── executor.py          # 代码执行器抽象接口和实现
├── utils.py             # 辅助工具和函数
└── examples/            # 示例代码
    └── code_team.py     # AutoGen与E2B结合的示例
```

### 3.2 抽象接口设计

`CodeExecutor`抽象基类定义了所有代码执行器必须实现的方法：
- 连接和关闭：`connect()`, `close()`
- 代码执行：`run_code()`, `install_package()`
- 文件操作：`list_files()`, `read_file()`, `write_file()`, `upload_file()`, `download_file()`

### 3.3 E2B实现

`E2BExecutor`类实现了`CodeExecutor`接口，使用E2B SDK提供的功能：
- 使用`Sandbox`类创建安全的沙盒环境
- 封装`run_code()`方法执行Python代码
- 提供`install_package()`方法安装Python包
- 实现完整的文件操作功能

### 3.4 工具函数

`utils.py`提供了一系列辅助工具：
- 文件路径规范化：`sanitize_file_path()`
- 结果格式化：`format_code_result()`
- 数据可视化代码生成：`generate_data_visualization_code()`

## 4. AutoGen集成

我们提供了一个完整的示例`code_team.py`，展示如何将E2B沙盒与AutoGen多智能体系统集成：
- 使用`Swarm`模式创建多代理协作团队：
  - `Planner`：负责协调整个流程
  - `CodeAgent`：负责使用E2B沙盒执行代码
  - `AnalystAgent`：负责分析数据和结果
- 提供多种终止条件控制对话流程
- 定义代码执行、文件操作和数据可视化等工具函数

## 5. 使用指南

### 5.1 环境配置

在`.env`文件中配置E2B API密钥：
```
# E2B 沙盒配置
E2B_API_KEY=your_e2b_api_key
E2B_SANDBOX_TIMEOUT=300  # 沙盒超时时间（秒）
```

### 5.2 基本使用

使用代码执行器执行Python代码：
```python
import asyncio
from backend.labs.e2b import create_code_executor

async def main():
    # 创建代码执行器
    executor = await create_code_executor()
    
    try:
        # 执行代码
        result = await executor.run_code("print('Hello, E2B!')")
        print(result)
        
        # 安装包
        await executor.install_package("pandas")
        
        # 写入文件
        await executor.write_file("/example.txt", "Hello, World!")
        
        # 读取文件
        content = await executor.read_file("/example.txt")
        print(content.decode("utf-8"))
    finally:
        # 关闭执行器
        await executor.close()

asyncio.run(main())
```

### 5.3 数据可视化示例

使用E2B沙盒生成数据可视化：
```python
import asyncio
from backend.labs.e2b import create_code_executor
from backend.labs.e2b.utils import generate_data_visualization_code

async def main():
    executor = await create_code_executor()
    
    try:
        # 创建测试数据
        data_code = """
import pandas as pd
import numpy as np

# 生成随机数据
np.random.seed(42)
data = np.random.randn(100)
df = pd.DataFrame({'values': data})
df.to_csv('/data.csv', index=False)
print('已生成数据文件: /data.csv')
"""
        await executor.run_code(data_code)
        
        # 生成可视化代码
        viz_code = generate_data_visualization_code("/data.csv", "bar")
        
        # 执行可视化代码
        result = await executor.run_code(viz_code)
        print(result)
        
        # 获取生成的图表
        chart_bytes = await executor.read_file("/chart.png")
        
        # 保存图表到本地
        with open("chart.png", "wb") as f:
            f.write(chart_bytes)
            
        print("已保存图表到chart.png")
    finally:
        await executor.close()

asyncio.run(main())
```

## 6. 注意事项

- **API密钥安全**：E2B API密钥应当妥善保管，避免泄露
- **超时设置**：沙盒默认超时时间为300秒，可以根据需要调整
- **包安装**：沙盒环境中安装包可能需要一定时间，请耐心等待
- **文件管理**：沙盒中的文件仅在当前会话有效，请及时下载重要文件
- **资源限制**：沙盒环境有CPU和内存限制，不适合大规模计算任务

## 7. 未来扩展

- 支持更多代码执行后端，如Jupyter内核、本地Docker容器等
- 添加代码执行结果缓存机制，提高性能
- 实现沙盒状态持久化，支持长会话任务
- 增强数据可视化能力，支持更多图表类型和交互式可视化
- 添加代码执行监控和安全审计功能 