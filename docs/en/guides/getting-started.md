# Getting Started with OperatorNext

This guide will help you get started with OperatorNext, an enterprise-grade AI browser automation platform.

## Prerequisites

Before you begin, ensure you have the following installed:

- Node.js 18+ (LTS recommended)
- pnpm 10+
- Docker & Docker Compose
- Git

## Quick Installation

1. Clone the repository:
```bash
git clone https://github.com/OperatorNext/OperatorNext.git
cd OperatorNext
```

2. Install dependencies:
```bash
pnpm install
```

3. Set up environment variables:
```bash
cp .env.local.example .env.local
```

4. Initialize the database:
```bash
# Push database schema
sudo pnpm db:push

# Generate Prisma client and types
sudo pnpm db:generate
```

## Development Environment

Start the development server:
```bash
pnpm dev
```

This will start all necessary services:

| Service | URL | Purpose |
|---------|-----|---------|
| Next.js App | http://localhost:3000 | Main application interface |
| PostgreSQL | localhost:5438 | Database for persistent storage |
| PgAdmin | http://localhost:5051 | Database management UI |
| MinIO | http://localhost:9002 | S3-compatible object storage |
| MinIO Console | http://localhost:9003 | Storage management UI |
| Maildev | http://localhost:8026 | Email testing interface |

## Configuration

### Email Service

Configure the email service in your `.env.local`:

```env
# Available providers: "nodemailer" | "resend" | "plunk" | "postmark" | "console" | "custom"
MAIL_PROVIDER="nodemailer"

# For local development
MAIL_HOST="localhost"
MAIL_PORT="1026"
```

### Storage Service

Configure the storage service in your `.env.local`:

```env
# For local development with MinIO
S3_ACCESS_KEY_ID="operatornext_storage_admin"
S3_SECRET_ACCESS_KEY="your_secure_password"
S3_ENDPOINT="http://localhost:9002"
NEXT_PUBLIC_AVATARS_BUCKET_NAME="avatars"
```

## Verify Installation

1. Open http://localhost:3000 in your browser
2. Sign up for a new account
3. Check http://localhost:8026 for the verification email
4. Complete the email verification process

## Next Steps

- [Configuration Guide](configuration.md) - Learn about all configuration options
- [User Guide](user-guide.md) - Learn how to use OperatorNext
- [Development Guide](development.md) - Learn how to develop with OperatorNext
- [API Reference](../api/reference.md) - Explore the API documentation

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Ensure PostgreSQL is running: `docker ps | grep postgres`
   - Check database logs: `docker-compose logs db`

2. **Email Service Issues**
   - Verify Maildev is running: `docker ps | grep maildev`
   - Check Maildev UI at http://localhost:8026

3. **Storage Service Issues**
   - Ensure MinIO is running: `docker ps | grep minio`
   - Check MinIO Console at http://localhost:9003

### Getting Help

- Check our [FAQ](faq.md)
- Join our [Discord Community](https://discord.gg/operatornext)
- Open an issue on [GitHub](https://github.com/OperatorNext/OperatorNext/issues)

## Security Notes

- Never commit your `.env.local` file
- Use strong passwords for all services
- Keep your dependencies up to date
- Follow our [Security Guidelines](../deployment/security.md) 