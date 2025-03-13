# Browserless 实验

这个实验模块用于测试 Browserless 服务的各种功能。

## 环境配置

已在 docker-compose.yml 中配置了 Browserless 服务：
- 服务名：chrome
- 端口：13000
- WebSocket 地址：ws://localhost:13000
- Token：browser-token-2024

## 实验内容

1. 基础操作
   - 连接到 Browserless
   - 创建新标签页
   - 导航到网页
   - 页面交互（点击、输入等）
   - 截图和 PDF 导出

2. 高级特性
   - 并发会话管理
   - 超时处理
   - 错误恢复
   - 性能监控

3. HTTP API 调用
   - 内容获取 (/content API)
   - 屏幕截图 (/screenshot API)
   - 自定义函数 (/function API)
   - PDF 生成 (/pdf API)
   - 文件下载 (/download API)

## 运行示例

```bash
# 启动 Browserless 服务
docker-compose up -d chrome

# 运行基础示例
python -m labs.browserless.examples.basic_operations

# 运行 Google 搜索示例
python -m labs.browserless.examples.google_search

# 运行 Bing 搜索示例
python -m labs.browserless.examples.bing_search

# 运行并发测试示例
python -m labs.browserless.examples.concurrent_test

# 运行 HTTP API 示例
python -m labs.browserless.examples.http_api_demo
```

## 注意事项

1. 确保 Browserless 服务已启动
2. 检查服务健康状态：http://localhost:13000/health
3. 查看实时监控：http://localhost:13000/metrics 

## API 参考

### HTTP API

可以通过 HTTP API 直接与 Browserless 服务交互，无需使用 Playwright 库：

- `/content` - 获取网页渲染后的 HTML 内容
- `/screenshot` - 对网页进行截图
- `/pdf` - 将网页导出为 PDF
- `/function` - 在浏览器中执行自定义 JavaScript 函数
- `/download` - 下载浏览器中生成的文件

详细 API 文档请参考：https://browserless.io/docs/http.html 