# Browserless ESM 模块支持

## 需求背景

Browserless 是一个提供无头 Chrome 环境的强大服务，用于自动化浏览器操作。其中，Function API 是一个关键功能，允许执行 JavaScript 代码并与浏览器进行交互。然而，默认的 Browserless 镜像对现代 JavaScript 特性如 ESM 模块（使用 `import`/`export` 语法）的支持有限。

本文档记录了我们如何扩展官方 Browserless Docker 镜像，以添加对 ESM 模块的支持，以及如何引入第三方 JavaScript 库，特别是 `@faker-js/faker`。

## 实现方案

### 1. 创建自定义 Dockerfile

我们创建了一个扩展的 Dockerfile，基于官方的 `browserless/chrome` 镜像，添加了对 ESM 模块的支持和所需的第三方库。

**文件位置**: `docker/browserless/Dockerfile`

```dockerfile
# 使用 Browserless 官方镜像作为基础镜像
FROM browserless/chrome:latest

# 设置工作目录
WORKDIR /browserless

# 安装faker-js库和其他可能需要的依赖
RUN npm install @faker-js/faker esm

# 配置 Node.js 环境支持 ESM 模块
ENV NODE_OPTIONS="--experimental-modules --es-module-specifier-resolution=node"

# 设置环境变量，允许使用外部模块
ENV FUNCTION_EXTERNALS='["@faker-js/faker", "esm"]'

# 配置支持ESM模块的参数
ENV FUNCTION_ENABLE_ESMODULES=true

# 设置健康检查
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:3000/health || exit 1

# 暴露端口
EXPOSE 3000

# 使用默认的启动命令
CMD ["node", "browserless.js"]
```

### 2. 修改 docker-compose.yml

我们更新了 `docker-compose.yml` 中的 `chrome` 服务配置，使其使用我们的自定义 Dockerfile 而不是直接使用官方镜像，并添加了必要的环境变量。

```yaml
chrome:
  build:
    context: ./docker/browserless
    dockerfile: Dockerfile
  platform: linux/arm64
  container_name: operatornext-chrome
  environment:
    # ... 原有配置保持不变 ...
    
    # ESM模块支持
    - FUNCTION_ENABLE_ESMODULES=true
    - FUNCTION_EXTERNALS=["@faker-js/faker", "esm"]
```

### 3. 更新测试脚本

我们修改了 `function_api_demo.py` 测试脚本，使其使用本地安装的 `@faker-js/faker` 库，而不是从 CDN 加载，并确保在请求中包含 `sourceType=module` 参数。

**修改前**:
```javascript
import { faker } from "https://esm.sh/@faker-js/faker";
```

**修改后**:
```javascript
import { faker } from "@faker-js/faker";
```

### 4. 创建构建和测试脚本

我们创建了一个便捷的 `build-and-test.sh` 脚本，用于构建自定义 Docker 镜像，启动服务，并运行测试。

## 使用方法

1. **构建和启动自定义 Browserless 服务**:
   ```bash
   ./docker/browserless/build-and-test.sh
   ```

2. **在代码中使用 Function API**:
   确保在调用 Function API 时添加 `sourceType=module` 参数：
   ```
   http://localhost:13000/function?token=your-token&sourceType=module
   ```

3. **使用 ESM 语法**:
   ```javascript
   import { faker } from "@faker-js/faker";

   export default async function() {
     // 你的代码
   }
   ```

## 注意事项

1. **兼容性**: 确保使用的 Browserless 版本支持 ESM 模块功能。
2. **请求头**: 使用 `application/javascript` 或 `application/json` 作为 Content-Type。
3. **URL 参数**: 始终在请求中包含 `sourceType=module` 参数。
4. **错误处理**: 如果遇到 "Unexpected identifier" 等错误，检查 JavaScript 语法是否正确。

## 排错指南

1. **检查日志**:
   ```bash
   docker-compose logs chrome
   ```

2. **验证健康状态**:
   ```bash
   curl http://localhost:13000/health
   ```

3. **常见错误**:
   - `'import' and 'export' may only appear with 'sourceType: module'`: 确保添加了 `sourceType=module` 参数。
   - `Cannot find module`: 检查模块名称是否正确，且已在 Dockerfile 中安装。

## 结论

通过自定义 Dockerfile 和环境配置，我们成功地扩展了 Browserless 服务，使其支持 ESM 模块和第三方库。这使得我们可以在 Function API 中使用现代 JavaScript 语法和丰富的外部库，极大地增强了服务的功能和灵活性。 