# OperatorNext 🤖

<div align="center">

<img src=".github/assets/brand/logo.png" alt="OperatorNext Logo" width="500"/>

[![GitHub license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/OperatorNext/OperatorNext/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/pulls)
[![Discord](https://img.shields.io/discord/1336375322379161661?logo=discord&logoColor=white)](https://discord.gg/zafb9TzYYA)
[![Version](https://img.shields.io/github/v/release/OperatorNext/OperatorNext?include_prereleases&label=version)](https://github.com/OperatorNext/OperatorNext/releases)

[English](./README.md) | [简体中文](./README.zh-CN.md)

---

**Open-Source Alternative to OpenAI Operator**

*LLM-Powered Browser Automation Agent*

[Get Started](#-getting-started) • [Documentation](https://github.com/OperatorNext/OperatorNext/tree/main/docs) • [Examples](#-usage-example) • [Contributing](#-contributing) • [Demo](https://operatornext.com)

</div>

OperatorNext is an open-source AI agent platform that understands and executes complex browser tasks through natural language processing and visual reasoning. By combining state-of-the-art LLM technologies (including GPT-4o, Claude, and more) with browser automation, we provide developers and users with a powerful Computer-Using Agent (CUA) for web automation, data collection, UI testing, and various other scenarios.

<div align="center">
  <p><strong>🖥️ Modern Interface with Real-time Task Monitoring</strong></p>
  <img src=".github/assets/hero.png" alt="Operator Next Hero" width="100%" />
  
  <p><strong>🤖 Intelligent Task Execution with Visual Feedback</strong></p>
  <img src=".github/assets/hero2.png" alt="Operator Next Screenshot" width="100%" />
</div>

> ⚠️ **Project Status**
>
> This project is in early development stage. Core features are under active development and not yet implemented.
> 
> Please note that breaking changes may occur frequently during this phase.

### 🌟 Why Choose OperatorNext?

| Feature | OperatorNext | OpenAI Operator |
|---------|-------------|-----------------|
| License | MIT Open Source | Proprietary |
| Deployment | Self-hosted & Cloud | Cloud-only |
| Data Privacy | Local Processing | Cloud Processing |
| Customization | Full Control | Limited |
| Cost | Free & Self-hosted | Usage-based Pricing |
| API Integration | Flexible & Open | Restricted |

OperatorNext empowers developers with:
- 🔍 **Web Scraping & Data Extraction** - Automated data collection with pixel-level accuracy
- 🧪 **End-to-End Testing** - Modern alternative to Selenium for UI/UX testing
- 🤖 **RPA (Robotic Process Automation)** - Chain-of-Thought planning for complex tasks
- 🌐 **Web Testing & QA** - Visual reasoning based quality assurance
- 📊 **Data Mining & Analytics** - Intelligent web data gathering with self-correction
- 🔄 **Workflow Automation** - Custom workflow design with plugin ecosystem

Perfect for:
- DevOps and QA Teams (Automated Testing)
- Data Scientists and Researchers (Web Scraping)
- Digital Marketing Professionals (Form Automation)
- Business Process Automation (RPA Solutions)
- Web Developers and Testers (GUI Testing)
- Enterprise Automation Solutions (Custom Workflows)

## ✨ Features

- 🤖 **AI Agent & Visual Reasoning** - Complete complex browser operations through natural language and visual understanding, powered by GPT-4o multimodal capabilities
- 🧠 **Chain-of-Thought Planning** - Advanced task planning and execution with reinforcement learning for optimal automation
- 🎯 **Precise GUI Interaction** - Pixel-perfect DOM operations, XPath navigation, and complex interaction scenarios using computer vision
- 📊 **Real-time Task Tracking** - WebSocket-based monitoring system with CPU, memory, and network metrics for execution insights
- 🔒 **Privacy-First Design** - Local processing of sensitive data with comprehensive error handling and self-correction mechanisms
- 🌐 **Cross-Platform & Multilingual** - Full i18n support with Chinese/English interfaces, works on Windows, macOS, and Linux
- 🔌 **Extensible Architecture** - REST API, WebSocket endpoints, and plugin system for seamless integration
- 🚀 **Cloud & Self-Hosted** - Deploy on your infrastructure or use our cloud solution for maximum flexibility
- ⚡ **High Performance** - Parallel task execution with optimized resource management
- 🎨 **Modern Developer Experience** - Beautiful UI/UX built with Next.js and Tailwind CSS, extensive API documentation

## 🚀 Getting Started

Try our online demo at [operatornext.com](https://operatornext.com) or set up your own instance:

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
sudo pnpm db:push

# Generate Prisma client and types
sudo pnpm db:generate
```

> Note: `sudo` might be required for database operations depending on your system configuration.

### Start Services

1. Start Docker services

```bash
docker-compose up -d
```

This will start the following services:

| Service | URL | Description |
|---------|-----|-------------|
| Web Application | http://localhost:3000 | Next.js frontend application |
| PgAdmin | http://localhost:5051 | PostgreSQL database management |
| Maildev | http://localhost:8026 | Email testing interface |
| MinIO Console | http://localhost:9003 | Object storage management |
| MinIO API | http://localhost:9002 | S3-compatible API endpoint |
| PostgreSQL | localhost:5438 | Database (connect via psql or GUI) |

### Default Credentials

> ⚠️ These are development credentials. Do NOT use in production!

- **PostgreSQL**:
  - User: operatornext_prod_user
  - Database: operatornext_production

- **PgAdmin**:
  - Email: admin@operatornext.dev
  - Password: See `.env` file

- **MinIO**:
  - Access Key: See `MINIO_ROOT_USER` in `.env`
  - Secret Key: See `MINIO_ROOT_PASSWORD` in `.env`

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

### AI & Automation
- LLM Support - Compatible with GPT-4o, Claude, and other language models
- LangChain - Large Language Model (LLM) orchestration framework
- Computer Vision - Pixel-level DOM interaction and visual analysis
- Reinforcement Learning - Self-improving task execution strategies
- Chain-of-Thought - Advanced planning and decision making

### Backend Infrastructure
- FastAPI - High-performance Python web framework for building scalable APIs
- WebSocket - Real-time bidirectional communication for task monitoring
- Playwright - Modern web testing and automation with superior stability
- PostgreSQL - Advanced open-source database for task management
- MinIO - S3-compatible object storage for artifact management
- Redis - In-memory data structure store for caching and queuing
- Docker - Containerization and deployment automation

### Frontend Technologies
- Next.js 15 (App Router) - React framework with server-side rendering
- React 19 - Latest version with concurrent features and Suspense
- TypeScript - Type-safe JavaScript development for reliability
- Tailwind CSS - Utility-first CSS framework for modern UI
- Shadcn UI - Modern and accessible component library
- Prisma - Next-generation ORM for type-safe database access
- Turbo Repo - High-performance monorepo build system
- WebSocket - Real-time updates and task monitoring
- Biome - Fast and reliable code formatter

### DevOps & Quality
- Docker Compose - Multi-container orchestration
- GitHub Actions - CI/CD automation pipeline
- Playwright - End-to-end testing framework
- Prisma - Database schema management and migrations
- Biome - Code quality and formatting tools
- pnpm - Fast, disk space efficient package manager

### Security & Privacy
- Local Processing - Sensitive data handling
- End-to-End Encryption - Secure communication
- Role-Based Access - Fine-grained permissions
- Audit Logging - Comprehensive activity tracking

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

## 📮 Contact & Community

Join our growing community:

- [Discord](https://discord.gg/zafb9TzYYA) - Join our community for discussions, support, and updates
- [Slack](https://join.slack.com/t/operatornext/shared_invite/zt-2yzynnxiv-ywt7Z8UtykGAm6EUfpljQA) - Join our Slack workspace for team collaboration
- [GitHub Issues](https://github.com/OperatorNext/OperatorNext/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/OperatorNext/OperatorNext/discussions) - Technical discussions and questions
- Email: hi@operatornext.com
- Telegram: [@HaiPro_2025](https://t.me/HaiPro_2025)

Company: CyberPoet LLC (Position: CEO) 