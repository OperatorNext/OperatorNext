import asyncio
import traceback
import uuid
import os
import sys
import platform
import psutil
from datetime import datetime
from typing import Dict, Optional, List

from fastapi import WebSocket
from app.models.agent import create_agent
from app.schemas.browser_task import BrowserTask, WSMessage

from .metrics import SystemMetricsCollector
from .error_handler import ErrorHandler
from .callbacks import CallbackManager
from .message_processor import MessageProcessor

class BrowserService:
    """浏览器服务"""
    def __init__(self):
        print("\n=== BrowserService 初始化开始 ===")
        try:
            self.tasks: Dict[str, BrowserTask] = {}
            print("✓ 任务字典初始化成功")
            
            self.task_steps: Dict[str, List[Dict]] = {}
            print("✓ 步骤字典初始化成功")
            
            self.task_result: Dict[str, Dict] = {}
            print("✓ 结果字典初始化成功")
            
            self.task_errors: Dict[str, List[Dict]] = {}
            print("✓ 错误字典初始化成功")
            
            self.task_metadata: Dict[str, Dict] = {}
            print("✓ 元数据字典初始化成功")
            
            self.task_stats: Dict[str, Dict] = {}
            print("✓ 统计数据字典初始化成功")

            # 初始化系统监控
            self.process = psutil.Process(os.getpid())
            self.metrics_collector = SystemMetricsCollector(self.process)
            print("✓ 系统监控初始化成功")
            
            print("=== BrowserService 初始化完成 ===\n")
        except Exception as e:
            print(f"❌ BrowserService 初始化失败: {str(e)}")
            print(f"错误详情:\n{traceback.format_exc()}")
            raise

    def create_task(self, task_description: str) -> BrowserTask:
        """创建新任务"""
        print("\n=== 开始创建任务 ===")
        try:
            print(f"1. 任务描述: {task_description}")
            
            print("2. 生成任务ID...")
            task_id = str(uuid.uuid4())
            print(f"   ✓ 生成的任务ID: {task_id}")
            
            print("3. 创建任务对象...")
            task = BrowserTask(
                task_id=task_id,
                task_description=task_description,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            print("   ✓ 任务对象创建成功")
            
            print("4. 初始化任务相关数据...")
            self.tasks[task_id] = task
            self.task_steps[task_id] = []
            self.task_errors[task_id] = []
            self.task_metadata[task_id] = {
                "browser_info": {},
                "performance_metrics": self.metrics_collector.get_metrics(),
                "environment": {
                    "python_version": sys.version,
                    "platform": platform.platform(),
                    "cpu_count": psutil.cpu_count(),
                    "memory_total": psutil.virtual_memory().total
                }
            }
            self.task_stats[task_id] = {
                "started_at": None,
                "completed_at": None,
                "duration": 0,
                "step_count": 0,
                "error_count": 0,
                "retry_count": 0,
                "last_activity": datetime.now().isoformat(),
                "system_metrics": []  # 用于存储任务执行过程中的系统指标
            }
            print("   ✓ 任务数据初始化成功")
            
            print(f"=== 任务创建成功 (ID: {task_id}) ===\n")
            return task
            
        except Exception as e:
            print("\n❌ 任务创建失败!")
            print(f"错误信息: {str(e)}")
            print(f"错误详情:\n{traceback.format_exc()}")
            raise

    def get_task(self, task_id: str) -> Optional[BrowserTask]:
        """获取任务"""
        print(f"\n=== 获取任务 (ID: {task_id}) ===")
        task = self.tasks.get(task_id)
        if task:
            print("✓ 任务找到")
            print(f"  描述: {task.task_description}")
            print(f"  状态: {task.status}")
            print(f"  步骤数: {len(self.task_steps[task_id])}")
            print(f"  错误数: {len(self.task_errors[task_id])}")
            if task.status == "completed":
                duration = self.task_stats[task_id]["duration"]
                print(f"  执行时长: {duration:.2f}秒")
        else:
            print("❌ 任务未找到")
        print("=== 获取任务结束 ===\n")
        return task

    async def run_task(self, task: BrowserTask, websocket: WebSocket) -> None:
        """运行任务"""
        try:
            # 更新任务状态和开始时间
            task.status = "running"
            task.updated_at = datetime.now()
            self.task_stats[task.task_id]["started_at"] = datetime.now().isoformat()
            self.task_stats[task.task_id]["last_activity"] = datetime.now().isoformat()

            # 如果任务已有缓存的步骤，先发送所有缓存的步骤
            if self.task_steps[task.task_id]:
                print(f"发送缓存的步骤，共 {len(self.task_steps[task.task_id])} 步")
                for cached_message in self.task_steps[task.task_id]:
                    await websocket.send_json(cached_message)
                
                # 如果任务已完成，发送结果消息
                if task.status == "completed" and task.task_id in self.task_result:
                    await websocket.send_json(self.task_result[task.task_id])
                    return

            # 初始化错误处理器
            error_handler = ErrorHandler(self.task_stats, self.task_errors)

            # 初始化消息处理器
            message_processor = MessageProcessor(websocket, task.task_id, error_handler)
            
            # 初始化回调管理器
            callback_manager = CallbackManager(
                task_id=task.task_id,
                task_stats=self.task_stats,
                task_steps=self.task_steps,
                task_result=self.task_result,
                metrics_collector=self.metrics_collector,
                error_handler=error_handler,
                message_queue=message_processor.get_queue()
            )

            # 启动消息处理
            print("1. 启动消息处理...")
            message_processor_task = asyncio.create_task(message_processor.process_messages())
            print("2. 消息处理器启动完成")

            try:
                # 启动 Agent
                print("\n=== 开始创建 Agent ===")
                print("1. 初始化 Agent...")
                agent = create_agent(
                    task=task.task_description,
                    step_callback=callback_manager.create_step_callback(),
                    done_callback=callback_manager.create_done_callback()
                )
                print("2. Agent 初始化完成")
                
                # 验证浏览器连接
                print("\n=== 验证浏览器连接 ===")
                try:
                    browser = agent.browser
                    playwright_browser = await browser.get_playwright_browser()
                    contexts = playwright_browser.contexts
                    print(f"✓ 成功连接到远程浏览器")
                    print(f"✓ 当前活动上下文数: {len(contexts)}")
                    print(f"✓ 浏览器版本: {playwright_browser.version}")
                    print("=== 浏览器连接验证完成 ===\n")
                except Exception as e:
                    print("❌ 浏览器连接验证失败")
                    print(f"错误信息: {str(e)}")
                    raise

                print("\n=== 开始执行任务 ===")
                print("Starting agent.run()...")
                await agent.run()
                print("✓ agent.run() completed")
                await message_processor.get_queue().join()
                print("✓ All messages processed")
                print("=== 任务执行完成 ===\n")
            finally:
                message_processor_task.cancel()
                try:
                    await message_processor_task
                except asyncio.CancelledError:
                    pass

        except Exception as e:
            print(f"Error in run_task: {e}")
            error_handler = ErrorHandler(self.task_stats, self.task_errors)
            error = error_handler.handle_error(task.task_id, e)
            
            # 发送错误消息
            current_time = datetime.now().isoformat()
            error_message = WSMessage(
                type="error",
                data=error.model_dump(),
                timestamp=current_time,
                session_id=task.task_id,
                sequence=1  # 错误消息使用固定序号 1
            )
            error_dict = error_message.model_dump()
            await websocket.send_json(error_dict)
            
            # 更新任务状态
            task.status = "failed"
            task.result = {"error": str(e)}
            task.updated_at = current_time 