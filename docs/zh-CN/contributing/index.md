# 贡献指南

感谢您有兴趣为 OperatorNext 做出贡献！本指南将帮助您开始参与我们的项目。

## 行为准则

请阅读并遵守我们的[行为准则](CODE_OF_CONDUCT.md)，以帮助我们维护一个健康和友好的社区。

## 入门指南

### 环境要求

- Node.js 18+
- pnpm 10+
- Python 3.11+
- Docker & Docker Compose
- Git

### 开发环境设置

1. Fork 仓库
2. 克隆您的 fork：
```bash
git clone https://github.com/YOUR_USERNAME/OperatorNext.git
cd OperatorNext
```

3. 设置开发环境：
```bash
# 安装依赖
pnpm install

# 设置 pre-commit hooks
pre-commit install

# 复制环境文件
cp .env.example .env
cp frontend/.env.local.example frontend/.env.local

# 启动开发服务
docker-compose up -d
```

## 开发工作流

### 分支命名

- 功能：`feature/description`
- 修复：`fix/description`
- 文档：`docs/description`
- 性能：`perf/description`

### 提交消息

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
type(scope): description

[可选的正文]

[可选的页脚]
```

类型：
- `feat`：新功能
- `fix`：错误修复
- `docs`：文档更新
- `style`：代码风格变更
- `refactor`：代码重构
- `perf`：性能优化
- `test`：测试相关
- `chore`：维护任务

示例：
```
feat(auth): 添加 Google OAuth 支持

添加 Google OAuth 认证提供商，包含适当的错误处理
和用户资料同步。

Closes #123
```

### Pull Request 流程

1. 从 `main` 创建新分支
2. 进行更改
3. 运行测试和代码检查
4. 推送更改
5. 创建 pull request
6. 等待审查

## 代码风格

### TypeScript/JavaScript

遵循我们的 ESLint 和 Prettier 配置：

```bash
# 检查代码风格
pnpm lint

# 修复代码风格问题
pnpm format
```

主要规则：
- 使用 TypeScript
- 使用 2 个空格缩进
- 使用单引号
- 必须使用分号
- 最大行长度：100 字符

### Python

遵循我们的 Ruff 和 Black 配置：

```bash
# 检查代码风格
ruff check .

# 格式化代码
black .
```

主要规则：
- 使用类型提示
- 使用 4 个空格缩进
- 使用双引号
- 最大行长度：88 字符
- 遵循 PEP 8

## 测试

### 前端测试

```bash
# 运行单元测试
pnpm test

# 运行端到端测试
pnpm test:e2e

# 运行特定测试
pnpm test -t "测试名称"
```

### 后端测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_file.py -k "test_name"

# 运行覆盖率测试
pytest --cov=app
```

## 文档

### 编写文档

- 使用清晰简洁的语言
- 包含代码示例
- 提供步骤说明
- 为 UI 更改添加截图
- 保持文档更新

### 构建文档

```bash
# 安装文档依赖
pip install -r docs/requirements.txt

# 构建文档
mkdocs build

# 本地服务文档
mkdocs serve
```

## 提交更改

### 功能请求

1. 检查现有问题
2. 使用功能请求模板创建新问题
3. 与维护者讨论功能
4. 获得批准后开始实现

### 错误报告

1. 检查现有问题
2. 使用错误报告模板创建新问题
3. 包含：
   - 重现步骤
   - 预期行为
   - 实际行为
   - 环境详情
   - 相关截图

### Pull Requests

1. 引用相关问题
2. 描述您的更改
3. 包含测试覆盖
4. 更新文档
5. 添加到 CHANGELOG.md
6. 请求维护者审查

## 审查流程

### 代码审查

我们遵循以下原则：
- 保持尊重和建设性
- 关注代码，而不是个人
- 解释建议背后的原因
- 链接相关文档

### 审查清单

- [ ] 代码遵循风格指南
- [ ] 包含测试
- [ ] 文档已更新
- [ ] 提交消息清晰
- [ ] 更改范围适当
- [ ] 无安全漏洞
- [ ] 已考虑性能

## 发布流程

### 版本号

我们使用[语义化版本](https://semver.org/)：
- 主版本号：不兼容的 API 更改
- 次版本号：新功能
- 修订号：错误修复

### 发布步骤

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建发布分支
4. 运行测试和检查
5. 创建发布标签
6. 部署到预发环境
7. 部署到生产环境

## 社区

### 获取帮助

- [Discord 社区](https://discord.gg/operatornext)
- [GitHub 讨论区](https://github.com/OperatorNext/OperatorNext/discussions)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/operatornext)

### 交流渠道

- 技术讨论：GitHub 讨论区
- 实时聊天：Discord
- 错误报告：GitHub Issues
- 功能请求：GitHub Issues

## 其他资源

- [开发指南](../guides/development.md)
- [架构概览](../architecture/overview.md)
- [API 文档](../api/reference.md)
- [测试指南](testing.md)
- [风格指南](style-guide.md) 