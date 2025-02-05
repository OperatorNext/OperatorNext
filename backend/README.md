# OperatorNext Backend

LLM-Powered Browser Automation Agent Backend Service

## 开发环境设置

1. 创建虚拟环境：
```bash
uv venv
source .venv/bin/activate
```

2. 安装依赖：
```bash
uv pip install -e ".[dev]"
```

3. 安装 pre-commit hooks：
```bash
pre-commit install
```

4. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置
```

5. 运行开发服务器：
```bash
uvicorn main:app --reload
```

## 项目结构

```
backend/
├── api/         # API 路由和端点
├── core/        # 核心配置和工具
├── models/      # 数据模型
├── schemas/     # API 模式
└── services/    # 业务逻辑服务
```

## 技术栈

- FastAPI
- SQLAlchemy
- Pydantic
- browser-use
- LangChain 