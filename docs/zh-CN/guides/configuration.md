# 配置指南

本指南提供了 OperatorNext 在开发和生产环境下的详细配置信息。

## 环境变量

### 核心配置

```env
# 应用配置
APP_ENV=development  # development, staging, production
DEBUG=true
PORT=8000

# 站点 URL
NEXT_PUBLIC_SITE_URL="http://localhost:3000"

# 认证
BETTER_AUTH_SECRET="your_secure_auth_secret"
```

### 数据库配置

```env
# PostgreSQL
DATABASE_URL="postgresql://user:password@localhost:5438/operatornext"
POSTGRES_USER=operatornext_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=operatornext
POSTGRES_PORT=5438

# PgAdmin
PGADMIN_PORT=5051
PGADMIN_DEFAULT_EMAIL=admin@operatornext.dev
PGADMIN_DEFAULT_PASSWORD=your_secure_password
```

### 邮件服务配置

系统支持多个邮件提供商：

```env
# 可用提供商: "nodemailer" | "resend" | "plunk" | "postmark" | "console" | "custom"
MAIL_PROVIDER="nodemailer"

# Nodemailer (本地开发)
MAIL_HOST="localhost"
MAIL_PORT="1026"
MAIL_USER=""  # 生产环境必需
MAIL_PASS=""  # 生产环境必需

# Resend
RESEND_API_KEY="your_resend_api_key"

# Plunk
PLUNK_API_KEY="your_plunk_api_key"

# Postmark
POSTMARK_SERVER_TOKEN="your_postmark_token"
```

### 存储服务配置

```env
# MinIO 配置
MINIO_ROOT_USER=operatornext_storage_admin
MINIO_ROOT_PASSWORD=your_secure_password
MINIO_API_PORT=9002
MINIO_CONSOLE_PORT=9003

# S3 客户端配置
S3_ACCESS_KEY_ID="operatornext_storage_admin"
S3_SECRET_ACCESS_KEY="your_secure_password"
S3_ENDPOINT="http://localhost:9002"
NEXT_PUBLIC_AVATARS_BUCKET_NAME="avatars"
```

### OAuth 配置

```env
# GitHub OAuth
GITHUB_CLIENT_ID="your_github_client_id"
GITHUB_CLIENT_SECRET="your_github_client_secret"

# Google OAuth
GOOGLE_CLIENT_ID="your_google_client_id"
GOOGLE_CLIENT_SECRET="your_google_client_secret"
```

### 浏览器自动化配置

```env
# Chrome 配置
CHROME_OPTS="--remote-debugging-port=9222 --remote-debugging-address=0.0.0.0 --no-sandbox"
CHROME_PERSISTENT_SESSION=true
BROWSERLESS_URL="http://localhost:13000"
BROWSERLESS_TOKEN="your_secure_browser_token"
BROWSERLESS_TIMEOUT=300000
```

## 服务配置

### 邮件服务

系统支持多个邮件提供商，具有不同的配置要求：

1. **Nodemailer (开发环境)**
   - 仅需要 `MAIL_HOST` 和 `MAIL_PORT`
   - 配合 Maildev 进行本地测试

2. **Nodemailer (生产环境)**
   - 需要完整的 SMTP 配置
   - 包含认证凭据

3. **云服务提供商**
   - Resend：仅需要 API 密钥
   - Plunk：仅需要 API 密钥
   - Postmark：仅需要服务器令牌

### 存储服务

两种主要配置选项：

1. **本地开发 (MinIO)**
   ```env
   S3_ENDPOINT="http://localhost:9002"
   S3_ACCESS_KEY_ID="operatornext_storage_admin"
   S3_SECRET_ACCESS_KEY="your_secure_password"
   ```

2. **生产环境 (云存储)**
   ```env
   S3_ENDPOINT="https://your-storage-service.com"
   S3_ACCESS_KEY_ID="your_cloud_storage_key"
   S3_SECRET_ACCESS_KEY="your_cloud_storage_secret"
   ```

## 安全注意事项

### 认证

- 为所有密钥使用强大且唯一的值
- 在生产环境中定期轮换密钥
- 使用环境特定的密钥

### 数据库

- 使用强密码
- 限制数据库访问权限
- 在生产环境中启用 SSL

### 存储

- 设置适当的存储桶策略
- 为不同环境使用独立的凭据
- 启用静态加密

## 环境特定配置

### 开发环境

```env
APP_ENV=development
DEBUG=true
MAIL_PROVIDER=nodemailer
```

### 预发环境

```env
APP_ENV=staging
DEBUG=false
MAIL_PROVIDER=resend
```

### 生产环境

```env
APP_ENV=production
DEBUG=false
MAIL_PROVIDER=resend
```

## 验证和故障排除

### 配置验证

系统在启动时验证配置：

1. **邮件提供商**
   - 检查必需的凭据
   - 如果无效则回退到控制台提供商

2. **存储服务**
   - 验证 S3 凭据
   - 检查存储桶可访问性

3. **数据库**
   - 验证连接字符串
   - 检查架构版本

### 常见问题

1. **邮件配置**
   - 检查提供商特定要求
   - 验证端口可访问性
   - 检查凭据格式

2. **存储配置**
   - 验证端点 URL 格式
   - 检查凭据权限
   - 确保存储桶存在

3. **数据库配置**
   - 检查连接字符串格式
   - 验证主机可访问性
   - 确认用户权限

## 最佳实践

1. **环境变量**
   - 使用 `.env.local` 进行本地覆盖
   - 永远不要提交敏感值
   - 为每个环境使用不同的值

2. **密钥管理**
   - 使用安全的密钥管理系统
   - 定期轮换凭据
   - 限制生产环境密钥的访问

3. **配置更新**
   - 记录所有配置更改
   - 在预发环境中先测试更改
   - 使用配置版本控制

## 其他资源

- [环境变量参考](../reference/env-vars.md)
- [安全指南](../deployment/security.md)
- [生产环境部署指南](../deployment/production.md) 