# API 参考文档

本文档提供了 OperatorNext API 端点、请求/响应格式和认证方法的详细信息。

## 认证

### OAuth 认证

```http
POST /api/auth/oauth
Content-Type: application/json

{
  "provider": "github",
  "code": "oauth_code"
}
```

### 邮箱/密码认证

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

### 令牌刷新

```http
POST /api/auth/refresh
Authorization: Bearer refresh_token
```

## 浏览器自动化

### 创建浏览器任务

```http
POST /api/browser/tasks
Content-Type: application/json
Authorization: Bearer access_token

{
  "task_description": "登录 GitHub 并为仓库点星标",
  "options": {
    "headless": true,
    "timeout": 30000
  }
}
```

### 获取任务状态

```http
GET /api/browser/tasks/{task_id}
Authorization: Bearer access_token
```

### 取消任务

```http
POST /api/browser/tasks/{task_id}/cancel
Authorization: Bearer access_token
```

### WebSocket 连接

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/tasks/{task_id}');
```

## 用户管理

### 创建用户

```http
POST /api/users
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "张三"
}
```

### 更新用户资料

```http
PATCH /api/users/{user_id}
Content-Type: application/json
Authorization: Bearer access_token

{
  "name": "李四",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

### 上传头像

```http
POST /api/users/avatar
Content-Type: multipart/form-data
Authorization: Bearer access_token

file: <avatar_file>
```

## 存储管理

### 获取上传 URL

```http
POST /api/storage/upload-url
Content-Type: application/json
Authorization: Bearer access_token

{
  "filename": "example.jpg",
  "content_type": "image/jpeg"
}
```

### 列出文件

```http
GET /api/storage/files
Authorization: Bearer access_token
```

## 响应格式

### 成功响应

```json
{
  "success": true,
  "data": {
    "id": "123",
    "created_at": "2024-02-20T12:00:00Z"
  }
}
```

### 错误响应

```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "邮箱或密码无效"
  }
}
```

## WebSocket 事件

### 任务状态更新

```json
{
  "type": "status",
  "data": {
    "status": "running",
    "progress": 50,
    "current_step": "正在导航到页面"
  }
}
```

### 任务完成

```json
{
  "type": "complete",
  "data": {
    "result": {
      "success": true,
      "message": "任务成功完成"
    }
  }
}
```

### 任务错误

```json
{
  "type": "error",
  "data": {
    "code": "NAVIGATION_ERROR",
    "message": "导航到页面失败"
  }
}
```

## 速率限制

API 基于以下规则实施速率限制：

- 认证端点：每分钟 5 个请求
- 浏览器自动化端点：每分钟 10 个请求
- 用户管理端点：每分钟 30 个请求
- 存储端点：每分钟 100 个请求

所有响应中都包含速率限制头：

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1582188300
```

## 错误代码

| 代码 | 描述 |
|------|------|
| `INVALID_CREDENTIALS` | 邮箱或密码无效 |
| `TOKEN_EXPIRED` | 认证令牌已过期 |
| `INSUFFICIENT_PERMISSIONS` | 用户缺少所需权限 |
| `RESOURCE_NOT_FOUND` | 请求的资源不存在 |
| `VALIDATION_ERROR` | 请求载荷验证失败 |
| `RATE_LIMIT_EXCEEDED` | 请求过于频繁 |

## SDK 示例

### JavaScript/TypeScript

```typescript
import { OperatorNext } from '@operatornext/sdk';

const client = new OperatorNext({
  apiKey: 'your_api_key',
  endpoint: 'https://api.operatornext.com'
});

// 创建浏览器任务
const task = await client.browser.createTask({
  description: '登录 GitHub',
  options: { headless: true }
});

// 监控任务状态
client.browser.onTaskUpdate(task.id, (status) => {
  console.log('任务状态:', status);
});
```

### Python

```python
from operatornext import OperatorNext

client = OperatorNext(
    api_key='your_api_key',
    endpoint='https://api.operatornext.com'
)

# 创建浏览器任务
task = client.browser.create_task(
    description='登录 GitHub',
    options={'headless': True}
)

# 监控任务状态
for status in client.browser.monitor_task(task.id):
    print('任务状态:', status)
```

## 其他资源

- [API 更新日志](changelog.md)
- [认证指南](../guides/authentication.md)
- [浏览器自动化指南](../guides/browser-automation.md)
- [SDK 文档](../sdk/index.md) 