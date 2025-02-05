# OperatorNext Frontend | Modern Web Interface for AI Browser Automation

<div align="center">

[![Built with Next.js](https://img.shields.io/badge/Built%20with-Next.js%2015-black?style=flat&logo=next.js)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue?style=flat&logo=typescript)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4-38B2AC?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![pnpm](https://img.shields.io/badge/pnpm-10.0-orange?style=flat&logo=pnpm)](https://pnpm.io)

*Enterprise-grade frontend monorepo for AI-powered browser automation*

</div>

## 🌟 Overview

The OperatorNext frontend is a modern, type-safe monorepo built with cutting-edge web technologies. It provides a seamless user interface for controlling and monitoring AI-driven browser automation tasks.

### Key Features

- 🎨 **Modern UI/UX** - Beautiful and responsive interface with dark mode support
- 🔄 **Real-time Updates** - WebSocket-based task monitoring and live feedback
- 🌍 **i18n Ready** - Full internationalization support with English and Chinese
- 📱 **Responsive Design** - Optimized for desktop, tablet, and mobile devices
- 🔒 **Type Safety** - End-to-end type safety with TypeScript and Prisma
- 🚀 **High Performance** - Built with Next.js 15 App Router and React Server Components

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ (LTS recommended)
- pnpm 10+
- Docker & Docker Compose (for development services)

### Installation

1. Install dependencies:
```bash
pnpm install
```

2. Set up environment variables:
```bash
cp .env.local.example .env.local
```

3. Initialize database and generate types:
```bash
# Push database schema
sudo pnpm db:push

# Generate Prisma client and types
sudo pnpm db:generate
```

> Note: `sudo` might be required for database operations depending on your system configuration.

### Development

Start the development server:
```bash
pnpm dev
```

This will start the following services:

| Service | URL | Purpose |
|---------|-----|---------|
| Next.js App | http://localhost:3000 | Main application interface |
| PostgreSQL | localhost:5438 | Database for persistent storage |
| PgAdmin | http://localhost:5051 | Database management UI |
| MinIO | http://localhost:9002 | S3-compatible object storage |
| MinIO Console | http://localhost:9003 | Storage management UI |
| Maildev | http://localhost:8026 | Email testing interface |

### Local Development Best Practices

#### Email Service Configuration
The project supports multiple email providers that can be configured via environment variables:

```env
# Available providers: "nodemailer" | "resend" | "plunk" | "postmark" | "console" | "custom"
MAIL_PROVIDER="nodemailer"
```

For local development:
- Use `nodemailer` provider with Maildev
- Configure in `.env.local`:
  ```env
  MAIL_PROVIDER="nodemailer"
  MAIL_HOST="localhost"
  MAIL_PORT="1026"
  ```
- Access Maildev UI at http://localhost:8026 to view sent emails

For production:
- Use cloud email services like Resend or Postmark
- Configure the appropriate provider and API keys
- Example with Resend:
  ```env
  MAIL_PROVIDER="resend"
  RESEND_API_KEY="your_api_key"
  ```

#### Storage Service Configuration
The project uses S3-compatible storage that can be configured for both local development and production:

For local development:
- Uses MinIO as S3-compatible storage
- Configure in `.env.local`:
  ```env
  S3_ACCESS_KEY_ID="operatornext_storage_admin"
  S3_SECRET_ACCESS_KEY="your_secure_password"
  S3_ENDPOINT="http://localhost:9002"
  NEXT_PUBLIC_AVATARS_BUCKET_NAME="avatars"
  ```
- Access MinIO Console at http://localhost:9003 for storage management

For production:
- Use cloud storage services (e.g., Supabase Storage, AWS S3)
- Configure the appropriate credentials and endpoint
- Example with Supabase Storage:
  ```env
  S3_ACCESS_KEY_ID="your_cloud_storage_key"
  S3_SECRET_ACCESS_KEY="your_cloud_storage_secret"
  S3_ENDPOINT="https://your-project.supabase.co/storage/v1/s3"
  ```

The storage service is used for:
- User avatar uploads
- File attachments
- Other static assets

Note: When using Docker Compose, the services are automatically configured with the correct environment variables and network settings.

## 📦 Project Structure

```
frontend/
├── apps/
│   └── web/              # Main Next.js application
│       ├── app/          # App router pages and layouts
│       ├── modules/      # Feature-based modules
│       ├── public/       # Static assets
│       └── styles/       # Global styles
├── packages/
│   ├── ai/              # AI integration and models
│   ├── api/             # API routes and handlers
│   ├── auth/            # Authentication and authorization
│   ├── database/        # Database schema and migrations
│   ├── i18n/            # Internationalization system
│   ├── mail/            # Email templates and services
│   ├── payments/        # Payment processing integration
│   └── ui/              # Shared UI components library
└── tooling/             # Build and development tools
    ├── eslint/          # ESLint configurations
    ├── prettier/        # Prettier configurations
    └── typescript/      # TypeScript configurations
```

## 🛠 Available Scripts

- `pnpm dev` - Start development environment
- `pnpm build` - Build all packages and apps
- `pnpm lint` - Run ESLint across the monorepo
- `pnpm format` - Format code with Prettier
- `pnpm test` - Run test suites
- `pnpm clean` - Clean build artifacts
- `pnpm db:push` - Push database schema changes
- `pnpm db:generate` - Generate Prisma client
- `pnpm db:studio` - Open Prisma Studio UI

## 🔧 Technology Stack

### Core
- Next.js 15 (App Router)
- React 19 (Server Components)
- TypeScript 5.3
- Tailwind CSS 3.4

### State Management & Data
- Prisma ORM
- PostgreSQL
- MinIO (S3)
- Zustand

### UI Components
- Shadcn UI
- Radix UI
- Framer Motion
- Lucide Icons

### Development Tools
- Turbo Repo
- ESLint
- Prettier
- Biome
- Husky

### Testing & Quality
- Jest
- React Testing Library
- Playwright
- TypeScript strict mode

## 📚 Documentation

For detailed documentation, please visit our [documentation site](https://github.com/OperatorNext/OperatorNext/tree/main/docs).

## 🤝 Contributing

Please read our [Contributing Guide](../CONTRIBUTING.md) for details on our code of conduct and development process.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
