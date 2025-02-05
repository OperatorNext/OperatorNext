# Deployment Guide

This guide provides comprehensive instructions for deploying OperatorNext in various environments.

## Deployment Options

### 1. Docker Compose (Recommended for Development)

The simplest way to deploy OperatorNext locally or for development:

```bash
# Clone the repository
git clone https://github.com/OperatorNext/OperatorNext.git
cd OperatorNext

# Copy environment files
cp .env.example .env
cp frontend/.env.local.example frontend/.env.local

# Start services
docker-compose up -d
```

### 2. Kubernetes (Recommended for Production)

For production deployments, we recommend using Kubernetes:

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n operatornext
```

### 3. Cloud Platforms

Supported cloud platforms:
- AWS (Amazon Web Services)
- GCP (Google Cloud Platform)
- Azure
- Digital Ocean
- Vercel (Frontend)

## Prerequisites

### System Requirements

- CPU: 4+ cores
- RAM: 8GB+ minimum
- Storage: 20GB+ SSD
- Network: 100Mbps+

### Software Requirements

- Docker 24+
- Docker Compose 2.x
- Node.js 18+
- pnpm 10+
- Python 3.11+

## Environment Setup

### Production Environment Variables

```env
# Application
NODE_ENV=production
APP_ENV=production
DEBUG=false

# Database
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://host:6379

# Storage
S3_ENDPOINT=https://storage.example.com
S3_ACCESS_KEY_ID=your_access_key
S3_SECRET_ACCESS_KEY=your_secret_key

# Email
MAIL_PROVIDER=resend
RESEND_API_KEY=your_api_key

# Security
BETTER_AUTH_SECRET=your_secure_secret
```

### SSL/TLS Configuration

1. Generate certificates:
```bash
certbot certonly --nginx -d your-domain.com
```

2. Configure NGINX:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # ... other configurations
}
```

## Deployment Steps

### 1. Database Setup

```bash
# Create production database
createdb operatornext_production

# Run migrations
pnpm db:migrate
```

### 2. Frontend Deployment

```bash
# Build frontend
cd frontend
pnpm build

# Deploy static files
pnpm deploy
```

### 3. Backend Deployment

```bash
# Install production dependencies
pip install -r requirements.txt

# Start backend services
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Reverse Proxy Setup

Example NGINX configuration:

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

## Monitoring & Logging

### System Monitoring

1. Install Prometheus:
```bash
helm install prometheus prometheus-community/prometheus
```

2. Install Grafana:
```bash
helm install grafana grafana/grafana
```

### Log Management

1. Configure logging:
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

2. Set up log rotation:
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

## Backup & Recovery

### Database Backup

1. Automated backup script:
```bash
#!/bin/bash
pg_dump -Fc operatornext_production > backup_$(date +%Y%m%d).dump
```

2. Configure backup schedule:
```cron
0 2 * * * /path/to/backup.sh
```

### Storage Backup

1. MinIO backup:
```bash
mc mirror myminio/avatars backup/avatars
```

## Security Hardening

### Firewall Configuration

```bash
# Allow necessary ports
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp

# Enable firewall
ufw enable
```

### Security Headers

```nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-XSS-Protection "1; mode=block";
add_header X-Content-Type-Options "nosniff";
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Content-Security-Policy "default-src 'self';";
```

## Performance Optimization

### Caching Strategy

1. Redis caching:
```typescript
const cache = new Redis({
  host: process.env.REDIS_HOST,
  port: parseInt(process.env.REDIS_PORT),
});
```

2. Static file caching:
```nginx
location /static/ {
    expires 1y;
    add_header Cache-Control "public, no-transform";
}
```

### Database Optimization

1. Connection pooling:
```python
pool = await asyncpg.create_pool(
    dsn=DATABASE_URL,
    min_size=10,
    max_size=20
)
```

2. Query optimization:
```sql
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_task_status ON tasks(status);
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Check connection string
   - Verify network connectivity
   - Check firewall rules

2. **Email Service Issues**
   - Verify SMTP settings
   - Check API keys
   - Monitor email logs

3. **Storage Service Issues**
   - Verify S3 credentials
   - Check bucket permissions
   - Monitor storage metrics

### Health Checks

1. Service health endpoint:
```http
GET /api/health
```

2. Database health check:
```sql
SELECT 1;
```

## Additional Resources

- [Security Guidelines](security.md)
- [Monitoring Guide](monitoring.md)
- [Backup Procedures](backup.md)
- [Performance Tuning](performance.md) 