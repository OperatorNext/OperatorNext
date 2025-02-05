# 部署指南

本指南提供了在各种环境中部署 OperatorNext 的详细说明。

## 部署选项

### 1. Docker Compose（推荐用于开发）

在本地或开发环境部署 OperatorNext 的最简单方式：

```bash
# 克隆仓库
git clone https://github.com/OperatorNext/OperatorNext.git
cd OperatorNext

# 复制环境文件
cp .env.example .env
cp frontend/.env.local.example frontend/.env.local

# 启动服务
docker-compose up -d
```

### 2. Kubernetes（推荐用于生产）

对于生产环境部署，我们推荐使用 Kubernetes：

```bash
# 应用 Kubernetes 配置
kubectl apply -f k8s/

# 验证部署
kubectl get pods -n operatornext
```

### 3. 云平台

支持的云平台：
- AWS（亚马逊云服务）
- GCP（谷歌云平台）
- Azure（微软云）
- Digital Ocean
- Vercel（前端）

## 环境要求

### 系统要求

- CPU：4 核以上
- 内存：8GB 以上
- 存储：20GB+ SSD
- 网络：100Mbps 以上

### 软件要求

- Docker 24+
- Docker Compose 2.x
- Node.js 18+
- pnpm 10+
- Python 3.11+

## 环境配置

### 生产环境变量

```env
# 应用配置
NODE_ENV=production
APP_ENV=production
DEBUG=false

# 数据库
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://host:6379

# 存储
S3_ENDPOINT=https://storage.example.com
S3_ACCESS_KEY_ID=your_access_key
S3_SECRET_ACCESS_KEY=your_secret_key

# 邮件
MAIL_PROVIDER=resend
RESEND_API_KEY=your_api_key

# 安全
BETTER_AUTH_SECRET=your_secure_secret
```

### SSL/TLS 配置

1. 生成证书：
```bash
certbot certonly --nginx -d your-domain.com
```

2. 配置 NGINX：
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # ... 其他配置
}
```

## 部署步骤

### 1. 数据库设置

```bash
# 创建生产数据库
createdb operatornext_production

# 运行迁移
pnpm db:migrate
```

### 2. 前端部署

```bash
# 构建前端
cd frontend
pnpm build

# 部署静态文件
pnpm deploy
```

### 3. 后端部署

```bash
# 安装生产依赖
pip install -r requirements.txt

# 启动后端服务
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. 反向代理设置

NGINX 配置示例：

```nginx
upstream frontend {
    server localhost:3000;
}

upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://frontend;
    }
    
    location /api {
        proxy_pass http://backend;
    }
    
    location /ws {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 监控和日志

### 系统监控

1. 安装 Prometheus：
```bash
helm install prometheus prometheus-community/prometheus
```

2. 安装 Grafana：
```bash
helm install grafana grafana/grafana
```

### 日志管理

1. 配置日志：
```yaml
logging:
  level: INFO
  format: json
  handlers:
    - type: file
      filename: /var/log/operatornext.log
    - type: syslog
      facility: local0
```

2. 设置日志轮转：
```conf
/var/log/operatornext.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

## 备份和恢复

### 数据库备份

1. 自动备份脚本：
```bash
#!/bin/bash
pg_dump -Fc operatornext_production > backup_$(date +%Y%m%d).dump
```

2. 配置备份计划：
```cron
0 2 * * * /path/to/backup.sh
```

### 存储备份

1. MinIO 备份：
```bash
mc mirror myminio/avatars backup/avatars
```

## 安全加固

### 防火墙配置

```bash
# 允许必要端口
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp

# 启用防火墙
ufw enable
```

### 安全头部

```nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-XSS-Protection "1; mode=block";
add_header X-Content-Type-Options "nosniff";
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Content-Security-Policy "default-src 'self';";
```

## 性能优化

### 缓存策略

1. Redis 缓存：
```typescript
const cache = new Redis({
  host: process.env.REDIS_HOST,
  port: parseInt(process.env.REDIS_PORT),
});
```

2. 静态文件缓存：
```nginx
location /static/ {
    expires 1y;
    add_header Cache-Control "public, no-transform";
}
```

### 数据库优化

1. 连接池：
```python
pool = await asyncpg.create_pool(
    dsn=DATABASE_URL,
    min_size=10,
    max_size=20
)
```

2. 查询优化：
```sql
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_task_status ON tasks(status);
```

## 故障排除

### 常见问题

1. **数据库连接问题**
   - 检查连接字符串
   - 验证网络连接
   - 检查防火墙规则

2. **邮件服务问题**
   - 验证 SMTP 设置
   - 检查 API 密钥
   - 监控邮件日志

3. **存储服务问题**
   - 验证 S3 凭据
   - 检查存储桶权限
   - 监控存储指标

### 健康检查

1. 服务健康端点：
```http
GET /api/health
```

2. 数据库健康检查：
```sql
SELECT 1;
```

## 其他资源

- [安全指南](security.md)
- [监控指南](monitoring.md)
- [备份流程](backup.md)
- [性能调优](performance.md) 