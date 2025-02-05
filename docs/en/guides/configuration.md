# Configuration Guide

This guide provides detailed information about configuring OperatorNext for both development and production environments.

## Environment Variables

### Core Configuration

```env
# Application
APP_ENV=development  # development, staging, production
DEBUG=true
PORT=8000

# Site URL
NEXT_PUBLIC_SITE_URL="http://localhost:3000"

# Authentication
BETTER_AUTH_SECRET="your_secure_auth_secret"
```

### Database Configuration

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

### Email Service Configuration

The system supports multiple email providers:

```env
# Available providers: "nodemailer" | "resend" | "plunk" | "postmark" | "console" | "custom"
MAIL_PROVIDER="nodemailer"

# Nodemailer (Local Development)
MAIL_HOST="localhost"
MAIL_PORT="1026"
MAIL_USER=""  # Required in production
MAIL_PASS=""  # Required in production

# Resend
RESEND_API_KEY="your_resend_api_key"

# Plunk
PLUNK_API_KEY="your_plunk_api_key"

# Postmark
POSTMARK_SERVER_TOKEN="your_postmark_token"
```

### Storage Service Configuration

```env
# MinIO Configuration
MINIO_ROOT_USER=operatornext_storage_admin
MINIO_ROOT_PASSWORD=your_secure_password
MINIO_API_PORT=9002
MINIO_CONSOLE_PORT=9003

# S3 Client Configuration
S3_ACCESS_KEY_ID="operatornext_storage_admin"
S3_SECRET_ACCESS_KEY="your_secure_password"
S3_ENDPOINT="http://localhost:9002"
NEXT_PUBLIC_AVATARS_BUCKET_NAME="avatars"
```

### OAuth Configuration

```env
# GitHub OAuth
GITHUB_CLIENT_ID="your_github_client_id"
GITHUB_CLIENT_SECRET="your_github_client_secret"

# Google OAuth
GOOGLE_CLIENT_ID="your_google_client_id"
GOOGLE_CLIENT_SECRET="your_google_client_secret"
```

### Browser Automation Configuration

```env
# Chrome Configuration
CHROME_OPTS="--remote-debugging-port=9222 --remote-debugging-address=0.0.0.0 --no-sandbox"
CHROME_PERSISTENT_SESSION=true
BROWSERLESS_URL="http://localhost:13000"
BROWSERLESS_TOKEN="your_secure_browser_token"
BROWSERLESS_TIMEOUT=300000
```

## Service Configuration

### Email Service

The system supports multiple email providers with different configuration requirements:

1. **Nodemailer (Development)**
   - Only requires `MAIL_HOST` and `MAIL_PORT`
   - Works with Maildev for local testing

2. **Nodemailer (Production)**
   - Requires full SMTP configuration
   - Includes authentication credentials

3. **Cloud Providers**
   - Resend: Only requires API key
   - Plunk: Only requires API key
   - Postmark: Only requires server token

### Storage Service

Two main configuration options:

1. **Local Development (MinIO)**
   ```env
   S3_ENDPOINT="http://localhost:9002"
   S3_ACCESS_KEY_ID="operatornext_storage_admin"
   S3_SECRET_ACCESS_KEY="your_secure_password"
   ```

2. **Production (Cloud Storage)**
   ```env
   S3_ENDPOINT="https://your-storage-service.com"
   S3_ACCESS_KEY_ID="your_cloud_storage_key"
   S3_SECRET_ACCESS_KEY="your_cloud_storage_secret"
   ```

## Security Considerations

### Authentication

- Use strong, unique values for all secret keys
- Rotate secrets regularly in production
- Use environment-specific secrets

### Database

- Use strong passwords
- Limit database access to necessary services
- Enable SSL in production

### Storage

- Set appropriate bucket policies
- Use separate credentials for different environments
- Enable encryption at rest

## Environment-Specific Configuration

### Development

```env
APP_ENV=development
DEBUG=true
MAIL_PROVIDER=nodemailer
```

### Staging

```env
APP_ENV=staging
DEBUG=false
MAIL_PROVIDER=resend
```

### Production

```env
APP_ENV=production
DEBUG=false
MAIL_PROVIDER=resend
```

## Validation and Troubleshooting

### Configuration Validation

The system validates configurations on startup:

1. **Email Provider**
   - Checks for required credentials
   - Falls back to console provider if invalid

2. **Storage Service**
   - Validates S3 credentials
   - Checks bucket accessibility

3. **Database**
   - Verifies connection string
   - Checks schema version

### Common Issues

1. **Email Configuration**
   - Check provider-specific requirements
   - Verify port accessibility
   - Check credentials format

2. **Storage Configuration**
   - Verify endpoint URL format
   - Check credential permissions
   - Ensure bucket exists

3. **Database Configuration**
   - Check connection string format
   - Verify host accessibility
   - Confirm user permissions

## Best Practices

1. **Environment Variables**
   - Use `.env.local` for local overrides
   - Never commit sensitive values
   - Use different values per environment

2. **Secrets Management**
   - Use a secure secret management system
   - Rotate credentials regularly
   - Limit access to production secrets

3. **Configuration Updates**
   - Document all configuration changes
   - Test changes in staging first
   - Use configuration version control

## Additional Resources

- [Environment Variables Reference](../reference/env-vars.md)
- [Security Guidelines](../deployment/security.md)
- [Production Deployment Guide](../deployment/production.md) 