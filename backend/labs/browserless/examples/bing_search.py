"""
Bing 搜索示例

演示如何使用 Browserless 进行 Bing 搜索，包括：
1. 连接到 Browserless
2. 打开 Bing 搜索页面
3. 输入搜索内容
4. 执行搜索
5. 等待结果加载
6. 截图保存
"""

import asyncio
import time
from pathlib import Path

from ..config import check_browserless_status, print_status_info
from ..utils import create_browser_client


async def wait_for_navigation_complete(page, timeout=45):
    """
    优雅地等待页面导航完成
    
    综合使用多种方法确保页面加载完成：
    1. 等待网络状态
    2. 等待页面内容稳定
    3. 检查页面标题
    """
    print("等待页面导航完成...")
    
    try:
        # 1. 等待网络活动基本完成
        await page.wait_for_load_state("networkidle", timeout=timeout * 1000)
        print("✓ 网络活动已完成")
        
        # 2. 等待一小段时间，让 JS 渲染完成
        await asyncio.sleep(2)
        
        # 3. 检查页面是否包含搜索结果内容
        has_content = await page.evaluate("""() => {
            // 搜索标题通常会改变
            const title = document.title;
            // 内容区域通常会有大量元素
            const contentArea = document.querySelector('main') || document.body;
            const elementCount = contentArea.querySelectorAll('*').length;
            
            // 返回状态信息
            return {
                title,
                elementCount,
                url: window.location.href,
                isSearchResultPage: window.location.href.includes('/search?')
            };
        }""")
        
        print(
            f"✓ 页面信息: 标题='{has_content['title']}',\
                元素数={has_content['elementCount']}"
        )
        print(f"✓ 当前URL: {has_content['url']}")
        
        if has_content['isSearchResultPage']:
            print("✓ 已加载到搜索结果页面")
            return True
        else:
            print("⚠️ 未检测到搜索结果页面，可能仍在主页")
            # 再等待一会儿
            await asyncio.sleep(3)
            return False
            
    except Exception as e:
        print(f"⚠️ 等待页面加载时出现异常: {e}")
        return False


async def bing_search(keyword: str) -> None:
    """
    使用 Bing 搜索指定关键词
    
    Args:
        keyword: 搜索关键词
    """
    print(f"开始 Bing 搜索关键词: {keyword}")
    screenshots_dir = Path(__file__).parent.parent / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    # 创建客户端
    client = await create_browser_client()
    
    try:
        # 确保 page 对象存在
        if not client.page:
            raise RuntimeError("页面未正确初始化")
            
        # 访问 Bing
        print("正在访问 Bing...")
        await client.page.goto("https://www.bing.com")
        
        # 保存初始页面截图（用于调试）
        await client.page.screenshot(
            path=str(screenshots_dir / "bing_initial.png")
        )
        
        # 等待搜索框出现并聚焦
        print("定位搜索框...")
        search_box = await client.page.wait_for_selector('#sb_form_q', timeout=10000)
        await search_box.click()
        
        # 输入搜索关键词
        print(f"输入关键词: {keyword}")
        await search_box.fill(keyword)
        
        # 保存输入关键词后的截图（用于调试）
        await client.page.screenshot(
            path=str(screenshots_dir / "bing_keyword_entered.png")
        )
        
        # 使用回车键提交搜索
        print("按回车键执行搜索...")
        start_time = time.time()
        
        # 简单地按回车并等待页面加载状态
        await search_box.press("Enter")
        
        # 等待页面加载完成
        await wait_for_navigation_complete(client.page)
        
        # 计算加载时间
        load_time = time.time() - start_time
        print(f"页面加载耗时: {load_time:.2f}秒")
        
        # 保存搜索结果截图
        screenshot_path = (
            screenshots_dir / f"bing_search_{keyword.replace(' ', '_')}.png"
        )
        print(f"保存截图到: {screenshot_path}")
        await client.page.screenshot(path=str(screenshot_path), full_page=True)
        
        print("搜索完成！")

    except Exception as e:
        print(f"发生错误: {e}")
        
        # 即使出错也尝试保存当前页面状态
        try:
            error_screenshot = screenshots_dir / f"bing_error_{int(time.time())}.png"
            await client.page.screenshot(path=str(error_screenshot))
            print(f"已保存错误状态截图: {error_screenshot}")
        except Exception as e:
            print(f"无法保存错误状态截图: {e}")

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
    await bing_search("Python Playwright Browserless")


if __name__ == "__main__":
    asyncio.run(main()) 