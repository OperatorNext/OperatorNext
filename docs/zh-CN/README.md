# OperatorNext 文档中心

<div align="center">

[![Built with Next.js](https://img.shields.io/badge/Built%20with-Next.js%2015-black?style=flat&logo=next.js)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue?style=flat&logo=typescript)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4-38B2AC?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![pnpm](https://img.shields.io/badge/pnpm-10.0-orange?style=flat&logo=pnpm)](https://pnpm.io)

*企业级 AI 浏览器自动化平台*

[English](../README.md) | [简体中文](README.md)

</div>

## 📚 文档目录

- [快速开始](guides/getting-started.md)
- [架构概览](architecture/overview.md)
- [API 参考](api/reference.md)
- [部署指南](deployment/index.md)
- [贡献指南](contributing/index.md)

## 🚀 快速导航

### 用户指南
- [安装教程](guides/installation.md)
- [配置说明](guides/configuration.md)
- [使用手册](guides/user-guide.md)
- [常见问题](guides/faq.md)

### 开发者指南
- [开发环境搭建](guides/development.md)
- [代码风格指南](contributing/code-style.md)
- [测试指南](contributing/testing.md)
- [API 文档](api/reference.md)

### 运维指南
- [部署方案](deployment/options.md)
- [基础设施搭建](deployment/infrastructure.md)
- [监控与日志](deployment/monitoring.md)
- [安全指南](deployment/security.md)

## 🌟 核心特性

### AI 浏览器自动化
- 先进的 AI 驱动浏览器自动化能力
- 实时任务监控和控制
- 智能错误处理和恢复机制

### 现代化 Web 界面
- 精美响应式设计
- 深色模式支持
- WebSocket 实时更新
- 国际化（i18n）支持

### 企业级功能
- 基于角色的访问控制
- 审计日志
- 可扩展架构
- 高可用性设置

## 🛠 技术栈

### 前端技术
- Next.js 15 (App Router)
- React 19 (服务器组件)
- TypeScript 5.3
- Tailwind CSS 3.4
- Shadcn UI & Radix UI

### 后端技术
- Node.js & Express
- PostgreSQL 与 Prisma ORM
- MinIO (S3 兼容存储)
- Redis 缓存系统

### 开发工具
- pnpm 包管理器
- Turbo Repo 单仓库管理
- ESLint & Prettier 代码质量工具
- Jest & Playwright 测试框架

## 📦 项目结构

```
OperatorNext/
├── frontend/           # 前端单仓库
│   ├── apps/          # Next.js 应用
│   └── packages/      # 共享包
├── backend/           # 后端服务
├── infrastructure/    # 基础设施即代码
└── docs/             # 文档
    ├── en/           # 英文文档
    └── zh-CN/        # 中文文档
```

## 🤝 参与贡献

我们欢迎各种形式的贡献！详情请参阅我们的[贡献指南](contributing/index.md)。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../../LICENSE) 文件。

## 🌐 社区

- [GitHub 讨论区](https://github.com/OperatorNext/OperatorNext/discussions)
- [Discord 社区](https://discord.gg/operatornext)
- [Twitter](https://twitter.com/OperatorNext)

## 📞 技术支持

如需企业支持和定制化解决方案，请联系我们：support@operatornext.com
