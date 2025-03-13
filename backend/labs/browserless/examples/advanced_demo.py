"""
Browserless 高级 API 示例

演示 Browserless 高级 API 的使用方法，包括：
1. 连接到 Browserless
2. 绕过反爬检测 (unblock API)
3. 结构化抓取内容 (scrape API)
4. 网站性能分析 (performance API)
"""

import asyncio
import base64
import json
import re
import time
from datetime import datetime
from pathlib import Path

from ..config import check_browserless_status, print_status_info
from ..utils import create_http_client


async def demo_unblock_api(client):
    """演示 unblock API"""
    print("\n1. 使用 unblock API 绕过反爬检测...")

    # 创建保存目录
    unblock_dir = Path(__file__).parent.parent / "output" / "advanced_api" / "unblock"
    unblock_dir.mkdir(exist_ok=True, parents=True)

    # 基本使用 - 获取被保护网页的内容
    print("获取被保护网页内容...")
    response = await client.unblock(
        url="https://example.com",
        options={
            "browserWSEndpoint": False,
            "cookies": False,
            "content": True,
            "screenshot": False,
        },
    )

    # 提取标题
    content = response.get("content", "")
    title_match = re.search(r"<title>(.*?)</title>", content)
    title = title_match.group(1) if title_match else "未找到标题"
    print(f"解除阻止页面标题: {title}")
    print(f"内容长度: {len(content)} 字符")

    # 保存内容到文件
    content_path = unblock_dir / "unblocked_content.html"
    with open(content_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"解除阻止内容已保存: {content_path}")

    # 带截图的使用
    print("获取被保护网页截图...")
    screenshot_response = await client.unblock(
        url="https://example.com",
        options={
            "browserWSEndpoint": False,
            "cookies": False,
            "content": False,
            "screenshot": True,
            "waitForSelector": {"selector": "h1", "timeout": 5000},
        },
    )

    # 保存截图
    screenshot_data = screenshot_response.get("screenshot")
    if screenshot_data:
        screenshot_path = unblock_dir / "unblocked_screenshot.png"
        with open(screenshot_path, "wb") as f:
            f.write(base64.b64decode(screenshot_data))
        print(f"解除阻止截图已保存: {screenshot_path}")

    # 获取带浏览器连接端点的响应，用于后续自动化操作
    print("获取带浏览器连接端点的响应...")
    endpoint_response = await client.unblock(
        url="https://example.com",
        options={
            "browserWSEndpoint": True,
            "cookies": True,
            "content": False,
            "screenshot": False,
            "ttl": 30000,
        },
    )

    # 输出连接信息
    browser_ws_endpoint = endpoint_response.get("browserWSEndpoint", "未获取到连接端点")
    cookies = endpoint_response.get("cookies", [])
    cookies_count = len(cookies)
    print(f"获取到浏览器 WebSocket 连接端点 ({browser_ws_endpoint[:30]}...)")
    print(f"获取到 {cookies_count} 个 cookies")

    return {"unblock_dir": unblock_dir, "example_url": "https://example.com"}


async def demo_scrape_api(client, context):
    """演示 scrape API"""
    print("\n2. 使用 scrape API 结构化抓取内容...")

    # 创建保存目录
    scrape_dir = Path(__file__).parent.parent / "output" / "advanced_api" / "scrape"
    scrape_dir.mkdir(exist_ok=True, parents=True)

    # 基本使用 - 抓取网页标题和链接
    print("抓取网页标题和链接...")
    scrape_result = await client.scrape(
        url=context["example_url"],
        options={
            "elements": [{"selector": "h1"}, {"selector": "a"}],
            "gotoOptions": {"timeout": 10000, "waitUntil": "networkidle2"},
        },
    )

    # 解析结果
    data = scrape_result.get("data", [])
    headers = [item for item in data if item.get("selector") == "h1"]
    links = [item for item in data if item.get("selector") == "a"]

    print(f"找到 {len(headers)} 个标题和 {len(links)} 个链接")

    # 输出一些内容
    if headers and headers[0].get("results"):
        print("标题内容:")
        for i, h in enumerate(headers[0].get("results", [])):
            print(f"  {i + 1}. {h.get('text', 'N/A')}")

    if links and links[0].get("results"):
        print("链接内容:")
        for i, link in enumerate(links[0].get("results", [])[:3]):  # 只显示前3个
            attrs = {attr["name"]: attr["value"] for attr in link.get("attributes", [])}
            print(f"  {i + 1}. {link.get('text', 'N/A')} -> {attrs.get('href', 'N/A')}")
        if len(links[0].get("results", [])) > 3:
            print(f"  ...以及其他 {len(links[0].get('results', [])) - 3} 个链接")

    # 保存完整结果到文件
    scrape_path = scrape_dir / "scrape_result.json"
    with open(scrape_path, "w", encoding="utf-8") as f:
        json.dump(scrape_result, f, indent=2)
    print(f"抓取结果已保存: {scrape_path}")

    # 使用等待函数的复杂抓取
    print("\n使用等待选项抓取内容...")
    complex_scrape = await client.scrape(
        url=context["example_url"],
        options={
            "elements": [{"selector": "h1"}, {"selector": "p"}],
            "waitForSelector": {"selector": "p", "timeout": 5000},
        },
    )

    # 解析段落
    paragraphs = [
        item for item in complex_scrape.get("data", []) if item.get("selector") == "p"
    ]
    if paragraphs and paragraphs[0].get("results"):
        print(f"找到 {len(paragraphs[0].get('results', []))} 个段落")
        print("段落内容预览:")
        for i, p in enumerate(paragraphs[0].get("results", [])[:2]):  # 只显示前2个
            text = p.get("text", "N/A")
            print(
                f"  {i + 1}. {text[:100]}..."
                if len(text) > 100
                else f"  {i + 1}. {text}"
            )

    # 保存复杂抓取结果
    complex_path = scrape_dir / "complex_scrape_result.json"
    with open(complex_path, "w", encoding="utf-8") as f:
        json.dump(complex_scrape, f, indent=2)
    print(f"复杂抓取结果已保存: {complex_path}")

    # 尝试 GitHub 抓取
    print("\n抓取 GitHub 页面上的元素...")
    github_scrape = await client.scrape(
        url="https://github.com",
        options={
            "elements": [
                {"selector": "nav a"},
                {"selector": "h1"},
                {"selector": "article"},
            ],
            "gotoOptions": {"waitUntil": "networkidle2", "timeout": 15000},
        },
    )

    # 简单分析 GitHub 结果
    github_data = github_scrape.get("data", [])
    nav_links = [item for item in github_data if item.get("selector") == "nav a"]
    if nav_links and nav_links[0].get("results"):
        link_count = len(nav_links[0].get("results", []))
        print(f"找到 {link_count} 个导航链接")
        print("导航链接预览:")
        for i, link in enumerate(nav_links[0].get("results", [])[:5]):  # 只显示前5个
            text = link.get("text", "").strip()
            if text:
                print(f"  {i + 1}. {text}")

    # 保存 GitHub 抓取结果
    github_path = scrape_dir / "github_scrape_result.json"
    with open(github_path, "w", encoding="utf-8") as f:
        json.dump(github_scrape, f, indent=2)
    print(f"GitHub 抓取结果已保存: {github_path}")

    return {**context, "scrape_dir": scrape_dir}


async def demo_performance_api(client, context):
    """演示 performance API"""
    print("\n3. 使用 performance API 分析网站性能...")

    # 创建保存目录
    perf_dir = Path(__file__).parent.parent / "output" / "advanced_api" / "performance"
    perf_dir.mkdir(exist_ok=True, parents=True)

    # 基本使用 - 只获取性能分析
    print("分析网站性能(仅性能指标)...")
    print("这可能需要一点时间，请耐心等待...")
    performance_result = await client.analyze_performance(
        url=context["example_url"],
        options={
            "config": {
                "extends": "lighthouse:default",
                "settings": {"onlyCategories": ["performance"]},
            }
        },
    )

    # 提取关键指标
    print("\n性能分析结果:")
    categories = performance_result.get("categories", {})
    if "performance" in categories:
        perf_score = categories["performance"].get("score", 0) * 100
        print(f"总体性能评分: {perf_score:.1f}/100")

    # 提取一些关键审核指标
    audits = performance_result.get("audits", {})
    key_metrics = [
        "first-contentful-paint",
        "speed-index",
        "largest-contentful-paint",
        "interactive",
        "total-blocking-time",
        "cumulative-layout-shift",
    ]

    print("\n关键指标:")
    for metric in key_metrics:
        if metric in audits:
            score = audits[metric].get("score", 0) * 100
            display = audits[metric].get("displayValue", "N/A")
            print(
                f"  - {audits[metric].get('title', metric)}: "
                f"{display} (评分: {score:.1f}/100)"
            )

    # 保存完整结果到文件
    perf_path = perf_dir / "performance_result.json"
    with open(perf_path, "w", encoding="utf-8") as f:
        json.dump(performance_result, f, indent=2)
    print(f"性能分析结果已保存: {perf_path}")

    # 完整的可访问性分析
    print("\n分析网站可访问性...")
    print("这可能需要一点时间，请耐心等待...")
    accessibility_result = await client.analyze_performance(
        url=context["example_url"],
        options={
            "config": {
                "extends": "lighthouse:default",
                "settings": {"onlyCategories": ["accessibility"]},
            }
        },
    )

    # 提取可访问性评分
    if "accessibility" in accessibility_result.get("categories", {}):
        access_score = (
            accessibility_result["categories"]["accessibility"].get("score", 0) * 100
        )
        print(f"可访问性评分: {access_score:.1f}/100")

    # 保存可访问性结果
    access_path = perf_dir / "accessibility_result.json"
    with open(access_path, "w", encoding="utf-8") as f:
        json.dump(accessibility_result, f, indent=2)
    print(f"可访问性分析结果已保存: {access_path}")

    # SEO 分析
    print("\n分析网站 SEO...")
    print("这可能需要一点时间，请耐心等待...")
    seo_result = await client.analyze_performance(
        url=context["example_url"],
        options={
            "config": {
                "extends": "lighthouse:default",
                "settings": {"onlyCategories": ["seo"]},
            }
        },
    )

    # 提取 SEO 评分
    if "seo" in seo_result.get("categories", {}):
        seo_score = seo_result["categories"]["seo"].get("score", 0) * 100
        print(f"SEO 评分: {seo_score:.1f}/100")

    # 保存 SEO 结果
    seo_path = perf_dir / "seo_result.json"
    with open(seo_path, "w", encoding="utf-8") as f:
        json.dump(seo_result, f, indent=2)
    print(f"SEO 分析结果已保存: {seo_path}")

    return {**context, "performance_dir": perf_dir}


def get_current_time():
    """获取当前时间字符串"""
    return datetime.now().isoformat()


async def demo_advanced_apis():
    """演示高级 HTTP API"""
    print("开始演示 Browserless 高级 API...")
    start_time = time.time()

    # 创建一个日志目录
    log_dir = Path(__file__).parent.parent / "output" / "logs"
    log_dir.mkdir(exist_ok=True, parents=True)

    # 记录运行结果
    results = {"start_time": get_current_time(), "steps": {}, "success": True}

    # 创建 HTTP 客户端
    client = await create_http_client()
    context = {}

    try:
        # 1. 绕过反爬检测
        try:
            print("\n" + "=" * 50)
            print("步骤 1/3: 绕过反爬检测")
            step_start = time.time()
            context = await demo_unblock_api(client)
            results["steps"]["unblock_api"] = {
                "success": True,
                "duration": time.time() - step_start,
            }
        except Exception as e:
            print(f"绕过反爬检测失败: {e}")
            results["steps"]["unblock_api"] = {"success": False, "error": str(e)}
            # 设置基本上下文以便后续步骤能继续
            unblock_dir = (
                Path(__file__).parent.parent / "output" / "advanced_api" / "unblock"
            )
            unblock_dir.mkdir(exist_ok=True, parents=True)
            context = {"unblock_dir": unblock_dir, "example_url": "https://example.com"}

        # 2. 结构化抓取
        try:
            print("\n" + "=" * 50)
            print("步骤 2/3: 结构化抓取内容")
            step_start = time.time()
            context = await demo_scrape_api(client, context)
            results["steps"]["scrape_api"] = {
                "success": True,
                "duration": time.time() - step_start,
            }
        except Exception as e:
            print(f"结构化抓取失败: {e}")
            results["steps"]["scrape_api"] = {"success": False, "error": str(e)}
            # 确保下一步能继续
            scrape_dir = (
                Path(__file__).parent.parent / "output" / "advanced_api" / "scrape"
            )
            scrape_dir.mkdir(exist_ok=True, parents=True)
            context["scrape_dir"] = scrape_dir

        # 3. 性能分析
        try:
            print("\n" + "=" * 50)
            print("步骤 3/3: 网站性能分析")
            step_start = time.time()
            context = await demo_performance_api(client, context)
            results["steps"]["performance_api"] = {
                "success": True,
                "duration": time.time() - step_start,
            }
        except Exception as e:
            print(f"网站性能分析失败: {e}")
            results["steps"]["performance_api"] = {"success": False, "error": str(e)}

        # 执行总结
        results["end_time"] = get_current_time()
        results["total_duration"] = time.time() - start_time

        # 计算成功率
        success_count = sum(1 for step in results["steps"].values() if step["success"])
        results["success_rate"] = success_count / len(results["steps"]) * 100

        # 输出路径
        print("\n" + "=" * 50)
        print(f"演示完成! 总耗时: {results['total_duration']:.2f}秒")
        print(
            f"成功率: {results['success_rate']:.1f}% "
            f"({success_count}/{len(results['steps'])}步)"
        )

        if context.get("unblock_dir"):
            print(f"反爬内容: {context['unblock_dir']}")
        if context.get("scrape_dir"):
            print(f"抓取内容: {context['scrape_dir']}")
        if context.get("performance_dir"):
            print(f"性能分析: {context['performance_dir']}")

    except Exception as e:
        print(f"演示过程中发生严重错误: {e}")
        results["success"] = False
        results["fatal_error"] = str(e)

    finally:
        # 保存结果日志
        results_path = (
            log_dir / f"advanced_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"执行日志已保存到: {results_path}")

        # 关闭 HTTP 客户端
        try:
            await client.close()
            print("HTTP 客户端已关闭")
        except Exception as e:
            print(f"关闭 HTTP 客户端时出错: {e}")


async def main():
    """运行示例"""
    # 确保 Browserless 服务已启动
    success, metrics = await check_browserless_status()
    if not success:
        return

    print("Browserless 服务健康检查通过!")
    print_status_info(metrics)

    # 运行高级 API 示例
    await demo_advanced_apis()


if __name__ == "__main__":
    asyncio.run(main())
