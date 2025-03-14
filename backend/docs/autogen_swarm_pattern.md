# AutoGen Swarm模式多代理协作系统实现指南

## 1. 背景介绍

在构建AI系统时，单一代理的局限性日益明显。为了解决复杂任务，我们采用了AutoGen框架的Swarm模式，构建了一个多代理协作系统。通过将任务分解给专业代理，我们实现了更高效、更高质量的内容生成过程。

本文档记录了我们如何将单一代理系统重构为多代理Swarm协作模式，以及在这个过程中获得的最佳实践经验。

## 2. 问题分析与解决方案

### 2.1 原始系统的局限性

最初的浏览器助手是一个单一代理系统：

- 一个代理负责**所有**任务：网页浏览、内容提取、诗歌创作
- 终止条件依赖于代理输出特定的终止标记（`[诗歌创作完成]`）
- 缺乏明确的流程控制和专业分工

这种设计导致了几个问题：
- 代理需要同时掌握多种能力，容易"身兼数职"但效果不佳
- 任务耦合严重，难以单独优化某一环节
- 终止逻辑不够清晰，有时需要到达最大消息数才终止

### 2.2 Swarm模式解决方案

我们采用AutoGen的Swarm模式，将系统重构为三个专业代理协作团队：

1. **Planner(规划者)** - 团队"大脑"，负责协调整个流程
2. **BrowserAgent(浏览器代理)** - 专门负责访问网站获取内容
3. **PoetAgent(诗人代理)** - 专门负责将网站内容转化为诗歌

并引入了以下改进：
- 使用`handoffs`机制实现代理间的任务交接
- 专业分工，每个代理专注于自己擅长的领域
- 将终止决策权交给Planner，通过检测"TERMINATE"关键词终止流程

## 3. 实现细节

### 3.1 Swarm模式核心概念

在AutoGen的Swarm模式中，关键概念包括：

- **参与者(Participants)** - 加入团队的多个代理
- **交接(Handoffs)** - 代理之间传递任务的机制
- **终止条件(Termination Condition)** - 结束对话的条件

与其他团队协作模式不同，Swarm允许代理自行决定将任务交给谁，形成一种分散式的任务规划机制。

### 3.2 代码实现

#### 创建专业代理

```python
# 1. 创建规划者智能体 - 负责协调整个流程
planner = AssistantAgent(
    name="Planner",
    model_client=model_client,
    # 规划者可以将任务交给浏览器代理或诗人代理
    handoffs=["BrowserAgent", "PoetAgent"],
    system_message="""你是一个负责协调网页诗歌创作流程的规划者。
你需要按照以下流程协调团队工作:
1. 首先让BrowserAgent访问指定网站并获取内容
2. 然后让PoetAgent将网站内容转化为优美的诗歌
3. 最后检查诗歌，确认完成后输出TERMINATE以结束任务

请确保每次只将任务交给一个代理，并等待其完成后再进行下一步。
当看到"[诗歌创作完成]"标记时，请检查诗歌质量，如果满意则输出TERMINATE。""",
)

# 2. 创建浏览器代理 - 专门负责访问网站
browser_agent = AssistantAgent(
    name="BrowserAgent",
    model_client=model_client,
    # 浏览器代理只能将任务交回给规划者
    handoffs=["Planner"],
    tools=[browse_website],  # 注册浏览网站工具
    system_message="""你是一个专业的网页浏览器代理，负责访问网站并获取内容。
你只有一个工具可用: browse_website - 访问网站并获取页面HTML内容

当收到访问网站的请求时:
1. 使用browse_website工具访问指定网站
2. 提取关键内容信息，将HTML内容精简为主要文本内容
3. 整理内容后交回给Planner

不要尝试创作诗歌，这是PoetAgent的任务。你的职责是获取和整理网站内容。""",
)

# 3. 创建诗人代理 - 专门负责创作诗歌
poet_agent = AssistantAgent(
    name="PoetAgent",
    model_client=model_client,
    # 诗人代理只能将任务交回给规划者
    handoffs=["Planner"],
    system_message="""你是一位才华横溢的诗人，擅长将网页内容转化为优美的诗歌。
当你收到网页内容时:
1. 仔细分析内容的主题和情感
2. 创作一首优美、富有意境的诗歌，反映网站的核心内容
3. 确保诗歌有适当的结构和韵律
4. 将完成的诗歌交回给Planner

你的诗歌应该具有独特的风格和深度，能够打动读者。""",
)
```

#### 设置终止条件

```python
# 设置多种终止条件
# 1. 当Planner输出TERMINATE时终止
text_termination = TextMentionTermination("TERMINATE")

# 2. 最大消息数量限制(防止无限对话)
max_msg_termination = MaxMessageTermination(max_messages=15)

# 3. 对话超时限制(单位：秒)
timeout_termination = TimeoutTermination(timeout_seconds=180)  # 3分钟超时

# 组合终止条件：满足任一条件即终止
combined_termination = text_termination | max_msg_termination | timeout_termination
```

#### 创建Swarm团队

```python
# 创建Swarm团队
team = Swarm(
    participants=[planner, browser_agent, poet_agent],
    termination_condition=combined_termination,
)

# 运行团队
result = await Console(
    team.run_stream(
        task=TextMessage(content=request, source="user"),
        cancellation_token=CancellationToken(),
    )
)
```

## 4. 最佳实践与经验教训

### 4.1 代理设计原则

1. **专业分工**：每个代理应该专注于一项核心能力，避免"身兼数职"
   - BrowserAgent只负责网页浏览和内容提取
   - PoetAgent只负责诗歌创作
   - Planner负责协调和决策

2. **明确指令**：为每个代理提供清晰、具体的指令
   - 明确告知代理的职责范围
   - 列出具体的步骤和预期输出
   - 指明何时以及如何交接任务

3. **合理的交接路径**：设计合理的任务流转路径
   - Planner可以交接给所有专业代理
   - 专业代理只能交回给Planner
   - 避免形成循环或死锁

### 4.2 终止条件优化

1. **使用正确的终止条件类**：
   - 使用`TextMentionTermination`而非`TextMessageTermination`检测特定文本
   - 前者检查消息内容中是否包含指定文本
   - 后者只检查消息类型，不关心内容

2. **多重终止保障**：设置多种终止条件，防止系统陷入无限循环
   - 内容条件：关键词触发终止
   - 数量条件：最大消息数限制
   - 时间条件：超时限制

3. **将终止决策权交给Planner**：让协调者决定何时终止流程，而非由执行者决定

### 4.3 性能与质量提升

1. **控制消息数量**：适当增加最大消息数限制，但不宜过多
   - 单一代理：5条消息足够
   - 多代理Swarm：15条消息较为合理

2. **监控执行时间**：记录开始和结束时间，输出总耗时
   ```python
   start_time = asyncio.get_event_loop().time()
   result = await Console(team.run_stream(...))
   end_time = asyncio.get_event_loop().time()
   print(f"⏱️ 总耗时: {end_time - start_time:.2f}秒")
   ```

3. **输出终止原因**：了解系统是如何结束的
   ```python
   print(f"📊 终止原因: {result.stop_reason}")
   ```

## 5. 实际效果对比

### 5.1 单一代理系统

- **优点**：设置简单，代码量少
- **缺点**：诗歌质量一般，流程控制不够清晰，有时不按预期终止

### 5.2 多代理Swarm系统

- **优点**：
  - 任务分工明确，各司其职
  - 内容质量提升，每个代理都能专注于自己擅长的任务
  - 流程控制更加清晰，终止条件更可靠
  - 系统更具可扩展性，易于添加新的专业代理

- **缺点**：
  - 代码复杂度增加
  - 可能需要更多的消息交互，增加延迟
  - 需要更仔细地设计代理间的交互

## 6. 结论

通过将单一代理系统重构为多代理Swarm协作模式，我们成功提升了系统的质量和可靠性。关键改进包括：

1. 实现了代理间的专业分工，让每个代理专注于自己的优势领域
2. 优化了终止条件，使系统能够可靠地结束
3. 建立了清晰的任务流转路径，避免了混乱和循环

这种多代理Swarm模式适用于各种复杂任务，尤其是那些可以自然分解为多个专业步骤的任务。通过正确设计代理、交接机制和终止条件，可以构建出高效、可靠的AI协作系统。

## 7. 参考资料

- [AutoGen官方文档: Swarm模式](https://microsoft.github.io/autogen/docs/agentchat/groupchat_termination/)
- [AutoGen终止条件文档](https://microsoft.github.io/autogen/docs/agentchat/termination/) 