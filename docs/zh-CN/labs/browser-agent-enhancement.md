# 浏览器代理增强：实现会话式浏览器工具

本文档记录了对AutoGen浏览器代理的增强实现过程，通过添加会话式浏览器工具，使浏览器代理能够执行更复杂的网页交互操作。

## 需求背景

原有的浏览器代理只能执行简单的网页访问操作，每次操作都需要重新创建浏览器连接，无法在同一个浏览器会话中执行连续的操作。这限制了浏览器代理的能力，使其无法完成更复杂的任务，如搜索操作、表单填写等。

为了增强浏览器代理的能力，我们需要实现以下功能：
1. 维护浏览器会话状态，支持多步连续操作
2. 提供文本输入功能，用于填写表单、搜索框等
3. 提供JavaScript执行功能，用于触发点击事件等操作

## 设计方案

我们采用了会话式浏览器工具的方案，核心思想是维护一个共享的浏览器会话，让多个工具函数可以在同一个浏览器页面上连续操作。

### 方案对比

我们考虑了三种可能的实现方案：

1. **简单工具函数扩展**：每个工具函数独立工作，每次调用都创建新的浏览器连接。
   - 优点：简单易实现，每个工具职责单一
   - 缺点：无法在同一页面上连续操作，效率低下

2. **会话式浏览器工具**：维护一个共享的浏览器会话，所有工具函数共享同一个浏览器连接。
   - 优点：支持多步连续操作，提高性能，更接近真实用户操作体验
   - 缺点：需要实现会话状态管理，复杂度略高

3. **综合浏览器工具函数**：使用一个统一的工具函数，通过不同的参数执行不同的操作。
   - 优点：接口统一，使用简单，灵活支持各种操作
   - 缺点：工具函数内部逻辑复杂，对AI模型使用略有挑战

最终我们选择了**方案二：会话式浏览器工具**，因为它在保持代码清晰的同时，提供了足够强大的功能，让AI能够执行连续的浏览器操作，更接近真实用户的使用体验。

## 实现细节

### 1. 浏览器会话管理器

首先，我们创建了一个`BrowserSession`类，用于管理浏览器会话状态：

```python
class BrowserSession:
    """浏览器会话管理器，维护浏览器会话状态以支持连续操作"""
    
    _instance = None
    
    @classmethod
    async def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = BrowserSession()
            await cls._instance.initialize()
        return cls._instance
    
    def __init__(self):
        """初始化会话管理器"""
        self.client = None
        self.current_url = None
        self.current_title = None
        self.initialized = False
    
    async def initialize(self):
        """初始化浏览器客户端"""
        if not self.initialized:
            print("🌐 初始化浏览器会话...")
            self.client = await create_browser_client()
            self.initialized = True
            print("✅ 浏览器会话初始化完成")
    
    async def close(self):
        """关闭浏览器会话"""
        if self.client:
            print("🔄 关闭浏览器会话...")
            await self.client.close()
            self.client = None
            self.initialized = False
            BrowserSession._instance = None
            print("✅ 浏览器会话已关闭")
    
    @property
    def page(self):
        """获取当前页面对象"""
        return self.client.page if self.client else None
```

这个类使用了单例模式，确保在整个应用程序中只有一个浏览器会话实例，所有工具函数共享同一个浏览器连接。

### 2. 工具函数实现

然后，我们实现了三个工具函数：

1. **open_website**：打开网站并获取内容
   ```python
   async def open_website(url: str, wait_for_load: bool = True) -> str:
       """在会话中打开网站并获取内容"""
       # 实现省略...
   ```

2. **type_text**：在指定元素中输入文本
   ```python
   async def type_text(selector: str, text: str) -> str:
       """在指定元素中输入文本"""
       # 实现省略...
   ```

3. **execute_js**：执行JavaScript代码
   ```python
   async def execute_js(script: str, selector: str = None) -> str:
       """执行JavaScript代码"""
       # 实现省略...
   ```

### 3. 浏览器代理配置

最后，我们更新了浏览器代理的配置，注册新的工具函数，并更新了系统提示：

```python
browser_agent = AssistantAgent(
    name="BrowserAgent",
    model_client=model_client,
    handoffs=["Planner"],
    tools=[open_website, type_text, execute_js],  # 注册增强版浏览器工具
    system_message="""你是一个专业的网页浏览器代理，负责访问网站并执行各种浏览器操作。
你有以下工具可用:
1. open_website(url, wait_for_load=True) - 打开指定网站并获取页面内容
2. type_text(selector, text) - 在指定元素中输入文本
3. execute_js(script, selector=None) - 执行JavaScript代码

当收到访问网站的请求时:
1. 使用open_website工具访问指定网站
2. 如果需要在输入框中输入文本，使用type_text工具
3. 如果需要点击元素或执行其他操作，使用execute_js工具
4. 提取并整理页面的关键内容，生成简洁的摘要
5. 整理内容后交回给Planner

当需要搜索内容时的一般操作流程:
1. 打开搜索引擎，如: await open_website("https://www.bing.com")
2. 在搜索框输入文本，如: await type_text("#sb_form_q", "要搜索的内容")
3. 执行搜索按钮点击，如: await execute_js("document.querySelector('.search-button').click()")
4. 获取搜索结果并整理

不要尝试创作诗歌，这是PoetAgent的任务。你的职责是获取和整理网站内容。""",
)
```

### 4. 会话关闭处理

为了确保浏览器资源被正确释放，我们在主函数结束时添加了会话关闭逻辑：

```python
# 关闭浏览器会话
session = await BrowserSession.get_instance()
await session.close()
```

同时在异常处理中也添加了会话关闭逻辑，确保即使发生错误，浏览器资源也能被正确释放：

```python
# 确保关闭浏览器会话
try:
    session = await BrowserSession.get_instance()
    await session.close()
except:
    pass
```

## 测试运行

我们修改了示例任务，从简单的网站内容获取改为使用Bing搜索特定内容：

```python
# 改为使用Bing搜索的创作任务
request = "请使用Bing搜索'人工智能诗歌创作'，然后根据搜索结果创作一首诗歌"
```

运行结果显示，浏览器代理成功完成了以下操作：
1. 打开Bing搜索页面
2. 在搜索框中输入"人工智能诗歌创作"
3. 执行搜索操作
4. 获取并整理搜索结果
5. 将结果传递给诗人代理，创作出一首诗歌

## 注意事项和局限性

1. **会话状态管理**：虽然会话状态由`BrowserSession`类管理，但如果出现未捕获的异常，可能导致浏览器资源泄漏。
2. **选择器稳定性**：`type_text`和`execute_js`函数依赖于CSS选择器，网站结构变化可能导致选择器失效。
3. **JavaScript执行安全性**：`execute_js`函数允许执行任意JavaScript代码，可能存在安全风险。

## 未来改进方向

1. **更健壮的错误处理**：增强错误处理机制，确保在各种异常情况下都能正确释放资源。
2. **更智能的选择器识别**：实现更智能的元素选择机制，减少对固定选择器的依赖。
3. **添加更多工具函数**：如表单提交、文件上传、cookie管理等。
4. **并发操作支持**：支持在多个标签页上同时执行操作。

## 运行日志

以下是一次成功运行的日志摘要：

```
✅ Browserless服务正常运行，地址: http://localhost:13000
🔑 使用API Base: https://jp.rcouyi.com/v1
🤖 使用模型: gpt-4o-2024-11-20

🚀 启动多代理协作团队，执行任务: 请使用Bing搜索'人工智能诗歌创作'，然后根据搜索结果创作一首诗歌

📝 终止条件设置:
  - Planner输出 "TERMINATE"
  - 最大消息数: 15条
  - 超时时间: 180秒

🌐 初始化浏览器会话...
✅ 浏览器会话初始化完成
🌐 正在访问网站: https://www.bing.com
✅ 页面加载完成
🔍 查找元素: #sb_form_q
⌨️ 在 #sb_form_q 中输入文本: 人工智能诗歌创作
🔧 执行JavaScript代码
...

✅ 任务完成!
⏱️ 总耗时: 86.45秒
📊 终止原因: Text 'TERMINATE' mentioned
🔄 关闭浏览器会话...
✅ 浏览器会话已关闭
```

## 结论

通过实现会话式浏览器工具，我们显著增强了浏览器代理的能力，使其能够执行更复杂的网页交互操作。这为构建更强大的AI智能体应用提供了基础，可以应用于自动化测试、网页内容抓取、信息整理等多种场景。 