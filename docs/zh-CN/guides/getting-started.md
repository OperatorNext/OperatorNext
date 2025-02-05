# OperatorNext 快速开始指南

本指南将帮助您开始使用 OperatorNext，这是一个企业级 AI 浏览器自动化平台。

## 环境要求

开始之前，请确保已安装以下软件：

- Node.js 18+ (推荐 LTS 版本)
- pnpm 10+
- Docker & Docker Compose
- Git

## 快速安装

1. 克隆仓库：
```bash
git clone https://github.com/OperatorNext/OperatorNext.git
cd OperatorNext
```

2. 安装依赖：
```bash
pnpm install
```

3. 设置环境变量：
```bash
cp .env.local.example .env.local
```

4. 初始化数据库：
```bash
# 推送数据库架构
sudo pnpm db:push

# 生成 Prisma 客户端和类型
sudo pnpm db:generate
```

## 开发环境

启动开发服务器：
```bash
pnpm dev
```

这将启动所有必需的服务：

| 服务 | 地址 | 用途 |
|---------|-----|---------|
| Next.js 应用 | http://localhost:3000 | 主应用界面 |
| PostgreSQL | localhost:5438 | 持久化存储数据库 |
| PgAdmin | http://localhost:5051 | 数据库管理界面 |
| MinIO | http://localhost:9002 | S3 兼容对象存储 |
| MinIO 控制台 | http://localhost:9003 | 存储管理界面 |
| Maildev | http://localhost:8026 | 邮件测试界面 |

## 配置说明

### 邮件服务

在 `.env.local` 中配置邮件服务：

```env
# 可用提供商: "nodemailer" | "resend" | "plunk" | "postmark" | "console" | "custom"
MAIL_PROVIDER="nodemailer"

# 本地开发配置
MAIL_HOST="localhost"
MAIL_PORT="1026"
```

### 存储服务

在 `.env.local` 中配置存储服务：

```env
# 本地开发使用 MinIO
S3_ACCESS_KEY_ID="operatornext_storage_admin"
S3_SECRET_ACCESS_KEY="your_secure_password"
S3_ENDPOINT="http://localhost:9002"
NEXT_PUBLIC_AVATARS_BUCKET_NAME="avatars"
```

## 验证安装

1. 在浏览器中打开 http://localhost:3000
2. 注册新账户
3. 在 http://localhost:8026 查看验证邮件
4. 完成邮件验证流程

## 下一步

- [配置指南](configuration.md) - 了解所有配置选项
- [使用手册](user-guide.md) - 学习如何使用 OperatorNext
- [开发指南](development.md) - 学习如何进行开发
- [API 文档](../api/reference.md) - 浏览 API 文档

## 故障排除

### 常见问题

1. **数据库连接问题**
   - 确保 PostgreSQL 正在运行：`docker ps | grep postgres`
   - 检查数据库日志：`docker-compose logs db`

2. **邮件服务问题**
   - 验证 Maildev 是否运行：`docker ps | grep maildev`
   - 检查 Maildev 界面：http://localhost:8026

3. **存储服务问题**
   - 确保 MinIO 正在运行：`docker ps | grep minio`
   - 检查 MinIO 控制台：http://localhost:9003

### 获取帮助

- 查看我们的[常见问题](faq.md)
- 加入我们的 [Discord 社区](https://discord.gg/operatornext)
- 在 [GitHub](https://github.com/OperatorNext/OperatorNext/issues) 上提交问题

## 安全注意事项

- 永远不要提交 `.env.local` 文件
- 为所有服务使用强密码
- 保持依赖包的更新
- 遵循我们的[安全指南](../deployment/security.md) 