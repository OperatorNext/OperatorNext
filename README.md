# OperatorNext 🤖

<div align="center">

[![GitHub license](https://img.shields.io/github/license/yourusername/OperatorNext)](https://github.com/yourusername/OperatorNext/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/OperatorNext)](https://github.com/yourusername/OperatorNext/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/OperatorNext)](https://github.com/yourusername/OperatorNext/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/OperatorNext)](https://github.com/yourusername/OperatorNext/pulls)
[![Tests](https://github.com/yourusername/OperatorNext/workflows/Tests/badge.svg)](https://github.com/yourusername/OperatorNext/actions)

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

- Python 3.9+
- Node.js 18+
- Chrome/Chromium browser

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/OperatorNext.git
cd OperatorNext
```

2. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies

```bash
cd frontend
npm install
```

### Configuration

1. Copy environment variable templates

```bash
cp frontend/.env.local.example frontend/.env.local
cp backend/.env.example backend/.env
```

2. Configure necessary environment variables (API keys, etc.)

### Start Services

1. Start backend server

```bash
cd backend
uvicorn main:app --reload
```

2. Start frontend development server

```bash
cd frontend
npm run dev
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

For more examples, please visit our [documentation](https://docs.operatornext.com).

## 🔧 Technology Stack

### Backend
- FastAPI
- WebSocket
- Playwright
- LangChain

### Frontend
- Next.js 14 (App Router)
- React
- TypeScript
- Tailwind CSS
- Shadcn UI

## 📝 Documentation

For detailed documentation, please visit our [documentation site](https://docs.operatornext.com).

## 🤝 Contributing

We welcome all forms of contributions, whether it's new features, documentation improvements, or bug reports. Please check our [Contributing Guide](CONTRIBUTING.md) for more information.

## 📄 License

This project is licensed under the [MIT](LICENSE) License.

## 🙏 Acknowledgments

Thanks to all the developers who have contributed to this project!

<div align="center">
  <img src="https://contrib.rocks/image?repo=yourusername/OperatorNext" />
</div>

## 🌟 Star History

<div align="center">
  <img src="https://api.star-history.com/svg?repos=yourusername/OperatorNext&type=Date" />
</div>

## 📮 Contact Us

- Submit Issues: [GitHub Issues](https://github.com/yourusername/OperatorNext/issues)
- Email: your-email@example.com
- WeChat Official Account: OperatorNext
- Discord: [Join our Discord](https://discord.gg/operatornext) 