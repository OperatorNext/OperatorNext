# OperatorNext 前端项目 | AI 浏览器自动化的现代 Web 界面

<div align="center">

[![Built with Next.js](https://img.shields.io/badge/Built%20with-Next.js%2015-black?style=flat&logo=next.js)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue?style=flat&logo=typescript)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4-38B2AC?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![pnpm](https://img.shields.io/badge/pnpm-10.0-orange?style=flat&logo=pnpm)](https://pnpm.io)

*企业级 AI 浏览器自动化前端整体解决方案*

</div>

## 🌟 概述

OperatorNext 前端是一个使用前沿 Web 技术构建的现代化、类型安全的 monorepo 项目。它为 AI 驱动的浏览器自动化任务提供了流畅的用户界面和控制系统。

### 核心特性

- 🎨 **现代化 UI/UX** - 精美响应式界面，支持深色模式
- 🔄 **实时更新** - 基于 WebSocket 的任务监控和实时反馈
- 🌍 **国际化就绪** - 完整的中英文国际化支持
- 📱 **响应式设计** - 针对桌面端、平板和移动设备优化
- 🔒 **类型安全** - 基于 TypeScript 和 Prisma 的端到端类型安全
- 🚀 **高性能架构** - 采用 Next.js 15 App Router 和 React 服务器组件

## 🚀 快速开始

### 环境要求

- Node.js 18+ (推荐 LTS 版本)
- pnpm 10+
- Docker & Docker Compose（用于开发服务）

### 安装步骤

1. 安装依赖：
```bash
pnpm install
```

2. 设置环境变量：
```bash
cp .env.local.example .env.local
```

3. 初始化数据库并生成类型：
```bash
# 推送数据库架构
sudo pnpm db:push

# 生成 Prisma 客户端和类型
sudo pnpm db:generate
```

> 注意：根据您的系统配置，数据库操作可能需要 `sudo` 权限。

### 开发环境

启动开发服务器：
```bash
pnpm dev
```

这将启动以下服务：

| 服务 | 地址 | 用途 |
|---------|-----|---------|
| Next.js 应用 | http://localhost:3000 | 主应用界面 |
| PostgreSQL | localhost:5438 | 持久化存储数据库 |
| PgAdmin | http://localhost:5051 | 数据库管理界面 |
| MinIO | http://localhost:9002 | S3 兼容对象存储 |
| MinIO 控制台 | http://localhost:9003 | 存储管理界面 |
| Maildev | http://localhost:8026 | 邮件测试界面 |

### 本地开发最佳实践

#### 邮件服务配置
项目支持多个邮件提供商，可以通过环境变量进行配置：

```env
# 可选值: "nodemailer" | "resend" | "plunk" | "postmark" | "console" | "custom"
MAIL_PROVIDER="nodemailer"
```

本地开发环境：
- 使用 `nodemailer` 提供商配合 Maildev
- 在 `.env.local` 中配置：
  ```env
  MAIL_PROVIDER="nodemailer"
  MAIL_HOST="localhost"
  MAIL_PORT="1026"
  ```
- 访问 http://localhost:8026 查看发送的邮件

生产环境：
- 使用云邮件服务，如 Resend 或 Postmark
- 配置相应的提供商和 API 密钥
- Resend 配置示例：
  ```env
  MAIL_PROVIDER="resend"
  RESEND_API_KEY="your_api_key"
  ```

#### 存储服务配置
项目使用 S3 兼容的存储服务，可以针对本地开发和生产环境进行配置：

本地开发环境：
- 使用 MinIO 作为 S3 兼容存储
- 在 `.env.local` 中配置：
  ```env
  S3_ACCESS_KEY_ID="operatornext_storage_admin"
  S3_SECRET_ACCESS_KEY="your_secure_password"
  S3_ENDPOINT="http://localhost:9002"
  NEXT_PUBLIC_AVATARS_BUCKET_NAME="avatars"
  ```
- 访问 http://localhost:9003 管理存储服务

生产环境：
- 使用云存储服务（如 Supabase Storage、AWS S3）
- 配置相应的凭据和端点
- Supabase Storage 配置示例：
  ```env
  S3_ACCESS_KEY_ID="your_cloud_storage_key"
  S3_SECRET_ACCESS_KEY="your_cloud_storage_secret"
  S3_ENDPOINT="https://your-project.supabase.co/storage/v1/s3"
  ```

存储服务用于：
- 用户头像上传
- 文件附件
- 其他静态资源

注意：使用 Docker Compose 时，服务会自动配置正确的环境变量和网络设置。

## 📦 项目结构

```
frontend/
├── apps/
│   └── web/              # 主要的 Next.js 应用
│       ├── app/          # App Router 页面和布局
│       ├── modules/      # 基于功能的模块
│       ├── public/       # 静态资源
│       └── styles/       # 全局样式
├── packages/
│   ├── ai/              # AI 集成和模型
│   ├── api/             # API 路由和处理器
│   ├── auth/            # 身份认证和授权
│   ├── database/        # 数据库架构和迁移
│   ├── i18n/            # 国际化系统
│   ├── mail/            # 邮件模板和服务
│   ├── payments/        # 支付处理集成
│   └── ui/              # 共享 UI 组件库
└── tooling/             # 构建和开发工具
    ├── eslint/          # ESLint 配置
    ├── prettier/        # Prettier 配置
    └── typescript/      # TypeScript 配置
```

## 🛠 可用脚本

- `pnpm dev` - 启动开发环境
- `pnpm build` - 构建所有包和应用
- `pnpm lint` - 运行 ESLint 检查
- `pnpm format` - 使用 Prettier 格式化代码
- `pnpm test` - 运行测试套件
- `pnpm clean` - 清理构建产物
- `pnpm db:push` - 推送数据库架构变更
- `pnpm db:generate` - 生成 Prisma 客户端
- `pnpm db:studio` - 打开 Prisma Studio 界面

## 🔧 技术栈

### 核心技术
- Next.js 15 (App Router)
- React 19 (服务器组件)
- TypeScript 5.3
- Tailwind CSS 3.4

### 状态管理与数据
- Prisma ORM
- PostgreSQL
- MinIO (S3)
- Zustand

### UI 组件
- Shadcn UI
- Radix UI
- Framer Motion
- Lucide Icons

### 开发工具
- Turbo Repo
- ESLint
- Prettier
- Biome
- Husky

### 测试与质量
- Jest
- React Testing Library
- Playwright
- TypeScript 严格模式

## 📚 文档

详细文档请访问我们的[文档站点](https://github.com/OperatorNext/OperatorNext/tree/main/docs)。

## 🤝 参与贡献

请阅读我们的[贡献指南](../CONTRIBUTING.md)，了解代码规范和开发流程。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../LICENSE) 文件。 
