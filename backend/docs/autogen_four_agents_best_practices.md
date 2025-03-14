# AutoGen四代理协作系统最佳实践

## 1. 系统概述

AutoGen四代理协作系统是一个基于AutoGen Swarm模式的多智能体协作框架，专为复杂任务设计，包含四个专业代理：

1. **Planner（规划者）**：负责协调整个流程，任务分解和进度跟踪
2. **BrowserAgent（浏览器代理）**：负责网络浏览和内容检索
3. **CodeAgent（代码代理）**：负责代码执行和文件处理
4. **AnalystAgent（分析师代理）**：负责数据分析与结果解释

该系统可以处理需要网络检索+代码执行+数据分析的复杂任务，例如：
- 从网络获取数据后进行分析
- 基于网络信息编写和执行代码
- 对编程问题进行在线搜索并实现解决方案
- 综合分析互联网上的数据集

## 2. 系统架构

### 2.1 核心组件

- **会话管理器**：`sessions.py`
  - `BrowserSession`：浏览器会话管理（基于Selenium）
  - `CodeSession`：代码执行会话管理（基于E2B）

- **工具函数**
  - `browser_tools.py`：浏览器相关工具函数
  - `code_tools.py`：代码执行相关工具函数

- **代理定义与协作**：`team_four_agent.py`
  - 定义四个代理及其系统提示词
  - 设置终止条件和协作流程

### 2.2 技术栈

- **AutoGen框架**：使用Swarm模式实现多代理协作
- **Selenium**：网页自动化和内容提取
- **E2B沙盒**：安全的代码执行环境
- **OpenAI API**：提供代理的基础语言能力

## 3. 代理配置最佳实践

### 3.1 Planner（规划者）

**关键职责**：
- 任务分解和子任务分配
- 协调各个专业代理的工作
- 跟踪任务完成情况
- 做出最终结论

**最佳实践**：
- 确保Planner的系统提示准确描述每个代理的能力和限制
- 使其知道何时调用哪个代理，避免任务错误分配
- 提供明确的工作流程指导，特别是任务转交规则
- 要求其在所有任务完成后使用TERMINATE标记结束对话

### 3.2 BrowserAgent（浏览器代理）

**关键职责**：
- 访问网站和执行搜索
- 提取网页内容和数据
- 与网页表单和元素交互
- 获取和分析页面结构

**最佳实践**：
```
在与网页元素交互时：
1. 总是先使用get_page_content()分析页面结构，再尝试操作元素
2. 对于搜索引擎，避免直接使用search_on_web()，而是采用更可靠的手动方法：
   - 打开网站
   - 分析页面找到搜索框
   - 使用type_text()输入查询内容
   - 使用execute_js()提交表单
3. 解决"element not interactable"问题的技巧：
   - 添加等待时间(await asyncio.sleep(2))
   - 使用execute_js而非直接点击
   - 验证元素可见性和可交互性
   - 使用更精确的选择器
```

### 3.3 CodeAgent（代码代理）

**关键职责**：
- 编写和执行Python代码
- 安装必要的软件包
- 文件操作和管理
- 数据处理和可视化

**最佳实践**：
```
编写高质量代码的关键技巧：
1. 总是使用try-except包裹关键操作，提供适当的错误处理
2. 在使用第三方包前先检查是否已安装
3. 保持会话状态的一致性，跟踪已安装的包和创建的文件
4. 数据处理时优先使用pandas等高性能库
5. 生成可视化时使用标准图表类型，确保兼容性
```

### 3.4 AnalystAgent（分析师代理）

**关键职责**：
- 分析数据和结果
- 解释可视化图表
- 提供专业见解和建议
- 总结发现的关键信息

**最佳实践**：
```
数据分析的最佳实践：
1. 先了解数据的来源和收集方法，评估数据质量
2. 使用统计方法验证结论，避免误导性分析
3. 明确区分观察结果和推断，标明不确定性
4. 提供多角度分析，避免单一视角
5. 在适当情况下建议进一步分析方向
```

## 4. 会话管理最佳实践

### 4.1 浏览器会话管理

**最佳实践**：
```
1. 使用单例模式确保会话一致性
2. 跟踪当前URL和页面标题，避免重复操作
3. 设置合理的浏览器窗口大小(1280x800)，兼顾可见性和性能
4. 采用非无头模式便于调试，生产环境可改为无头模式
5. 确保会话结束时正确关闭浏览器，释放资源
```

**常见问题**：
- **元素交互失败**：使用JavaScript执行交互，或增加等待时间
- **选择器失效**：使用更健壮的选择器，如XPath或多属性组合
- **页面加载问题**：实现显式等待机制，确保DOM已完全加载

### 4.2 代码执行会话管理

**最佳实践**：
```
1. 使用单例模式确保沙盒环境一致性
2. 跟踪已安装的包，避免重复安装
3. 跟踪当前文件列表，便于引用和管理
4. 对于长输出，实现合理的截断机制
5. 区分处理文本文件和二进制文件
```

**常见问题**：
- **包安装失败**：提供详细错误信息，尝试替代包或版本
- **代码执行超时**：设置超时机制，避免无限循环
- **内存溢出**：限制可处理的数据量，使用流式处理大型数据集

## 5. 工具函数最佳实践

### 5.1 浏览器工具函数

**get_page_content()** - 获取页面内容的关键工具：
```python
# 最佳用法
content = await get_page_content("html")  # 获取HTML源码
content = await get_page_content("text")  # 获取文本内容
content = await get_page_content("dom")   # 获取DOM结构
content = await get_page_content("both")  # 获取HTML和文本
```

**execute_js()** - 执行JavaScript的推荐模式：
```python
# 直接在页面上下文执行
result = await execute_js("return document.title")

# 在元素上下文执行
result = await execute_js("return el.value", "#search-box")

# 模拟点击操作（比直接点击更可靠）
await execute_js("el.click()", "#submit-button")

# 等待元素可见后操作
await execute_js("""
  return new Promise(resolve => {
    const checkVisible = () => {
      const el = document.querySelector('#element');
      if (el && el.offsetParent !== null) {
        el.click();
        resolve('clicked');
      } else {
        setTimeout(checkVisible, 500);
      }
    };
    checkVisible();
  });
""")
```

### 5.2 代码执行工具函数

**run_code()** - 代码执行的最佳实践：
```python
# 包含错误处理的代码模板
code = """
try:
    import pandas as pd
    
    # 主要操作
    df = pd.read_csv('data.csv')
    result = df.describe()
    print(result)
    
    # 保存结果
    df.to_csv('result.csv')
except Exception as e:
    print(f"错误: {e}")
"""
result = await run_code(code)
```

**generate_chart()** - 数据可视化最佳实践：
```
1. 确保数据文件格式正确，优先使用CSV格式
2. 选择合适的图表类型：数值比较用柱状图，趋势用折线图，占比用饼图
3. 处理缺失值和异常值，避免可视化失真
4. 为图表添加清晰的标题、轴标签和图例
```

## 6. 协作流程优化

### 6.1 任务转交机制

**最佳实践**：
```
1. 明确限制各代理的handoffs选项，确保正确的任务转交路径
2. Planner可以向所有专业代理转交任务
3. 专业代理只能将任务转回Planner
4. 每个代理完成子任务后应提供足够详细的结果，便于下一步操作
```

### 6.2 终止条件设置

系统使用多种终止条件确保可靠运行：
```python
# 1. 文本终止：当Planner输出TERMINATE时终止
text_termination = TextMentionTermination("TERMINATE")

# 2. 消息数量限制：防止无限对话
max_msg_termination = MaxMessageTermination(max_messages=40)

# 3. 时间限制：防止任务运行时间过长
timeout_termination = TimeoutTermination(timeout_seconds=900)  # 15分钟

# 组合终止条件
combined_termination = text_termination | max_msg_termination | timeout_termination
```

## 7. 故障排除和调试技巧

### 7.1 常见错误及解决方案

**1. 浏览器自动化问题**

| 错误 | 解决方案 |
|------|---------|
| Element not interactable | 使用get_page_content分析元素状态，使用JavaScript执行交互，增加等待时间 |
| No such element | 检查选择器是否正确，页面是否已加载完成，使用更强健的选择器 |
| Stale element reference | 每次操作前重新获取元素，避免保存陈旧的元素引用 |
| Selenium Grid连接问题 | 确保Docker容器正常运行，检查网络连接和防火墙设置 |

**2. 代码执行问题**

| 错误 | 解决方案 |
|------|---------|
| 模块未找到 | 使用install_package安装依赖，检查包名称是否正确 |
| 代码执行超时 | 优化代码效率，处理大数据集时使用抽样或流式处理 |
| 文件权限问题 | 确保在正确的路径操作文件，使用绝对路径 |
| E2B API错误 | 检查API密钥配置，确保账户额度充足 |

### 7.2 调试和监控

**最佳实践**：
```
1. 使用分层日志输出，便于问题定位
2. 对每个工具函数调用使用try-except并打印详细错误
3. 记录关键操作时间戳，便于性能分析
4. 非无头模式下可视化监控浏览器操作
5. 保存中间结果，便于问题复现和分析
```

## 8. 安全性和性能考虑

### 8.1 安全最佳实践

```
1. 代码执行严格限制在E2B沙盒环境中
2. 避免在提示词中包含敏感信息
3. 控制API密钥访问权限
4. 限制网络浏览范围，避免访问不安全网站
5. 定期审查代理行为，确保符合预期
```

### 8.2 性能优化

```
1. 使用并行任务处理加速独立操作
2. 实现会话缓存机制，避免重复操作
3. 控制输入/输出大小，避免处理过大的数据量
4. 优化提示词，减少不必要的代理交互
5. 使用更高效的AI模型（如gpt-4o）提高代理能力
```

## 9. 项目结构和代码组织

代码结构采用模块化设计，便于维护和扩展：

```
backend/labs/autogen/examples/four_agents/
├── __init__.py              # 包初始化文件
├── team_four_agent.py       # 主文件，定义代理和协作流程
├── sessions.py              # 会话管理模块
├── browser_tools.py         # 浏览器工具函数
└── code_tools.py            # 代码执行工具函数
```

**最佳实践**：
```
1. 使用相对导入确保模块间正确引用
2. 添加项目根目录到Python路径，解决导入问题
3. 为每个模块提供清晰的文档字符串
4. 使用类型注解提高代码可读性
5. 保持一致的错误处理和日志记录模式
```

## 10. 未来发展方向

### 10.1 功能增强

- **增强BrowserAgent的能力**：添加更复杂的网页交互，如表单填写和AJAX内容处理
- **扩展CodeAgent的代码生成能力**：支持更多编程语言和框架
- **提升AnalystAgent的分析深度**：整合更多统计工具和可视化类型
- **改进Planner的协调能力**：实现更精细的任务分解和资源调度

### 10.2 架构优化

- **增加记忆组件**：允许代理记住过去的交互和决策
- **实现更灵活的代理网络**：支持动态调整代理数量和类型
- **添加人类反馈循环**：允许人类在关键点介入指导代理行为
- **集成更多外部服务**：扩展系统能力边界

---

## 附录：快速启动指南

### 环境准备

1. 确保已安装必要的包：
```bash
pip install e2b_code_interpreter aiofiles python-dotenv autogenchat
```

2. 启动Selenium服务：
```bash
docker-compose up -d selenium-hub selenium-chromium
```

3. 配置环境变量（.env文件）：
```
OPENAI_API_KEY=your_openai_api_key
E2B_API_KEY=your_e2b_api_key
```

### 运行示例

```bash
python -m backend.labs.autogen.examples.four_agents.team_four_agent
```

### 自定义任务

修改`team_four_agent.py`中的`request`变量，自定义任务描述：

```python
request = """请帮我完成以下任务:
1. [第一步描述]
2. [第二步描述]
...
"""
``` 