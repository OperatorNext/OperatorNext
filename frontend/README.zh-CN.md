# OperatorNext 前端项目

这是 OperatorNext 的前端 monorepo 项目，使用 Next.js 15、TypeScript 和 Tailwind CSS 构建。

## 🚀 快速开始

### 环境要求

- Node.js 18+
- pnpm 10+
- Docker（用于开发服务）

### 安装

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
pnpm db:push

# 生成 Prisma 客户端和类型
pnpm db:generate
```

### 开发

启动开发服务器：
```bash
pnpm dev
```

这将启动以下服务：
- Next.js 应用：http://localhost:3000
- 数据库：端口 5438
- PgAdmin 管理界面：http://localhost:5051
- MinIO 对象存储：http://localhost:9002（控制台：http://localhost:9003）
- Maildev 邮件服务：http://localhost:8026

## 📦 项目结构

```
frontend/
├── apps/
│   └── web/          # 主要的 Next.js 应用
├── packages/
│   ├── ai/           # AI 相关功能
│   ├── api/          # API 路由和处理器
│   ├── auth/         # 认证逻辑
│   ├── database/     # 数据库架构和类型
│   ├── i18n/         # 国际化
│   ├── mail/         # 邮件模板和发送
│   ├── payments/     # 支付处理
│   └── ui/           # 共享 UI 组件
└── tooling/          # 开发工具和配置
```

## 🛠 可用脚本

- `pnpm dev` - 启动开发服务器
- `pnpm build` - 生产环境构建
- `pnpm db:push` - 推送数据库架构变更
- `pnpm db:generate` - 生成 Prisma 客户端和类型
- `pnpm db:studio` - 打开 Prisma Studio
- `pnpm seed` - 填充数据库种子数据
- `pnpm lint` - 运行代码检查
- `pnpm format` - 格式化代码
- `pnpm clean` - 清理构建文件

## 🔧 技术栈

- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- Shadcn UI
- Prisma
- PostgreSQL
- MinIO
- Turbo Repo

## 📚 文档

详细文档请访问我们的[文档站点](https://github.com/OperatorNext/OperatorNext/tree/main/docs)。 
