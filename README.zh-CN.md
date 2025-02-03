# OperatorNext 🤖

<div align="center">

<img src=".github/assets/brand/logo.png" alt="OperatorNext Logo" width="500"/>

[![GitHub license](https://img.shields.io/github/license/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/OperatorNext/OperatorNext)](https://github.com/OperatorNext/OperatorNext/pulls)
[![Tests](https://github.com/OperatorNext/OperatorNext/actions/workflows/test.yml/badge.svg)](https://github.com/OperatorNext/OperatorNext/actions)

[English](./README.md) | [简体中文](./README.zh-CN.md)

</div>

OperatorNext 是一个基于 AI 的智能浏览器操作平台，它能够通过自然语言理解和执行复杂的浏览器任务。通过结合最新的 LLM 技术和浏览器自动化，我们为开发者和用户提供了一个强大的工具，能够轻松实现网页自动化、数据采集、UI 测试等多种场景的应用。

## ✨ 特性

- 🤖 **智能任务执行** - 通过自然语言描述即可完成复杂的浏览器操作
- 🔄 **实时状态反馈** - WebSocket 实时推送任务执行状态和进度
- 🎯 **精确控制** - 支持精确的 DOM 操作和复杂的交互场景
- 📊 **性能监控** - 内置系统资源监控，实时掌握任务执行情况
- 🔒 **安全可靠** - 完善的错误处理和异常恢复机制
- 🌐 **中文优化** - 完整的中文交互体验和错误提示

## 🚀 快速开始

### 环境要求

- Docker & Docker Compose
- Node.js 18+
- Chrome/Chromium 浏览器

### 安装

1. 克隆仓库

```bash
git clone https://github.com/OperatorNext/OperatorNext.git
cd OperatorNext
```

2. 复制环境变量模板

```bash
# 复制前端环境变量
cp frontend/.env.local.example frontend/.env.local

# 复制 Docker 环境变量
cp .env.example .env
```

3. 安装前端依赖

```bash
cd frontend
npm install
```

### 启动服务

1. 启动 Docker 服务（PostgreSQL、MinIO、邮件服务器）

```bash
docker-compose up -d
```

这将启动以下服务：
- PostgreSQL 数据库（端口 5438）
- PgAdmin 管理界面（http://localhost:5051）
- MinIO 对象存储（API：http://localhost:9002，控制台：http://localhost:9003）
- Maildev 邮件服务（SMTP：1026，Web界面：http://localhost:8026）

2. 启动前端开发服务器

```bash
cd frontend
npm run dev
```

访问 http://localhost:3000 即可使用。

## 📖 使用示例

```python
# 创建一个新的浏览器任务
task = {
    "task_description": "登录GitHub并star一个项目"
}
response = requests.post("http://localhost:8000/api/tasks", json=task)
task_id = response.json()["task_id"]

# 通过WebSocket监听任务状态
ws = websockets.connect(f"ws://localhost:8000/ws/tasks/{task_id}")
```

更多示例请查看我们的[文档](https://github.com/OperatorNext/OperatorNext/tree/main/docs)。

## 🔧 技术架构

### 后端技术栈
- FastAPI
- WebSocket
- Playwright
- LangChain
- PostgreSQL
- MinIO

### 前端技术栈
- Next.js 14 (App Router)
- React
- TypeScript
- Tailwind CSS
- Shadcn UI

## 📝 文档

详细文档请访问我们的[项目文档](https://github.com/OperatorNext/OperatorNext/tree/main/docs)。

## 🤝 贡献指南

我们欢迎所有形式的贡献，无论是新功能、文档改进还是问题反馈。请查看我们的 [贡献指南](CONTRIBUTING.md) 了解更多信息。

## 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

## 🙏 致谢

本项目受到以下项目的启发和技术支持：
- [browser-use](https://github.com/browser-use/browser-use)
- [browserless](https://github.com/browserless/browserless)

感谢所有为这个项目做出贡献的开发者们！

<div align="center">
  <img src="https://contrib.rocks/image?repo=OperatorNext/OperatorNext" />
</div>

## 🌟 Star History

<div align="center">
  <img src="https://api.star-history.com/svg?repos=OperatorNext/OperatorNext&type=Date" />
</div>

## 📮 联系我们

- 提交 Issue: [GitHub Issues](https://github.com/OperatorNext/OperatorNext/issues)
- 邮件联系: hi@operatornext.com
- Telegram: [@HaiPro_2025](https://t.me/HaiPro_2025)
- 公司: CyberPoet LLC 