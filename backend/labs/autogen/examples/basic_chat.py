"""
基础对话示例

这个示例展示了如何：
1. 创建基本的智能体
2. 启动简单的对话
3. 处理对话结果
"""

import os
import sys

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from labs.autogen.src.agents import (
    create_assistant,
    create_coding_assistant,
    create_user_proxy,
)
from labs.autogen.src.config import get_config


def run_basic_chat(
    message: str,
    is_coding_task: bool = False,
    max_turns: int | None = None
) -> None:
    """
    运行一个基础的对话示例

    Args:
        message: 初始消息
        is_coding_task: 是否是编程任务
        max_turns: 最大对话轮数
    """
    # 创建智能体
    assistant = (create_coding_assistant() if is_coding_task 
                else create_assistant("AI助手"))
    
    user_proxy = create_user_proxy(
        name="用户",
        human_input_mode="TERMINATE"
    )

    # 配置对话参数
    chat_config = get_config("conversation")
    if max_turns:
        chat_config["max_turns"] = max_turns

    # 开始对话
    user_proxy.initiate_chat(
        assistant,
        message=message,
        **chat_config
    )

def main():
    """主函数：运行示例对话"""
    # 编程示例
    print("\n=== 编程任务示例 ===")
    run_basic_chat(
        "请帮我写一个Python函数，实现快速排序算法",
        is_coding_task=True
    )

    # 普通对话示例
    print("\n=== 普通对话示例 ===")
    run_basic_chat(
        "你能解释一下什么是机器学习吗？请用通俗易懂的语言。"
    )

if __name__ == "__main__":
    main() 