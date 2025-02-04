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
pnpm db:push

# Generate Prisma client and types
pnpm db:generate
```

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
