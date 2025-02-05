# OperatorNext 🤖

<div align="center">

<img src=".github/assets/brand/logo.png" alt="OperatorNext Logo" width="500"/>

[![GitHub license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/OperatorNext/OperatorNext/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/pulls)
[![Discord](https://img.shields.io/discord/1336375322379161661?logo=discord&logoColor=white)](https://discord.gg/zafb9TzYYA)
[![Version](https://img.shields.io/github/v/release/OperatorNext/OperatorNext?include_prereleases&label=version)](https://github.com/OperatorNext/OperatorNext/releases)

[English](./README.md) | [简体中文](./README.zh-CN.md)

---

**OpenAI Operator 的开源替代方案**

*基于大语言模型的智能浏览器自动化代理*

[快速开始](#-快速开始) • [项目文档](https://github.com/OperatorNext/OperatorNext/tree/main/docs) • [使用示例](#-使用示例) • [参与贡献](#-贡献指南) • [在线演示](https://operatornext.com)

</div>

OperatorNext 是一个开源的 AI 代理平台，通过自然语言处理和视觉推理来理解和执行复杂的浏览器任务。通过结合最先进的大语言模型技术（包括 GPT-4o、Claude 等）和浏览器自动化，我们为开发者和用户提供了一个强大的计算机使用代理（CUA），可用于网页自动化、数据采集、UI 测试等多种场景。

<div align="center">
  <p><strong>🖥️ 现代化界面与实时任务监控</strong></p>
  <img src=".github/assets/hero.png" alt="Operator Next Hero" width="100%" />
  
  <p><strong>🤖 智能任务执行与可视化反馈</strong></p>
  <img src=".github/assets/hero2.png" alt="Operator Next Screenshot" width="100%" />
</div>

> ⚠️ **项目状态**
>
> 本项目目前处于早期开发阶段，核心功能正在积极开发中，尚未实现。
> 
> 请注意，在此阶段可能会频繁发生破坏性更改。

### 🌟 为什么选择 OperatorNext？

| 特性 | OperatorNext | OpenAI Operator |
|---------|-------------|-----------------|
| 许可证 | MIT 开源 | 专有闭源 |
| 部署方式 | 自托管 + 云服务 | 仅云服务 |
| 数据隐私 | 本地处理 | 云端处理 |
| 定制能力 | 完全控制 | 受限 |
| 成本 | 免费且可自托管 | 按使用量计费 |
| API 集成 | 灵活开放 | 受限制 |

OperatorNext 为开发者提供：
- 🔍 **网页抓取与数据提取** - 像素级精确的自动数据采集
- 🧪 **端到端测试** - 现代化的 Selenium 替代方案，用于 UI/UX 测试
- 🤖 **RPA（机器人流程自动化）** - 基于链式思考的复杂任务规划
- 🌐 **Web 测试与质量保证** - 基于视觉推理的质量保证
- 📊 **数据挖掘与分析** - 具有自我纠正能力的智能网页数据采集
- 🔄 **工作流自动化** - 支持插件生态系统的自定义工作流设计

完美适用于：
- DevOps 和 QA 团队（自动化测试）
- 数据科学家和研究人员（网页抓取）
- 数字营销专业人士（表单自动化）
- 业务流程自动化（RPA 解决方案）
- Web 开发者和测试人员（GUI 测试）
- 企业自动化解决方案（自定义工作流）

## ✨ 特性

- 🤖 **AI 代理与视觉推理** - 通过自然语言和视觉理解完成复杂的浏览器操作，由 GPT-4o 多模态能力驱动
- 🧠 **链式思考规划** - 基于强化学习的高级任务规划和执行，实现最优自动化
- 🎯 **精确 GUI 交互** - 基于计算机视觉的像素级 DOM 操作、XPath 导航和复杂交互场景
- 📊 **实时任务追踪** - 基于 WebSocket 的监控系统，提供 CPU、内存和网络指标的执行洞察
- 🔒 **隐私优先设计** - 敏感数据本地处理，具备全面的错误处理和自我纠正机制
- 🌐 **跨平台多语言** - 完整的中英文界面支持，兼容 Windows、macOS 和 Linux
- 🔌 **可扩展架构** - REST API、WebSocket 端点和插件系统，实现无缝集成
- 🚀 **云端与自托管** - 可部署在自己的基础设施上或使用我们的云解决方案
- ⚡ **高性能设计** - 并行任务执行与优化资源管理
- 🎨 **现代开发体验** - 基于 Next.js 和 Tailwind CSS 构建的精美 UI/UX，提供详尽的 API 文档

## 🚀 快速开始

你可以在 [operatornext.com](https://operatornext.com) 体验在线演示，或按以下步骤部署自己的实例：

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
sudo pnpm db:push

# 生成 Prisma 客户端和类型
sudo pnpm db:generate
```

> 注意：根据您的系统配置，数据库操作可能需要 `sudo` 权限。

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
  - 密码：见 `.env`

## 🚀 技术栈

### AI 与自动化
- LLM 支持 - 兼容 GPT-4o、Claude 等多种大语言模型
- LangChain - 大型语言模型（LLM）编排框架
- 计算机视觉 - 像素级 DOM 交互和视觉分析
- 强化学习 - 自我改进的任务执行策略
- 链式思考 - 高级规划和决策制定

### 后端基础设施
- FastAPI - 用于构建可扩展 API 的高性能 Python Web 框架
- WebSocket - 用于任务监控的实时双向通信
- Playwright - 具有卓越稳定性的现代网页测试和自动化工具
- PostgreSQL - 用于任务管理的高级开源数据库
- MinIO - 用于工件管理的 S3 兼容对象存储
- Redis - 用于缓存和队列的内存数据结构存储
- Docker - 容器化和部署自动化

### 前端技术
- Next.js 15 (App Router) - 支持服务器端渲染的 React 框架
- React 19 - 具有并发特性和 Suspense 的最新版本
- TypeScript - 可靠的类型安全 JavaScript 开发
- Tailwind CSS - 用于现代 UI 的实用优先 CSS 框架
- Shadcn UI - 现代且无障碍的组件库
- Prisma - 用于类型安全数据库访问的下一代 ORM
- Turbo Repo - 高性能单体仓库构建系统
- WebSocket - 实时更新和任务监控
- Biome - 快速可靠的代码格式化工具

### DevOps 与质量
- Docker Compose - 多容器编排
- GitHub Actions - CI/CD 自动化流水线
- Playwright - 端到端测试框架
- Prisma - 数据库架构管理和迁移
- Biome - 代码质量和格式化工具
- pnpm - 快速且磁盘空间高效的包管理器

### 安全与隐私
- 本地处理 - 敏感数据处理
- 端到端加密 - 安全通信
- 基于角色的访问 - 细粒度权限
- 审计日志 - 全面的活动追踪

## 📮 联系与社区

加入我们不断成长的社区：

- [Discord](https://discord.gg/zafb9TzYYA) - 加入我们的社区，参与讨论、获取支持和更新
- [Slack](https://join.slack.com/t/operatornext/shared_invite/zt-2yzynnxiv-ywt7Z8UtykGAm6EUfpljQA) - 加入我们的 Slack 工作区进行团队协作
- [GitHub Issues](https://github.com/OperatorNext/OperatorNext/issues) - 问题报告和功能请求
- [GitHub Discussions](https://github.com/OperatorNext/OperatorNext/discussions) - 技术讨论和问题解答
- 电子邮件：hi@operatornext.com
- Telegram：[@HaiPro_2025](https://t.me/HaiPro_2025)

公司：CyberPoet LLC（职位：CEO）