# OperatorNext 🤖

<div align="center">

<img src=".github/assets/brand/logo.png" alt="OperatorNext Logo" width="500"/>

[![GitHub license](https://img.shields.io/github/license/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/pulls)
[![Tests](https://github.com/OperatorNext/OperatorNext/actions/workflows/test.yml/badge.svg)](https://github.com/OperatorNext/OperatorNext/actions)

[English](./README.md) | [简体中文](./README.zh-CN.md)

---

**智能浏览器自动化平台**

*将自然语言转化为智能浏览器操作*

[快速开始](#-快速开始) • [项目文档](https://github.com/OperatorNext/OperatorNext/tree/main/docs) • [使用示例](#-使用示例) • [参与贡献](#-贡献指南)

</div>

OperatorNext 是一个基于 AI 的智能浏览器操作平台，它能够通过自然语言理解和执行复杂的浏览器任务。通过结合最新的 LLM 技术和浏览器自动化，我们为开发者和用户提供了一个强大的工具，能够轻松实现网页自动化、数据采集、UI 测试等多种场景的应用。

> ⚠️ **项目状态**
>
> 本项目目前处于早期开发阶段，核心功能正在积极开发中，尚未实现。
> 
> 请注意，在此阶段可能会频繁发生破坏性更改。

## ✨ 特性

- 🤖 **智能任务执行** - 通过自然语言描述即可完成复杂的浏览器操作
- 🔄 **实时状态反馈** - WebSocket 实时推送任务执行状态和进度
- 🎯 **精确控制** - 支持精确的 DOM 操作和复杂的交互场景
- 📊 **性能监控** - 内置系统资源监控，实时掌握任务执行情况
- 🔒 **安全可靠** - 完善的错误处理和异常恢复机制
- 🌐 **中文优化** - 完整的中文交互体验和错误提示

## 🚀 快速开始

### 环境要求

- Docker & Docker Compose
- Node.js 18+
- pnpm 10+
- Chrome/Chromium 浏览器

### 安装

1. 克隆仓库

```bash
git clone https://github.com/OperatorNext/OperatorNext.git
cd OperatorNext
```

2. 复制环境变量模板

```bash
# 复制前端环境变量
cp frontend/.env.local.example frontend/.env.local

# 复制 Docker 环境变量
cp .env.example .env
```

3. 安装前端依赖

```bash
cd frontend
pnpm install
```

4. 初始化数据库并生成类型

```bash
# 推送数据库架构
pnpm db:push

# 生成 Prisma 客户端和类型
pnpm db:generate
```

### 启动服务

1. 启动 Docker 服务

```bash
docker-compose up -d
```

这将启动以下服务：

| 服务 | 地址 | 描述 |
|---------|-----|-------------|
| Web 应用 | http://localhost:3000 | Next.js 前端应用 |
| PgAdmin | http://localhost:5051 | PostgreSQL 数据库管理 |
| Maildev | http://localhost:8026 | 邮件测试界面 |
| MinIO 控制台 | http://localhost:9003 | 对象存储管理 |
| MinIO API | http://localhost:9002 | S3 兼容 API 端点 |
| PostgreSQL | localhost:5438 | 数据库（通过 psql 或 GUI 连接） |

### 默认凭据

> ⚠️ 这些是开发环境凭据，请勿在生产环境中使用！

- **PostgreSQL**:
  - 用户名：operatornext_prod_user
  - 数据库：operatornext_production

- **PgAdmin**:
  - 邮箱：admin@operatornext.dev
  - 密码：见 `.env` 文件

- **MinIO**:
  - 访问密钥：见 `.env` 文件中的 `MINIO_ROOT_USER`
  - 密钥：见 `.env` 文件中的 `MINIO_ROOT_PASSWORD`

2. 启动前端开发服务器

```bash
cd frontend
pnpm dev
```

访问 http://localhost:3000 即可使用。

## 📖 使用示例

```python
# 创建一个新的浏览器任务
task = {
    "task_description": "登录GitHub并star一个项目"
}
response = requests.post("http://localhost:8000/api/tasks", json=task)
task_id = response.json()["task_id"]

# 通过WebSocket监听任务状态
ws = websockets.connect(f"ws://localhost:8000/ws/tasks/{task_id}")
```

更多示例请查看我们的[文档](https://github.com/OperatorNext/OperatorNext/tree/main/docs)。

## 🔧 技术架构

### 后端技术栈
- FastAPI
- WebSocket
- Playwright
- LangChain
- PostgreSQL
- MinIO

### 前端技术栈
- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- Shadcn UI
- Prisma
- Turbo Repo

## 📝 文档

详细文档请访问我们的[项目文档](https://github.com/OperatorNext/OperatorNext/tree/main/docs)。

## 🤝 贡献指南

我们欢迎所有形式的贡献，无论是新功能、文档改进还是问题反馈。请查看我们的 [贡献指南](CONTRIBUTING.md) 了解更多信息。

## 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

## 🙏 致谢

本项目受到以下项目的启发和技术支持：
- [browser-use](https://github.com/browser-use/browser-use)
- [browserless](https://github.com/browserless/browserless)

感谢所有为这个项目做出贡献的开发者们！

<div align="center">
  <img src="https://contrib.rocks/image?repo=OperatorNext/OperatorNext" />
</div>

## 🌟 Star History

<div align="center">
  <img src="https://api.star-history.com/svg?repos=OperatorNext/OperatorNext&type=Date" />
</div>

## 🗺️ 路线图

- [ ] **第一阶段：基础设施搭建** (进行中)
  - [x] Docker 环境配置
  - [x] 数据库架构设计
  - [ ] 身份认证系统
  - [ ] 基础 UI 组件

- [ ] **第二阶段：核心功能**
  - [ ] 用户管理和组织架构
  - [ ] 基于角色的访问控制 (RBAC)
  - [ ] AI 代理管理
  - [ ] 知识库集成

- [ ] **第三阶段：AI 功能**
  - [ ] LLM 集成
  - [ ] 提示词工程界面
  - [ ] 模型微调能力
  - [ ] 多模型编排

- [ ] **第四阶段：高级功能**
  - [ ] 实时协作
  - [ ] 高级分析和监控
  - [ ] API 集成能力
  - [ ] 自定义工作流构建器

## 📮 联系我们

- 提交 Issue: [GitHub Issues](https://github.com/OperatorNext/OperatorNext/issues)
- 邮件联系: hi@operatornext.com
- Telegram: [@HaiPro_2025](https://t.me/HaiPro_2025)
- 公司: CyberPoet LLC 