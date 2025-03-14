# 使用 Browserless 官方镜像作为基础镜像，从GitHub Container Registry获取
FROM ghcr.io/browserless/chromium:latest

# 安装faker-js库和其他可能需要的依赖
RUN npm install @faker-js/faker esm

# 设置环境变量，允许使用外部模块
ENV FUNCTION_EXTERNALS='["@faker-js/faker", "esm"]'
ENV FUNCTION_BUILT_INS='["url"]'
ENV FUNCTION_ENV_VARS=[]

# 配置支持ESM模块的参数
ENV FUNCTION_ENABLE_ESMODULES=true

# 安全和API配置
ENV ENABLE_CORS=true
ENV CORS_ALLOW_ORIGINS="http://localhost:3000,http://localhost:8000"
ENV ENABLE_API_GET=true
ENV TOKEN="browser-token-2024"

# 启用HTTP GET API
ENV ALLOW_GET=true

# 浏览器配置
ENV DEFAULT_HEADLESS=true
ENV DEFAULT_IGNORE_HTTPS_ERRORS=true
ENV DEFAULT_USER_DATA_DIR=/tmp/browserless-data-dir
ENV DOWNLOAD_DIR=/tmp/downloads

# 设置健康检查
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f "http://localhost:3000/metrics?token=${TOKEN:-browser-token-2024}" || exit 1

# 暴露端口
EXPOSE 3000

# 使用默认的启动命令
CMD ["node", "/usr/src/app/build/index.js"] 