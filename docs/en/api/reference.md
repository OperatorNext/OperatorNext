# API Reference

This document provides detailed information about the OperatorNext API endpoints, request/response formats, and authentication methods.

## Authentication

### OAuth Authentication

```http
POST /api/auth/oauth
Content-Type: application/json

{
  "provider": "github",
  "code": "oauth_code"
}
```

### Email/Password Authentication

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

### Token Refresh

```http
POST /api/auth/refresh
Authorization: Bearer refresh_token
```

## Browser Automation

### Create Browser Task

```http
POST /api/browser/tasks
Content-Type: application/json
Authorization: Bearer access_token

{
  "task_description": "Login to GitHub and star a repository",
  "options": {
    "headless": true,
    "timeout": 30000
  }
}
```

### Get Task Status

```http
GET /api/browser/tasks/{task_id}
Authorization: Bearer access_token
```

### Cancel Task

```http
POST /api/browser/tasks/{task_id}/cancel
Authorization: Bearer access_token
```

### WebSocket Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/tasks/{task_id}');
```

## User Management

### Create User

```http
POST /api/users
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "John Doe"
}
```

### Update User Profile

```http
PATCH /api/users/{user_id}
Content-Type: application/json
Authorization: Bearer access_token

{
  "name": "John Smith",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

### Upload Avatar

```http
POST /api/users/avatar
Content-Type: multipart/form-data
Authorization: Bearer access_token

file: <avatar_file>
```

## Storage Management

### Get Upload URL

```http
POST /api/storage/upload-url
Content-Type: application/json
Authorization: Bearer access_token

{
  "filename": "example.jpg",
  "content_type": "image/jpeg"
}
```

### List Files

```http
GET /api/storage/files
Authorization: Bearer access_token
```

## Response Formats

### Success Response

```json
{
  "success": true,
  "data": {
    "id": "123",
    "created_at": "2024-02-20T12:00:00Z"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

## WebSocket Events

### Task Status Updates

```json
{
  "type": "status",
  "data": {
    "status": "running",
    "progress": 50,
    "current_step": "Navigating to page"
  }
}
```

### Task Completion

```json
{
  "type": "complete",
  "data": {
    "result": {
      "success": true,
      "message": "Task completed successfully"
    }
  }
}
```

### Task Error

```json
{
  "type": "error",
  "data": {
    "code": "NAVIGATION_ERROR",
    "message": "Failed to navigate to page"
  }
}
```

## Rate Limiting

The API implements rate limiting based on the following rules:

- Authentication endpoints: 5 requests per minute
- Browser automation endpoints: 10 requests per minute
- User management endpoints: 30 requests per minute
- Storage endpoints: 100 requests per minute

Rate limit headers are included in all responses:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1582188300
```

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_CREDENTIALS` | Invalid email or password |
| `TOKEN_EXPIRED` | Authentication token has expired |
| `INSUFFICIENT_PERMISSIONS` | User lacks required permissions |
| `RESOURCE_NOT_FOUND` | Requested resource does not exist |
| `VALIDATION_ERROR` | Request payload validation failed |
| `RATE_LIMIT_EXCEEDED` | Too many requests |

## SDK Examples

### JavaScript/TypeScript

```typescript
import { OperatorNext } from '@operatornext/sdk';

const client = new OperatorNext({
  apiKey: 'your_api_key',
  endpoint: 'https://api.operatornext.com'
});

// Create a browser task
const task = await client.browser.createTask({
  description: 'Login to GitHub',
  options: { headless: true }
});

// Monitor task status
client.browser.onTaskUpdate(task.id, (status) => {
  console.log('Task status:', status);
});
```

### Python

```python
from operatornext import OperatorNext

client = OperatorNext(
    api_key='your_api_key',
    endpoint='https://api.operatornext.com'
)

# Create a browser task
task = client.browser.create_task(
    description='Login to GitHub',
    options={'headless': True}
)

# Monitor task status
for status in client.browser.monitor_task(task.id):
    print('Task status:', status)
```

## Additional Resources

- [API Changelog](changelog.md)
- [Authentication Guide](../guides/authentication.md)
- [Browser Automation Guide](../guides/browser-automation.md)
- [SDK Documentation](../sdk/index.md) 