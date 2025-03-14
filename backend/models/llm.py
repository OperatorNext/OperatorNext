import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv()

def create_llm_model() -> ChatOpenAI:
    """创建 LLM 模型实例"""
    try:
        print("\n=== 初始化 LLM 模型 ===")
        print(f"Base URL: {os.getenv('OPENAI_API_BASE')}")
        print(f"Model: {os.getenv('OPENAI_MODEL')}")
        
        model = ChatOpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE'),
            model=os.getenv('OPENAI_MODEL')
        )
        print("✓ LLM 模型初始化成功")
        print("=== LLM 模型初始化完成 ===\n")
        return model
    except Exception as e:
        print("❌ LLM 模型初始化失败!")
        print(f"错误信息: {str(e)}")
        import traceback
        print(f"错误详情:\n{traceback.format_exc()}")
        raise 