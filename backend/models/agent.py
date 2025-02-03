from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from app.core.prompts import ChineseSystemPrompt
from app.models.llm import create_llm_model

def create_agent(
    task: str,
    step_callback=None,
    done_callback=None,
    headless: bool = False,  # 默认改为有头模式
    disable_security: bool = True,
) -> Agent:
    """创建并配置 Agent 实例"""
    try:
        print("\n=== 创建 Agent ===")
        print(f"任务描述: {task}")
        print(f"浏览器模式: {'无头模式' if headless else '有头模式'}")
        
        # 创建浏览器配置
        browser_config = BrowserConfig(
            headless=headless,  # 有头模式
            disable_security=disable_security,  # 禁用安全特性
            # 连接到browserless Chrome实例
            cdp_url="ws://localhost:13000/playwright/chromium?token=browser-token-2024",  # 使用WebSocket连接
        )
        
        print("\n=== 浏览器配置 ===")
        print(f"CDP URL: {browser_config.cdp_url}")
        print("Chrome 参数:")
        for arg in browser_config.extra_chromium_args:
            print(f"  {arg}")
        print("==================\n")
        
        # 创建浏览器实例
        print("正在创建浏览器实例...")
        browser = Browser(config=browser_config)
        print("✓ 浏览器实例创建成功")
        
        # 创建 LLM 模型
        print("正在创建 LLM 模型...")
        llm = create_llm_model()
        print("✓ LLM 模型创建成功")
        
        # 创建 Agent
        print("正在创建 Agent...")
        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,  # 注入配置好的浏览器实例
            system_prompt_class=ChineseSystemPrompt,
            register_new_step_callback=step_callback,
            register_done_callback=done_callback
        )
        
        print("\n✓ Agent 创建成功")
        print("=== Agent 创建完成 ===\n")
        return agent
        
    except Exception as e:
        print("\n❌ Agent 创建失败!")
        print(f"错误信息: {str(e)}")
        print("详细错误信息:")
        import traceback
        print(f"{traceback.format_exc()}")
        raise 