from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.browser import router as browser_router
import uvicorn

app = FastAPI(
    title="Browser Use API",
    description="使用 AI 控制浏览器的 API",
    version="0.1.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加路由
app.include_router(browser_router, prefix="/api", tags=["browser"])

# 直接运行支持
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 