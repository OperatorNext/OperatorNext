from datetime import datetime
from typing import Dict, List, Literal, Optional, Any
from pydantic import BaseModel, Field, validator
import logging
import json

# 配置日志
logger = logging.getLogger(__name__)

def pretty_print_json(data: Any) -> str:
    """格式化打印 JSON 数据"""
    if isinstance(data, dict):
        # 处理字典中的 datetime 对象
        processed_data = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                processed_data[key] = value.isoformat()
            else:
                processed_data[key] = value
        data = processed_data
    return json.dumps(data, indent=2, ensure_ascii=False)

class BrowserTaskCreate(BaseModel):
    """创建任务的请求模型"""
    task_description: str = Field(..., description="任务描述")
    
    @validator('task_description')
    def validate_task_description(cls, v):
        if not v.strip():
            raise ValueError("任务描述不能为空")
        logger.info("验证任务描述: %s...", v[:100])
        return v.strip()

class BrowserTask(BaseModel):
    """任务模型"""
    task_id: str = Field(..., description="任务ID")
    task_description: str = Field(..., description="任务描述")
    status: Literal["pending", "running", "completed", "failed"] = Field(default="pending", description="任务状态")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    result: Optional[Dict] = Field(default=None, description="任务结果")
    
    def __init__(self, **data):
        super().__init__(**data)
        logger.info("创建任务:\n任务ID: %s\n描述: %s...", self.task_id, self.task_description[:100])
    
    def update_status(self, new_status: str):
        """更新任务状态"""
        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.now()
        logger.info(f"任务 {self.task_id} 状态更新: {old_status} -> {new_status}")

# 将 WSMessageType 改为类型别名
WSMessageType = Literal["step", "result", "error"]

class Action(BaseModel):
    """动作模型"""
    type: str = Field(..., description="动作类型")
    args: Optional[Dict] = Field(default=None, description="动作参数")
    status: Optional[str] = Field(default=None, description="动作执行状态")
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat(), description="动作执行时间")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class StepMessage(BaseModel):
    """步骤消息"""
    step: int = Field(..., description="步骤编号")
    url: str = Field(..., description="当前URL")
    status: str = Field(default="completed", description="步骤状态: pending/running/completed/failed")
    evaluation: str = Field(..., description="评估结果")
    memory: str = Field(..., description="记忆状态")
    next_goal: str = Field(..., description="下一步目标")
    actions: List[Dict] = Field(default_factory=list, description="动作列表")
    screenshot: Optional[str] = Field(default=None, description="步骤截图的Base64编码")
    started_at: str = Field(..., description="步骤开始时间")
    completed_at: str = Field(..., description="步骤完成时间")
    duration: float = Field(default=0.0, description="步骤执行时长(秒)")
    metadata: Dict = Field(default_factory=dict, description="元数据")

    def __init__(self, **data):
        # 处理时间戳
        if isinstance(data.get('started_at'), datetime):
            data['started_at'] = data['started_at'].isoformat()
        if isinstance(data.get('completed_at'), datetime):
            data['completed_at'] = data['completed_at'].isoformat()
        
        # 计算持续时间
        try:
            if isinstance(data.get('started_at'), str) and isinstance(data.get('completed_at'), str):
                start_time = datetime.fromisoformat(data['started_at'])
                end_time = datetime.fromisoformat(data['completed_at'])
                data['duration'] = (end_time - start_time).total_seconds()
        except Exception as e:
            logger.warning("计算持续时间时出错: %s", str(e))
            data['duration'] = 0.0

        # 处理动作列表
        if 'actions' in data:
            processed_actions = []
            for action in data['actions']:
                if isinstance(action, dict):
                    # 确保时间戳是字符串格式
                    if 'timestamp' in action and isinstance(action['timestamp'], datetime):
                        action['timestamp'] = action['timestamp'].isoformat()
                    processed_actions.append(action)
            data['actions'] = processed_actions

        # 处理元数据
        if 'metadata' in data and isinstance(data['metadata'], dict):
            metadata = data['metadata']
            if 'browser_state' in metadata and isinstance(metadata['browser_state'], dict):
                browser_state = metadata['browser_state']
                # 截断 screenshot
                if 'screenshot' in browser_state and browser_state['screenshot']:
                    browser_state['screenshot'] = browser_state['screenshot'][:100] + "..."

        super().__init__(**data)
        
        # 记录日志
        logger.info("\n==================================================")
        logger.info("收到步骤回调:")
        logger.info("步骤编号: %d", self.step)
        logger.info("当前URL: %s", self.url)
        logger.info("状态: %s", self.status)
        logger.info("评估结果: %s", self.evaluation)
        logger.info("记忆状态: %s", self.memory)
        logger.info("下一步目标: %s", self.next_goal)
        logger.info("执行时长: %.2f秒", self.duration)
        
        if self.actions:
            logger.info("动作列表:")
            for i, action in enumerate(self.actions, 1):
                logger.info("  动作 %d:\n%s", i, pretty_print_json(action))
        
        logger.info("==================================================")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ResultMessage(BaseModel):
    """结果消息"""
    final_result: str = Field(..., description="最终结果")
    total_steps: int = Field(..., description="总步数")
    success: bool = Field(..., description="是否成功")
    status: str = Field(default="completed", description="任务状态: completed/failed/partial")
    started_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="任务开始时间")
    completed_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="任务完成时间")
    duration: float = Field(default=0.0, description="总执行时长(秒)")
    error_count: int = Field(default=0, description="错误次数")
    retry_count: int = Field(default=0, description="重试次数")
    summary: Optional[str] = Field(default=None, description="任务执行摘要")
    notes: Optional[str] = Field(default=None, description="任务备注")
    metadata: Optional[Dict] = Field(default_factory=dict, description="额外的元数据")
    
    def __init__(self, **data):
        if isinstance(data.get('started_at'), datetime):
            data['started_at'] = data['started_at'].isoformat()
        if isinstance(data.get('completed_at'), datetime):
            data['completed_at'] = data['completed_at'].isoformat()
            
        if 'completed_at' in data and 'started_at' in data:
            try:
                start_time = datetime.fromisoformat(data['started_at'])
                end_time = datetime.fromisoformat(data['completed_at'])
                data['duration'] = (end_time - start_time).total_seconds()
            except Exception as e:
                logger.warning("计算持续时间时出错: %s", str(e))
                data['duration'] = 0.0
                
        super().__init__(**data)
        logger.info("\n" + "=" * 50)
        logger.info("任务完成:")
        logger.info("最终结果: %s", self.final_result)
        logger.info("总步数: %d", self.total_steps)
        logger.info("状态: %s", self.status)
        logger.info("执行时长: %.2f秒", self.duration)
        logger.info("是否成功: %s", "✓" if self.success else "✗")
        if self.error_count:
            logger.info("错误次数: %d", self.error_count)
        if self.retry_count:
            logger.info("重试次数: %d", self.retry_count)
        if self.summary:
            logger.info("执行摘要: %s", self.summary)
        if self.notes:
            logger.info("备注: %s", self.notes)
        logger.info("=" * 50)

class ErrorMessage(BaseModel):
    """错误消息"""
    error: str = Field(..., description="错误信息")
    error_type: str = Field(default="unknown", description="错误类型")
    severity: str = Field(default="error", description="错误严重程度: warning/error/critical")
    details: Optional[Dict] = Field(default=None, description="错误详情")
    traceback: Optional[str] = Field(default=None, description="错误堆栈")
    step: Optional[int] = Field(default=None, description="发生错误的步骤")
    action: Optional[str] = Field(default=None, description="发生错误的动作")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="错误发生时间")
    recoverable: bool = Field(default=True, description="是否可恢复")
    retry_count: int = Field(default=0, description="重试次数")
    notes: Optional[str] = Field(default=None, description="错误备注")
    
    def __init__(self, **data):
        if isinstance(data.get('timestamp'), datetime):
            data['timestamp'] = data['timestamp'].isoformat()
        super().__init__(**data)
        logger.info("\n" + "=" * 50)
        logger.info("发生错误:")
        logger.info("错误类型: %s", self.error_type)
        logger.info("严重程度: %s", self.severity)
        logger.info("错误信息: %s", self.error)
        if self.step is not None:
            logger.info("步骤: %d", self.step)
        if self.action:
            logger.info("动作: %s", self.action)
        if self.details:
            logger.info("错误详情:\n%s", pretty_print_json(self.details))
        if self.traceback:
            logger.info("错误堆栈:\n%s", self.traceback)
        if self.notes:
            logger.info("备注: %s", self.notes)
        logger.info("=" * 50)

class WSMessage(BaseModel):
    """WebSocket 消息"""
    type: WSMessageType = Field(..., description="消息类型")
    data: Dict = Field(..., description="消息数据")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="时间戳")
    session_id: Optional[str] = Field(default=None, description="会话ID")
    sequence: Optional[int] = Field(default=None, description="消息序号")
    metadata: Optional[Dict] = Field(default_factory=dict, description="额外的元数据")
    
    def __init__(self, **data):
        if isinstance(data.get('timestamp'), datetime):
            data['timestamp'] = data['timestamp'].isoformat()
        super().__init__(**data)
        logger.info("\n" + "-" * 50)
        logger.info("WebSocket 消息:")
        logger.info("类型: %s", self.type)
        logger.info("时间: %s", self.timestamp)
        if self.session_id:
            logger.info("会话ID: %s", self.session_id)
        if self.sequence:
            logger.info("序号: %d", self.sequence)
        
        # 处理数据打印，避免打印完整的 base64
        log_data = self.data.copy()
        if isinstance(log_data, dict):
            if 'screenshot' in log_data:
                log_data['screenshot'] = f"{log_data['screenshot'][:50]}... (base64数据已截断)"
            elif isinstance(log_data.get('data'), dict) and 'screenshot' in log_data['data']:
                log_data['data']['screenshot'] = f"{log_data['data']['screenshot'][:50]}... (base64数据已截断)"
        
        logger.info("数据:\n%s", pretty_print_json(log_data))
        if self.metadata:
            logger.info("元数据:\n%s", pretty_print_json(self.metadata))
        logger.info("-" * 50)
        
    @validator('type')
    def validate_message_type(cls, v):
        logger.debug("验证消息类型: %s", v)
        return v 