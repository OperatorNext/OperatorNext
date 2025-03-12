"""
Google 搜索示例

演示如何使用 Browserless 进行 Google 搜索，包括：
1. 连接到 Browserless
2. 打开 Google 搜索页面
3. 输入搜索内容
4. 点击搜索按钮
5. 等待结果加载
6. 截图保存
"""

import asyncio
from pathlib import Path

from ..config import check_browserless_status, print_status_info
from ..utils import create_browser_client


async def google_search(keyword: str) -> None:
    """
    使用 Google 搜索指定关键词
    
    Args:
        keyword: 搜索关键词
    """
    print(f"开始搜索关键词: {keyword}")
    
    # 创建客户端
    client = await create_browser_client()
    
    try:
        # 确保 page 对象存在
        if not client.page:
            raise RuntimeError("页面未正确初始化")
            
        # 访问 Google
        print("正在访问 Google...")
        await client.page.goto("https://www.google.com")
        
        # 等待搜索框出现并聚焦
        print("定位搜索框...")
        search_box = await client.page.wait_for_selector('textarea[name="q"]')
        await search_box.click()
        
        # 输入搜索关键词
        print(f"输入关键词: {keyword}")
        await search_box.fill(keyword)
        await search_box.press("Enter")
        
        # 等待搜索结果加载
        print("等待搜索结果...")
        await client.page.wait_for_load_state("networkidle")
        
        # 创建 screenshots 目录
        screenshots_dir = Path(__file__).parent.parent / "screenshots"
        screenshots_dir.mkdir(exist_ok=True)
        
        # 保存截图
        screenshot_path = (
            screenshots_dir / f"google_search_{keyword.replace(' ', '_')}.png"
        )
        print(f"保存截图到: {screenshot_path}")
        await client.page.screenshot(path=str(screenshot_path), full_page=True)
        
        print("搜索完成！")

    except Exception as e:
        print(f"发生错误: {e}")
        raise

    finally:
        # 关闭连接
        await client.close()


async def main():
    """运行示例"""
    # 确保 Browserless 服务已启动
    success, metrics = await check_browserless_status()
    if not success:
        return
        
    print("Browserless 服务健康检查通过!")
    print_status_info(metrics)
    
    # 运行搜索示例
    await google_search("Python Playwright Browserless")


if __name__ == "__main__":
    asyncio.run(main()) 