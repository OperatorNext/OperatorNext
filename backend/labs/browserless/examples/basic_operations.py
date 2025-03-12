"""
Browserless 基础操作示例

演示 Browserless 的基本功能：
1. 连接服务
2. 创建新标签页
3. 导航到网页
4. 页面交互
5. 截图和 PDF 导出
"""

import asyncio
from pathlib import Path

from ..config import check_browserless_status, print_status_info
from ..utils import create_browser_client


async def demo_basic_operations():
    """演示基础操作"""
    print("开始演示 Browserless 基础操作...")
    
    # 创建客户端
    client = await create_browser_client()
    
    try:
        # 确保 page 对象存在
        if not client.page:
            raise RuntimeError("页面未正确初始化")
        
        # 1. 访问网页
        print("\n1. 访问网页...")
        await client.page.goto("https://example.com")
        
        # 2. 获取页面标题
        title = await client.page.title()
        print(f"页面标题: {title}")
        
        # 3. 获取页面内容
        heading = await client.page.inner_text("h1")
        print(f"页面标题文本: {heading}")
        
        # 4. 创建新标签页
        print("\n2. 创建新标签页...")
        page2 = await client.context.new_page()
        await page2.goto("https://browserless.io")
        print(f"新标签页标题: {await page2.title()}")
        
        # 5. 在两个标签页之间切换
        print("\n3. 切换标签页...")
        await client.page.bring_to_front()
        print("切回第一个标签页")
        await page2.bring_to_front()
        print("切回第二个标签页")
        
        # 6. 创建输出目录
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # 7. 截图
        print("\n4. 保存截图...")
        screenshot_path = output_dir / "example.png"
        await client.page.screenshot(path=str(screenshot_path))
        print(f"截图已保存到: {screenshot_path}")
        
        # 8. 导出 PDF
        print("\n5. 导出 PDF...")
        pdf_path = output_dir / "example.pdf"
        await client.page.pdf(path=str(pdf_path))
        print(f"PDF 已保存到: {pdf_path}")
        
        # 9. 页面交互
        print("\n6. 页面交互...")
        # 返回第一个页面
        await client.page.goto("https://example.com")
        # 点击链接
        await client.page.click("a[href='https://www.iana.org/domains/example']")
        print("点击了页面上的链接")
        
        print("\n演示完成！")
        
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
    
    # 运行基础操作示例
    await demo_basic_operations()


if __name__ == "__main__":
    asyncio.run(main()) 