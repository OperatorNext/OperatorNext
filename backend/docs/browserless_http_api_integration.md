# Browserless HTTP API 集成开发文档

## 项目概述

本文档记录了为 Browserless 实验模块添加 HTTP API 支持的开发过程和经验。这次开发的主要目标是在现有项目基础上扩展，增加对 Browserless HTTP API 的支持，使开发者可以不依赖 Playwright 库，直接通过 HTTP 请求使用 Browserless 的功能。

## 背景

原有的 Browserless 实验模块主要基于 Playwright 库通过 WebSocket 连接与 Browserless 服务进行交互。这种方式虽然功能强大，但需要额外安装 Playwright 库，且学习成本较高。而 Browserless 提供的 HTTP API 则更加简单直接，适用于不需要复杂交互的场景。

## 需求分析

1. 为项目添加对以下 HTTP API 的支持：
   - `/content` - 获取网页内容
   - `/screenshot` - 网页截图
   - `/pdf` - 生成 PDF
   - `/function` - 执行自定义函数
   - `/download` - 下载文件
   
2. 创建一个示例脚本，展示如何使用这些 API 进行连续操作，形成完整的工作流程

3. 保持与现有代码的一致性，使代码风格和使用方式统一

## 实现方案

### 方案考虑

在实现过程中，我们考虑了以下几种方案：

1. **在现有 `BrowserlessClient` 类中添加 HTTP API 相关方法**
   - 优点：代码集中，使用统一
   - 缺点：混合了 WebSocket 和 HTTP 两种交互方式，职责不清晰

2. **完全独立的函数集**
   - 优点：简单直接
   - 缺点：缺乏结构化，使用不便

3. **创建专门的 HTTP API 客户端类**
   - 优点：职责清晰，使用方便
   - 缺点：需要维护两套客户端代码

最终，我们选择了第三种方案，创建一个专门的 `HTTPBrowserlessClient` 类，与现有的 `BrowserlessClient` 类并列存在。这样既保持了代码结构的一致性，又使职责分工更加清晰。

### 实现步骤

1. 在 `utils.py` 中添加 `HTTPBrowserlessClient` 类，封装 HTTP API 调用
2. 创建 `create_http_client()` 函数，类似于现有的 `create_browser_client()`
3. 编写 `http_api_demo.py` 示例文件，展示各个 API 的使用方法
4. 更新 `README.md`，添加相关文档

## 关键代码实现

### 1. HTTPBrowserlessClient 类

```python
class HTTPBrowserlessClient:
    """Browserless HTTP API 客户端"""
    
    def __init__(self):
        self.base_url = get_browserless_url()
        self.token = get_browserless_token()
        self.session = None
    
    async def _ensure_session(self):
        """确保 HTTP 会话已创建"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def _get_api_url(self, endpoint: str) -> str:
        """获取完整的 API URL"""
        return f"{self.base_url}/{endpoint}?token={self.token}"
    
    # ... 各个 API 方法的实现
```

### 2. 关键 API 方法

每个 API 方法都遵循类似的模式：创建 payload，发送请求，处理响应，返回结果或保存文件。例如：

```python
async def get_content(self, url: str, ...) -> str:
    session = await self._ensure_session()
    api_url = self._get_api_url("content")
    
    payload = {"url": url}
    # ... 添加其他参数
    
    async with session.post(api_url, json=payload) as response:
        if response.status != 200:
            error_text = await response.text()
            raise RuntimeError(f"获取内容失败: {response.status} - {error_text}")
        
        return await response.text()
```

### 3. 示例文件结构

示例文件 `http_api_demo.py` 采用模块化设计，每个 API 对应一个演示函数：

```python
async def demo_content_api(client): ...
async def demo_screenshot_api(client, context): ...
async def demo_function_api(client, context): ...
async def demo_pdf_api(client, context): ...
async def demo_download_api(client, context): ...

async def demo_http_apis():
    # 创建客户端
    client = await create_http_client()
    
    try:
        # 按顺序调用各个演示函数
        context = await demo_content_api(client)
        context = await demo_screenshot_api(client, context)
        # ...
    finally:
        await client.close()
```

## 测试运行

执行示例脚本后，系统会依次执行以下操作：

1. 获取 example.com 的网页内容
2. 对 example.com 和 github.com 进行截图
3. 执行自定义函数，生成随机数据
4. 生成 example.com 和 github.com 的 PDF 文件
5. 下载自定义生成的 JSON 数据文件

所有生成的文件都保存在 `backend/labs/browserless/output/http_api` 目录下。

示例执行输出：

```
Browserless 服务健康检查通过!
CPU 使用率: 0.2%
内存使用率: 5.3%
活跃会话数: 1
开始演示 Browserless HTTP API...

1. 使用 content API 获取网页内容...
页面标题: Example Domain
主标题文本: Example Domain
Github 页面内容长度: 128395 字符

2. 使用 screenshot API 截图...
基本截图已保存: .../output/http_api/example_basic.png
样式化截图已保存: .../output/http_api/example_styled.png
GitHub 截图已保存: .../output/http_api/github.png

3. 使用 function API 执行自定义函数...
函数执行结果:
页面标题: Example Domain
生成的时间戳: 2023-08-15T12:30:45.123Z
随机数: 0.7123456789

4. 使用 pdf API 生成 PDF...
基本 PDF 已保存: .../output/example_basic.pdf
GitHub PDF 已保存: .../output/github.pdf

5. 使用 download API 下载文件...
数据文件已下载: .../output/downloaded_data.json
下载的 JSON 数据:
页面标题: Example Domain
生成时间戳: 2023-08-15T12:30:45.123Z

演示完成! 输出文件保存在:
截图: .../output/http_api
PDF: .../output
下载文件: .../output/downloaded_data.json
```

## 遇到的问题与解决方案

### 1. HTTP 请求格式问题

**问题**: Browserless 的某些 API 对请求格式有特定要求，例如 `function` API 既支持 JSON 也支持直接的 JavaScript 代码。

**解决方案**: 根据 API 文档，我们使用 JSON 格式统一处理所有请求，便于参数管理和错误处理。

### 2. 文件保存路径问题

**问题**: 各种 API 生成的文件需要保存到不同位置，且路径需要确保存在。

**解决方案**: 使用 `pathlib.Path` 库统一处理路径，并在保存文件前自动创建目录结构。

### 3. 错误处理问题

**问题**: HTTP 请求可能因各种原因失败，如网络问题、服务异常等。

**解决方案**: 对每个请求添加错误检查，包括状态码检查和详细的错误信息捕获。

## 经验总结

1. **模块化设计很重要**: 将 HTTP API 客户端独立为一个类，使代码结构更清晰，便于维护和扩展。

2. **参数处理要灵活**: Browserless API 的参数较多，采用可选参数和默认值的方式使 API 更易用。

3. **错误处理要完善**: HTTP 请求容易出错，完善的错误处理可以提高代码的鲁棒性。

4. **文档要详细**: 良好的代码注释和 API 文档对于使用者理解和使用功能至关重要。

5. **示例代码要实用**: 通过具体的示例展示 API 的使用方法，能够帮助使用者更快上手。

## 后续计划

1. 添加对更多 Browserless HTTP API 的支持，如 `/scrape`、`/performance` 等

2. 优化 API 参数处理，增加更多的默认值和简化选项

3. 添加单元测试，确保代码的稳定性和正确性

4. 考虑增加异步重试机制，提高在网络不稳定环境下的可靠性

## 参考资料

- [Browserless HTTP API 文档](https://browserless.io/docs/http.html)
- [aiohttp 文档](https://docs.aiohttp.org/)
- [Python asyncio 文档](https://docs.python.org/3/library/asyncio.html) 