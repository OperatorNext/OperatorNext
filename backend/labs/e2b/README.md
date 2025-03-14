# E2B 沙盒集成

该模块提供了安全执行用户生成Python代码的能力，基于E2B沙盒服务。它允许在隔离的环境中执行代码，安装包，处理文件和生成数据可视化，无需担心系统安全风险。

## 快速开始

### 环境配置

首先，确保安装了必要的依赖：

```bash
pip install e2b_code_interpreter aiofiles
```

在项目的`.env`文件中添加E2B配置：

```
E2B_API_KEY=your_e2b_api_key  # 从 https://e2b.dev 获取
E2B_SANDBOX_TIMEOUT=300       # 沙盒超时时间（秒）
```

### 基本使用

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

## 模块组成

- **`__init__.py`**: 模块初始化文件
- **`config.py`**: 配置管理
- **`executor.py`**: 代码执行器抽象接口和实现
- **`utils.py`**: 辅助工具和函数
  
## 示例

查看 `examples` 目录中的示例：

- **`simple_test.py`**: 基本功能测试，包括代码执行、包安装、文件操作和数据可视化
- **`code_team.py`**: AutoGen多智能体集成示例，展示如何将E2B沙盒与AutoGen结合

## 详细文档

完整的设计文档和API参考请查看 `backend/docs/e2b-integration.md`。 