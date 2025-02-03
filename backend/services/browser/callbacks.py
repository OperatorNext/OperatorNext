from datetime import datetime
import traceback
from typing import Any, Dict, Callable
import asyncio
from app.schemas.browser_task import WSMessage, StepMessage, ResultMessage, Action

class CallbackManager:
    """回调管理器"""
    def __init__(self, task_id: str, task_stats: Dict, task_steps: Dict, task_result: Dict,
                 metrics_collector: Any, error_handler: Any, message_queue: asyncio.Queue):
        self.task_id = task_id
        self.task_stats = task_stats
        self.task_steps = task_steps
        self.task_result = task_result
        self.metrics_collector = metrics_collector
        self.error_handler = error_handler
        self.message_queue = message_queue
        self.sequence_number = 0
        self.loop = asyncio.get_event_loop()

    def create_step_callback(self) -> Callable:
        """创建步骤回调函数"""
        def step_callback(state, output, step):
            try:
                self.sequence_number += 1
                current_step = len(self.task_steps[self.task_id]) + 1
                step_start_time = datetime.now()
                
                # 获取系统资源使用情况
                system_metrics = self.metrics_collector.get_metrics()
                self.task_stats[self.task_id]["system_metrics"].append({
                    "timestamp": datetime.now().isoformat(),
                    "step": current_step,
                    "metrics": system_metrics
                })
                
                # 处理浏览器状态
                browser_state = {
                    "url": state.url,
                    "title": getattr(state, 'title', None),
                    "content": getattr(state, 'content', None),
                    "elements": getattr(state, 'elements', None),
                    "screenshot": state.screenshot[:100] + "..." if hasattr(state, 'screenshot') and state.screenshot else None
                }
                
                # 处理动作列表
                actions = []
                for action in output.action:
                    try:
                        action_type = action.__class__.__name__.replace('Action', '').lower()
                        action_args = {k: v for k, v in vars(action).items() if not k.startswith('_')}
                        
                        action_obj = Action(
                            type=action_type,
                            args=action_args,
                            status="pending",
                            timestamp=datetime.now().isoformat()
                        )
                        actions.append(action_obj.model_dump())
                    except Exception as e:
                        print(f"Warning - 处理动作时出错: {str(e)}")
                        continue
                
                # 创建步骤消息
                step_start_time_str = step_start_time.isoformat()
                current_time_str = datetime.now().isoformat()
                
                message = WSMessage(
                    type="step",
                    data=StepMessage(
                        step=current_step,
                        url=state.url,
                        status="completed",
                        evaluation=output.current_state.evaluation_previous_goal,
                        memory=output.current_state.memory,
                        next_goal=output.current_state.next_goal,
                        actions=actions,
                        screenshot=state.screenshot,
                        started_at=step_start_time_str,
                        completed_at=current_time_str,
                        metadata={
                            "browser_state": browser_state,
                            "performance": system_metrics
                        }
                    ).model_dump(),
                    timestamp=current_time_str,
                    session_id=self.task_id,
                    sequence=self.sequence_number
                )
                
                # 更新统计数据
                self.task_stats[self.task_id].update({
                    "step_count": current_step,
                    "last_activity": current_time_str
                })
                
                # 将消息转换为 JSON 格式并缓存
                message_dict = message.model_dump()
                self.task_steps[self.task_id].append(message_dict)
                
                # 发送消息
                self.loop.call_soon_threadsafe(
                    lambda: asyncio.create_task(self.message_queue.put(message_dict))
                )
                
                # 记录简要日志
                print(f"\n步骤 {current_step}: {state.url}")
                print(f"评估: {output.current_state.evaluation_previous_goal}")
                print(f"下一步: {output.current_state.next_goal}")
                
            except Exception as e:
                print(f"Error in step_callback: {e}")
                print(traceback.format_exc())
                self.error_handler.handle_error(self.task_id, e, step=current_step)
        
        return step_callback

    def create_done_callback(self) -> Callable:
        """创建完成回调函数"""
        def done_callback(history):
            try:
                self.sequence_number += 1
                
                # 计算任务统计数据
                total_steps = len(self.task_steps[self.task_id])
                end_time = datetime.now()
                end_time_str = end_time.isoformat()
                start_time = datetime.fromisoformat(self.task_stats[self.task_id]["started_at"])
                duration = (end_time - start_time).total_seconds()
                
                # 更新任务统计
                self.task_stats[self.task_id].update({
                    "completed_at": end_time_str,
                    "duration": duration,
                    "last_activity": end_time_str
                })
                
                # 获取最终结果
                final_result = None
                if history.history and history.history[-1].result:
                    final_result = history.history[-1].result[-1].extracted_content
                
                # 创建结果消息
                result = ResultMessage(
                    final_result=final_result,
                    total_steps=total_steps,
                    success=history.is_done(),
                    status="completed",
                    started_at=self.task_stats[self.task_id]["started_at"],
                    completed_at=end_time_str,
                    duration=duration,
                    error_count=len(self.task_errors[self.task_id]),
                    retry_count=self.task_stats[self.task_id]["retry_count"],
                    summary=f"任务执行完成，共执行 {total_steps} 个步骤，用时 {duration:.2f} 秒",
                    metadata={
                        "performance_metrics": {
                            "average_step_duration": duration / total_steps if total_steps > 0 else 0,
                            "error_rate": len(self.task_errors[self.task_id]) / total_steps if total_steps > 0 else 0
                        }
                    }
                )
                
                message = WSMessage(
                    type="result",
                    data=result.model_dump(),
                    timestamp=end_time_str,
                    session_id=self.task_id,
                    sequence=self.sequence_number
                )
                
                # 将消息转换为 JSON 格式并缓存
                message_dict = message.model_dump()
                self.task_result[self.task_id] = message_dict
                
                # 发送消息
                self.loop.call_soon_threadsafe(
                    lambda: asyncio.create_task(self.message_queue.put(message_dict))
                )
                
                # 记录简要日志
                print(f"\n任务完成:")
                print(f"总步数: {total_steps}")
                print(f"执行时长: {duration:.2f}秒")
                print(f"最终结果: {final_result}")
                
            except Exception as e:
                print(f"Error in done_callback: {e}")
                print(traceback.format_exc())
                self.error_handler.handle_error(self.task_id, e)
        
        return done_callback 