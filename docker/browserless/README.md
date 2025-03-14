# 自定义 Browserless Docker 镜像

这个自定义 Docker 镜像基于官方的 `browserless/chrome` 镜像，但添加了对 ESM 模块和其他第三方库的支持，特别是 `@faker-js/faker`。

## 功能特性

- 支持 ECMAScript 模块 (ESM)，允许在 Function API 中使用 `import` 和 `export` 语法
- 内置 `@faker-js/faker` 库，用于生成测试数据
- 保留了原镜像的所有功能和配置选项

## 使用方法

### 构建镜像

在项目根目录运行以下命令来构建和启动包含自定义 Browserless 镜像的服务：

```bash
docker-compose up -d
```

### 使用 Function API 与 ESM 模块

现在你可以使用 Function API 与 ESM 模块语法了。例如：

```javascript
export default async function handler() {
  // 导入第三方库
  import { faker } from '@faker-js/faker';
  
  // 生成测试数据
  const users = Array.from({ length: 5 }, () => ({
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    avatar: faker.image.avatar()
  }));
  
  return {
    data: users,
    status: 'success'
  };
}
```

## 环境变量配置

以下环境变量已在 docker-compose.yml 中配置好：

- `FUNCTION_ENABLE_ESMODULES=true`: 启用 ESM 模块支持
- `FUNCTION_EXTERNALS=["@faker-js/faker", "esm"]`: 允许使用的外部模块

## 注意事项

- 确保 Function API 请求包含 `sourceType=module` 参数以启用 ESM 语法
- 使用 JSON API 时，在代码属性中包含 ESM 语法的代码 