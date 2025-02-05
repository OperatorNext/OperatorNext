# 安全指南

本文档概述了 OperatorNext 开发和部署的安全最佳实践和要求。

## 安全原则

### 核心原则

1. **纵深防御**
   - 多层安全控制
   - 避免单点故障
   - 全面的安全方法

2. **最小权限**
   - 最小必要权限
   - 基于角色的访问控制
   - 定期访问审查

3. **默认安全**
   - 安全优先配置
   - 安全的默认设置
   - 明确的安全决策

## 认证与授权

### 用户认证

1. **密码要求**
   ```typescript
   const passwordRequirements = {
     minLength: 12,
     requireUppercase: true,
     requireLowercase: true,
     requireNumbers: true,
     requireSpecialChars: true,
     maxAge: 90 // 天数
   };
   ```

2. **多因素认证**
   - 管理员账户必需
   - 普通用户可选
   - 支持 TOTP 和 WebAuthn

3. **会话管理**
   ```typescript
   const sessionConfig = {
     maxAge: '24h',
     secure: true,
     httpOnly: true,
     sameSite: 'strict'
   };
   ```

### OAuth 安全

1. **提供商配置**
   ```typescript
   const oauthConfig = {
     allowedProviders: ['github', 'google'],
     enforceHttps: true,
     validateRedirectUri: true,
     stateValidation: true
   };
   ```

2. **令牌处理**
   - 安全令牌存储
   - 定期令牌轮换
   - 令牌验证

## 数据安全

### 加密

1. **静态数据加密**
   ```python
   from cryptography.fernet import Fernet
   
   def encrypt_sensitive_data(data: str) -> str:
       key = Fernet.generate_key()
       f = Fernet(key)
       return f.encrypt(data.encode())
   ```

2. **传输中的数据**
   - 要求 TLS 1.3
   - 强密码套件
   - 证书验证

### 数据库安全

1. **连接安全**
   ```python
   db_config = {
       'ssl_mode': 'verify-full',
       'ssl_ca': '/path/to/ca.pem',
       'ssl_cert': '/path/to/client-cert.pem',
       'ssl_key': '/path/to/client-key.pem'
   }
   ```

2. **查询安全**
   ```typescript
   // 使用参数化查询
   const user = await db.query(
     'SELECT * FROM users WHERE id = $1',
     [userId]
   );
   ```

## API 安全

### 请求验证

1. **输入净化**
   ```typescript
   function sanitizeInput(input: string): string {
     return input
       .replace(/[<>]/g, '')
       .trim()
       .slice(0, MAX_LENGTH);
   }
   ```

2. **速率限制**
   ```typescript
   const rateLimitConfig = {
     window: '15m',
     max: 100,
     standardHeaders: true,
     skipFailedRequests: false
   };
   ```

### 响应安全

1. **安全头部**
   ```nginx
   add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
   add_header X-Content-Type-Options "nosniff" always;
   add_header X-Frame-Options "SAMEORIGIN" always;
   add_header Content-Security-Policy "default-src 'self';" always;
   ```

2. **错误处理**
   ```typescript
   function handleError(error: Error): ApiResponse {
     return {
       success: false,
       error: {
         code: error.code,
         message: sanitizeErrorMessage(error.message)
       }
     };
   }
   ```

## 基础设施安全

### 容器安全

1. **镜像安全**
   ```dockerfile
   # 使用特定版本
   FROM node:18.19-alpine
   
   # 以非 root 用户运行
   USER node
   
   # 最小化攻击面
   COPY --chown=node:node . .
   ```

2. **运行时安全**
   ```yaml
   securityContext:
     runAsNonRoot: true
     readOnlyRootFilesystem: true
     allowPrivilegeEscalation: false
   ```

### 网络安全

1. **防火墙规则**
   ```bash
   # 只允许必要端口
   ufw default deny incoming
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw enable
   ```

2. **网络策略**
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: default-deny
   spec:
     podSelector: {}
     policyTypes:
     - Ingress
     - Egress
   ```

## 监控和日志

### 安全监控

1. **审计日志**
   ```typescript
   interface AuditLog {
     timestamp: Date;
     actor: string;
     action: string;
     resource: string;
     status: string;
     details: Record<string, unknown>;
   }
   ```

2. **告警配置**
   ```yaml
   alerts:
     - name: suspicious_login
       condition: login_failures > 5
       window: 5m
       actions:
         - notify_security_team
         - block_ip_temporarily
   ```

### 事件响应

1. **响应计划**
   - 事件分类
   - 响应程序
   - 沟通计划
   - 恢复步骤

2. **安全联系人**
   ```yaml
   security_contacts:
     primary:
       name: 安全团队
       email: security@operatornext.com
       phone: +1-XXX-XXX-XXXX
     escalation:
       name: 技术总监
       email: cto@operatornext.com
   ```

## 合规和审计

### 安全扫描

1. **代码扫描**
   ```yaml
   name: 安全扫描
   on:
     push:
       branches: [main]
   jobs:
     security:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: 运行安全扫描
           run: |
             pnpm audit
             safety check
   ```

2. **依赖扫描**
   ```bash
   # 检查 npm 依赖
   pnpm audit
   
   # 检查 Python 依赖
   safety check
   ```

### 合规检查

1. **配置验证**
   ```typescript
   function validateSecurityConfig(): ValidationResult {
     return {
       tlsVersion: checkTlsVersion(),
       cipherSuites: checkCipherSuites(),
       securityHeaders: checkSecurityHeaders(),
       authConfig: checkAuthConfig()
     };
   }
   ```

2. **安全报告**
   ```python
   def generate_security_report():
       return {
           'last_scan': datetime.now(),
           'vulnerabilities': scan_vulnerabilities(),
           'compliance_status': check_compliance(),
           'recommendations': get_security_recommendations()
       }
   ```

## 其他资源

- [OWASP Top 10](https://owasp.org/Top10/)
- [安全检查清单](checklist.md)
- [事件响应计划](incident-response.md)
- [安全最佳实践](best-practices.md)
- [合规要求](compliance.md) 