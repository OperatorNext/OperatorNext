import logging
import sys

from fastapi import APIRouter, HTTPException, Request, WebSocket

from schemas.browser_task import BrowserTask, BrowserTaskCreate
from services.browser import BrowserService

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 添加控制台处理器
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

router = APIRouter()
logger.info("初始化 BrowserService...")
browser_service = BrowserService()
logger.info("BrowserService 初始化完成")


@router.post("/tasks", response_model=BrowserTask)
async def create_task(task: BrowserTaskCreate, request: Request) -> BrowserTask:
    """创建新任务"""
    logger.info("=" * 50)
    logger.info("收到创建任务请求")
    logger.info(f"请求方法: {request.method}")
    logger.info(f"请求URL: {request.url}")
    logger.info(f"客户端IP: {request.client.host}")
    logger.info(f"任务描述: {task.task_description}")

    try:
        logger.info("开始创建任务...")
        result = browser_service.create_task(task.task_description)
        logger.info(f"任务创建成功: {result.task_id}")
        logger.info("=" * 50)
        return result
    except Exception as e:
        logger.error("创建任务失败!")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"错误信息: {str(e)}")
        logger.exception("详细错误信息:")
        logger.error("=" * 50)
        raise HTTPException(status_code=500, detail=f"创建任务时发生错误: {str(e)}")


@router.get("/tasks/{task_id}", response_model=BrowserTask)
async def get_task(task_id: str, request: Request) -> BrowserTask:
    """获取任务状态"""
    logger.info("=" * 50)
    logger.info("收到获取任务请求")
    logger.info(f"请求方法: {request.method}")
    logger.info(f"请求URL: {request.url}")
    logger.info(f"客户端IP: {request.client.host}")
    logger.info(f"任务ID: {task_id}")

    try:
        logger.info("开始获取任务...")
        task = browser_service.get_task(task_id)
        if not task:
            logger.warning(f"任务未找到: {task_id}")
            logger.info("=" * 50)
            raise HTTPException(status_code=404, detail="Task not found")
        logger.info(f"成功获取任务: {task_id}")
        logger.info("=" * 50)
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error("获取任务失败!")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"错误信息: {str(e)}")
        logger.exception("详细错误信息:")
        logger.error("=" * 50)
        raise HTTPException(status_code=500, detail=f"获取任务状态时发生错误: {str(e)}")


@router.websocket("/ws/tasks/{task_id}")
async def task_websocket(websocket: WebSocket, task_id: str):
    """WebSocket 连接处理任务执行过程"""
    logger.info("=" * 50)
    logger.info(f"收到 WebSocket 连接请求: {task_id}")

    try:
        logger.info("接受 WebSocket 连接...")
        await websocket.accept()
        logger.info("WebSocket 连接已接受")

        logger.info("获取任务信息...")
        task = browser_service.get_task(task_id)
        if not task:
            logger.warning(f"WebSocket 连接的任务未找到: {task_id}")
            await websocket.close(code=4004, reason="Task not found")
            return

        logger.info(f"开始执行任务: {task_id}")
        await browser_service.run_task(task, websocket)
        logger.info(f"任务执行完成: {task_id}")

    except Exception as e:
        logger.error("任务执行失败!")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"错误信息: {str(e)}")
        logger.exception("详细错误信息:")
        try:
            await websocket.close(code=1011, reason=str(e))
        except RuntimeError:
            # 忽略已关闭连接的错误
            pass
    finally:
        logger.info(f"关闭 WebSocket 连接: {task_id}")
        logger.info("=" * 50)
        try:
            await websocket.close()
        except RuntimeError:
            # 忽略已关闭连接的错误
            pass
