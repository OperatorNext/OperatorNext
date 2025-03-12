"""
并发测试示例

测试 Browserless 的并发处理能力和性能监控：
1. 同时创建多个浏览器会话
2. 执行不同的任务
3. 监控性能指标
4. 处理超时和错误
"""

import asyncio
import time
from pathlib import Path

import aiohttp

from ..config import check_browserless_status, get_metrics_url, print_status_info
from ..utils import create_browser_client


async def monitor_metrics():
    """监控 Browserless 性能指标"""
    url = get_metrics_url()
    
    async with aiohttp.ClientSession() as session, session.get(url) as response:
        return await response.json()


async def single_browser_task(task_id: int, url: str):
    """单个浏览器任务"""
    print(f"任务 {task_id} 开始...")
    start_time = time.time()
    
    # 创建客户端
    client = await create_browser_client()
    
    try:
        if not client.page:
            raise RuntimeError("页面未正确初始化")
            
        # 访问页面
        await client.page.goto(url)
        
        # 等待页面加载
        await client.page.wait_for_load_state("networkidle")
        
        # 获取页面标题
        title = await client.page.title()
        
        # 创建截图目录
        screenshots_dir = Path(__file__).parent.parent / "screenshots" / "concurrent"
        screenshots_dir.mkdir(exist_ok=True, parents=True)
        
        # 保存截图
        screenshot_path = screenshots_dir / f"task_{task_id}.png"
        await client.page.screenshot(path=str(screenshot_path))
        
        duration = time.time() - start_time
        print(f"任务 {task_id} 完成 - 标题: {title} - 耗时: {duration:.2f}秒")
        
    except Exception as e:
        print(f"任务 {task_id} 失败: {e}")
        raise
        
    finally:
        await client.close()


async def run_concurrent_tasks(num_tasks: int = 5):
    """运行并发任务"""
    # 测试网站列表
    test_urls = [
        "https://example.com",
        "https://browserless.io",
        "https://www.google.com",
        "https://github.com",
        "https://www.python.org"
    ]
    
    print(f"\n开始运行 {num_tasks} 个并发任务...")
    
    # 获取初始指标
    print("\n初始性能指标:")
    initial_metrics = await monitor_metrics()
    
    if isinstance(initial_metrics, list) and len(initial_metrics) > 0:
        latest = initial_metrics[0]
        print(f"CPU 使用率: {latest.get('cpu', 0) * 100:.1f}%")
        print(f"内存使用率: {latest.get('memory', 0) * 100:.1f}%")
        print(f"活跃会话数: {latest.get('maxConcurrent', 0)}")
    
    # 创建任务
    tasks = []
    for i in range(num_tasks):
        url = test_urls[i % len(test_urls)]
        tasks.append(single_browser_task(i + 1, url))
    
    # 并发执行任务
    start_time = time.time()
    await asyncio.gather(*tasks, return_exceptions=True)
    total_duration = time.time() - start_time
    
    # 获取最终指标
    print("\n最终性能指标:")
    final_metrics = await monitor_metrics()
    
    if isinstance(final_metrics, list) and len(final_metrics) > 0:
        latest = final_metrics[0]
        print(f"CPU 使用率: {latest.get('cpu', 0) * 100:.1f}%")
        print(f"内存使用率: {latest.get('memory', 0) * 100:.1f}%")
        print(f"活跃会话数: {latest.get('maxConcurrent', 0)}")
    
    print(f"总耗时: {total_duration:.2f}秒")
    print(f"平均每个任务耗时: {total_duration/num_tasks:.2f}秒")


async def main():
    """运行示例"""
    # 确保 Browserless 服务已启动
    success, metrics = await check_browserless_status()
    if not success:
        return
        
    print("Browserless 服务健康检查通过!")
    print_status_info(metrics)
    
    # 运行并发测试
    await run_concurrent_tasks(8)  # 测试 8 个并发任务


if __name__ == "__main__":
    asyncio.run(main()) 