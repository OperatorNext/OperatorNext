import asyncio
from typing import Any

from fastapi import WebSocket


class MessageProcessor:
    """消息处理器"""
    def __init__(self, websocket: WebSocket, task_id: str, error_handler: Any):
        self.websocket = websocket
        self.task_id = task_id
        self.error_handler = error_handler
        self.message_queue = asyncio.Queue()

    async def process_messages(self):
        """处理消息队列"""
        while True:
            try:
                message = await self.message_queue.get()
                print(f"Sending message: {message['type']}, Step: {message['data'].get('step', 'N/A')}")
                await self.websocket.send_json(message)
                self.message_queue.task_done()
            except Exception as e:
                print(f"Error processing message: {e}")
                print(f"Message content: {message}")
                self.error_handler.handle_error(self.task_id, e)
                break

    def get_queue(self) -> asyncio.Queue:
        """获取消息队列"""
        return self.message_queue 