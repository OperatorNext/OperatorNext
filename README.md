# OperatorNext 🤖

> **Project Status**: This project is in early development stage. Core features are under active development and not yet implemented.

## Roadmap

- [ ] **Phase 1: Infrastructure Setup** (In Progress)
  - [x] Docker environment setup
  - [x] Database schema design
  - [ ] Authentication system
  - [ ] Basic UI components

- [ ] **Phase 2: Core Features**
  - [ ] User management and organization structure
  - [ ] Role-based access control (RBAC)
  - [ ] AI agent management
  - [ ] Knowledge base integration

- [ ] **Phase 3: AI Features**
  - [ ] LLM integration
  - [ ] Prompt engineering interface
  - [ ] Model fine-tuning capabilities
  - [ ] Multi-model orchestration

- [ ] **Phase 4: Advanced Features**
  - [ ] Real-time collaboration
  - [ ] Advanced analytics and monitoring
  - [ ] API integration capabilities
  - [ ] Custom workflow builder

<div align="center">

<img src=".github/assets/brand/logo.png" alt="OperatorNext Logo" width="500"/>

[![GitHub license](https://img.shields.io/github/license/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/pulls)
[![Tests](https://github.com/OperatorNext/OperatorNext/actions/workflows/test.yml/badge.svg)](https://github.com/OperatorNext/OperatorNext/actions)

[English](./README.md) | [简体中文](./README.zh-CN.md)

</div>

OperatorNext is an AI-powered intelligent browser automation platform that understands and executes complex browser tasks through natural language processing. By combining cutting-edge LLM technology with browser automation, we provide developers and users with a powerful tool for web automation, data collection, UI testing, and various other scenarios.

## ✨ Features

- 🤖 **Intelligent Task Execution** - Complete complex browser operations through natural language descriptions
- 🔄 **Real-time Status Updates** - WebSocket-based real-time task execution status and progress
- 🎯 **Precise Control** - Support for accurate DOM operations and complex interaction scenarios
- 📊 **Performance Monitoring** - Built-in system resource monitoring for real-time task execution insights
- 🔒 **Reliable & Secure** - Comprehensive error handling and exception recovery mechanisms
- 🌐 **Multi-language Support** - Full Chinese language support with localized interaction experience

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- pnpm 10+
- Chrome/Chromium browser

### Installation

1. Clone the repository

```bash
git clone https://github.com/OperatorNext/OperatorNext.git
cd OperatorNext
```

2. Copy environment variable templates

```bash
# Copy frontend environment variables
cp frontend/.env.local.example frontend/.env.local

# Copy Docker environment variables
cp .env.example .env
```

3. Install frontend dependencies

```bash
cd frontend
pnpm install
```

4. Initialize database and generate types

```bash
# Push database schema
pnpm db:push

# Generate Prisma client and types
pnpm db:generate
```

### Start Services

1. Start Docker services (PostgreSQL, MinIO, Mail Server)

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5438)
- PgAdmin interface (http://localhost:5051)
- MinIO storage (API: http://localhost:9002, Console: http://localhost:9003)
- Maildev server (SMTP: 1026, Web UI: http://localhost:8026)

2. Start frontend development server

```bash
cd frontend
pnpm dev
```

Visit http://localhost:3000 to use the application.

## 📖 Usage Example

```python
# Create a new browser task
task = {
    "task_description": "Login to GitHub and star a repository"
}
response = requests.post("http://localhost:8000/api/tasks", json=task)
task_id = response.json()["task_id"]

# Monitor task status via WebSocket
ws = websockets.connect(f"ws://localhost:8000/ws/tasks/{task_id}")
```

For more examples, please visit our [documentation](https://github.com/OperatorNext/OperatorNext/tree/main/docs).

## 🔧 Technology Stack

### Backend
- FastAPI
- WebSocket
- Playwright
- LangChain
- PostgreSQL
- MinIO

### Frontend
- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- Shadcn UI
- Prisma
- Turbo Repo

## 📝 Documentation

For detailed documentation, please visit our [documentation](https://github.com/OperatorNext/OperatorNext/tree/main/docs).

## 🤝 Contributing

We welcome all forms of contributions, whether it's new features, documentation improvements, or bug reports. Please check our [Contributing Guide](CONTRIBUTING.md) for more information.

## 📄 License

This project is licensed under the [MIT](LICENSE) License.

## 🙏 Acknowledgments

This project is inspired by and built upon:
- [browser-use](https://github.com/browser-use/browser-use)
- [browserless](https://github.com/browserless/browserless)

Thanks to all the developers who have contributed to this project!

<div align="center">
  <img src="https://contrib.rocks/image?repo=OperatorNext/OperatorNext" />
</div>

## 🌟 Star History

<div align="center">
  <img src="https://api.star-history.com/svg?repos=OperatorNext/OperatorNext&type=Date" />
</div>

## 📮 Contact Us

- Submit Issues: [GitHub Issues](https://github.com/OperatorNext/OperatorNext/issues)
- Email: hi@operatornext.com
- Telegram: [@HaiPro_2025](https://t.me/HaiPro_2025)
- Company: CyberPoet LLC 