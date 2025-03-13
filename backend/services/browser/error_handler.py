import traceback
from datetime import datetime

from schemas.browser_task import ErrorMessage


class ErrorHandler:
    """错误处理器"""
    def __init__(self, task_stats, task_errors):
        self.task_stats = task_stats
        self.task_errors = task_errors

    def handle_error(self, task_id: str, error: Exception, step: int | None = None) -> ErrorMessage:
        """处理错误并记录"""
        current_time = datetime.now().isoformat()
        
        # 特殊处理远程浏览器连接错误
        error_type = error.__class__.__name__
        error_msg = str(error)
        recoverable = True
        
        if "connect_over_cdp" in error_msg or "Failed to connect" in error_msg:
            error_type = "RemoteBrowserConnectionError"
            error_msg = "无法连接到远程浏览器，请确保Docker容器正在运行且9222端口已正确暴露"
            recoverable = False
        
        error_message = ErrorMessage(
            error=error_msg,
            error_type=error_type,
            severity="error",
            details={
                "traceback": traceback.format_exc(),
                "docker_container": "chrome-1",
                "remote_debug_port": "9222"
            },
            step=step,
            timestamp=current_time,
            recoverable=recoverable,
            retry_count=self.task_stats[task_id]["retry_count"]
        )
        
        # 更新统计数据
        self.task_stats[task_id]["error_count"] += 1
        self.task_errors[task_id].append(error_message.model_dump())
        
        return error_message 