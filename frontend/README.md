# OperatorNext Frontend

This is the frontend monorepo for OperatorNext, built with Next.js 15, TypeScript, and Tailwind CSS.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- pnpm 10+
- Docker (for development services)

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

This will start:
- Next.js app at http://localhost:3000
- Database at port 5438
- PgAdmin at http://localhost:5051
- MinIO at http://localhost:9002 (Console: http://localhost:9003)
- Maildev at http://localhost:8026

## 📦 Project Structure

```
frontend/
├── apps/
│   └── web/          # Main Next.js application
├── packages/
│   ├── ai/           # AI-related functionality
│   ├── api/          # API routes and handlers
│   ├── auth/         # Authentication logic
│   ├── database/     # Database schema and types
│   ├── i18n/         # Internationalization
│   ├── mail/         # Email templates and sending
│   ├── payments/     # Payment processing
│   └── ui/           # Shared UI components
└── tooling/          # Development tools and configs
```

## 🛠 Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm db:push` - Push database schema changes
- `pnpm db:generate` - Generate Prisma client and types
- `pnpm db:studio` - Open Prisma Studio
- `pnpm seed` - Seed the database
- `pnpm lint` - Run linter
- `pnpm format` - Format code
- `pnpm clean` - Clean build files

## 🔧 Tech Stack

- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- Shadcn UI
- Prisma
- PostgreSQL
- MinIO
- Turbo Repo

## 📚 Documentation

For detailed documentation, please visit our [documentation site](https://github.com/OperatorNext/OperatorNext/tree/main/docs).
