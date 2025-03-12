# AutoGen 实验 🤖

这个目录包含了使用 AutoGen SDK 的各种实验和示例。AutoGen 是一个强大的框架，支持构建多智能体对话和自动化系统。

## 功能特性

- 🤖 多智能体对话系统
- 🔄 自动化工作流程
- 🛠️ 自定义智能体行为
- 📝 对话历史管理
- 🎯 任务规划与执行

## 目录结构

```
autogen/
├── src/              # 核心实现
│   ├── config.py     # 配置管理
│   └── agents.py     # 智能体定义
│
├── examples/         # 使用示例
│   └── basic_chat.py # 基础对话示例
│
└── tests/           # 测试用例
    └── test_agents.py
```

## 快速开始

1. 设置环境变量：
```bash
export OPENAI_API_KEY="your-api-key"
```

2. 运行基础示例：
```bash
python -m labs.autogen.examples.basic_chat
```

## 示例说明

### 基础对话

```python
from labs.autogen.src.agents import create_assistant, create_user_proxy

# 创建智能体
assistant = create_assistant("AI助手")
user_proxy = create_user_proxy("用户")

# 开始对话
user_proxy.initiate_chat(
    assistant,
    message="你好，请帮我写一个Python函数来计算斐波那契数列"
)
```

## 配置说明

在 `src/config.py` 中可以自定义以下配置：

- 模型选择（GPT-4、GPT-3.5等）
- 温度和其他生成参数
- 智能体行为设置
- 对话历史记录设置

## 测试

运行测试：
```bash
pytest labs/autogen/tests/
```

## 注意事项

1. 请确保正确设置 API 密钥
2. 建议在开发时使用较低成本的模型
3. 对话历史会被保存在内存中
4. 长时间运行请注意资源管理

## 参考资料

- [AutoGen 官方文档](https://microsoft.github.io/autogen/)
- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [项目 Wiki](https://github.com/OperatorNext/OperatorNext/wiki) 