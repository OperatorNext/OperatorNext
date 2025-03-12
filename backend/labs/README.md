# OperatorNext Labs 🧪

这是 OperatorNext 的实验室目录，用于测试和实验各种 SDK 和新功能。

## 目录结构

```
labs/
├── README.md           # 本文件
├── common/            # 公共工具和类型
│   ├── __init__.py
│   ├── utils.py      # 通用工具函数
│   └── types.py      # 共享类型定义
│
└── autogen/          # AutoGen SDK 实验
    ├── README.md     # AutoGen 实验说明
    ├── src/          # 源代码
    ├── examples/     # 示例代码
    └── tests/        # 测试用例
```

## 使用指南

1. 每个 SDK 实验都在独立目录中
2. 使用 `common` 目录中的工具和类型
3. 遵循以下开发流程：
   - 在 `src/` 中实现核心功能
   - 在 `examples/` 中提供使用示例
   - 在 `tests/` 中编写测试用例

## 开发规范

1. 代码风格遵循项目 ruff 配置
2. 所有代码必须包含类型注解
3. 示例代码需要包含详细注释
4. 测试覆盖率要求 > 80%

## 环境设置

```bash
# 安装依赖
pip install -e ".[dev]"

# 运行测试
pytest labs/*/tests/
```

## 许可证

MIT License - 详见项目根目录的 LICENSE 文件 