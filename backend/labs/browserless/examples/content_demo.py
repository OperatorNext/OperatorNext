"""
Browserless 基本内容 API 示例

演示 Browserless 基本内容 API 的使用方法，包括：
1. 连接到 Browserless
2. 获取网页内容 (content API)
3. 网页截图 (screenshot API)
4. 生成 PDF (pdf API)
"""

import asyncio
import json
import re
import time
from datetime import datetime
from pathlib import Path

from ..config import check_browserless_status, print_status_info
from ..utils import create_http_client


async def demo_content_api(client):
    """演示 content API"""
    print("\n1. 使用 content API 获取网页内容...")

    # 基本使用 - 获取网页内容
    content = await client.get_content(
        url="https://example.com", goto_options={"waitUntil": "networkidle2"}
    )

    # 提取标题
    title_match = re.search(r"<title>(.*?)</title>", content)
    title = title_match.group(1) if title_match else "未找到标题"
    print(f"页面标题: {title}")

    # 提取主标题文本
    h1_match = re.search(r"<h1>(.*?)</h1>", content)
    h1_text = h1_match.group(1) if h1_match else "未找到主标题"
    print(f"主标题文本: {h1_text}")

    # 获取 GitHub 页面内容
    github_content = await client.get_content(
        url="https://github.com",
        goto_options={"waitUntil": "networkidle2", "timeout": 10000},
    )

    print(f"Github 页面内容长度: {len(github_content)} 字符")

    return {"title": title, "h1_text": h1_text, "example_url": "https://example.com"}


async def demo_screenshot_api(client, context):
    """演示 screenshot API"""
    print("\n2. 使用 screenshot API 截图...")

    # 创建截图保存目录
    screenshots_dir = Path(__file__).parent.parent / "output" / "basic_api"
    screenshots_dir.mkdir(exist_ok=True, parents=True)

    # 基本截图 - 全页面
    basic_screenshot_path = await client.take_screenshot(
        url=context["example_url"],
        output_path=screenshots_dir / "example_basic.png",
        options={"fullPage": True, "type": "png"},
    )
    print(f"基本截图已保存: {basic_screenshot_path}")

    # 使用导航选项 - 等待页面加载完成的截图
    styled_screenshot_path = await client.take_screenshot(
        url=context["example_url"],
        output_path=screenshots_dir / "example_styled.png",
        options={"type": "png"},
        wait_for={"timeout": 5000},  # 使用超时等待
    )
    print(f"样式化截图已保存: {styled_screenshot_path}")

    # GitHub 截图 - 设置导航选项
    github_screenshot_path = await client.take_screenshot(
        url="https://github.com",
        output_path=screenshots_dir / "github.png",
        options={"fullPage": False, "type": "jpeg"},
        wait_for={"timeout": 10000},
    )
    print(f"GitHub 截图已保存: {github_screenshot_path}")

    return {**context, "screenshots_dir": screenshots_dir}


async def demo_pdf_api(client, context):
    """演示 pdf API"""
    print("\n3. 使用 pdf API 生成 PDF...")

    # 创建 PDF 保存目录
    pdf_dir = context["screenshots_dir"].parent

    # 基本 PDF 生成
    basic_pdf_path = await client.generate_pdf(
        url=context["example_url"],
        output_path=pdf_dir / "example_basic.pdf",
        options={
            "format": "A4",
            "printBackground": True,
            "margin": {"top": "1cm", "right": "1cm", "bottom": "1cm", "left": "1cm"},
        },
    )
    print(f"基本 PDF 已保存: {basic_pdf_path}")

    # 使用导航选项的 PDF 生成
    github_pdf_path = await client.generate_pdf(
        url="https://github.com",
        output_path=pdf_dir / "github.pdf",
        options={"format": "A3", "landscape": True},
        goto_options={"waitUntil": "networkidle2", "timeout": 10000},
    )
    print(f"GitHub PDF 已保存: {github_pdf_path}")

    return {**context, "pdf_dir": pdf_dir}


def get_current_time():
    """获取当前时间字符串"""
    return datetime.now().isoformat()


async def demo_basic_apis():
    """演示基本 HTTP API"""
    print("开始演示 Browserless 基本内容 API...")
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
        # 1. 内容获取
        try:
            print("\n" + "=" * 50)
            print("步骤 1/3: 获取网页内容")
            step_start = time.time()
            context = await demo_content_api(client)
            results["steps"]["content_api"] = {
                "success": True,
                "duration": time.time() - step_start,
            }
        except Exception as e:
            print(f"内容获取失败: {e}")
            results["steps"]["content_api"] = {"success": False, "error": str(e)}
            # 提供基础上下文以便后续步骤继续
            context = {
                "title": "Example Domain",
                "h1_text": "Example Domain",
                "example_url": "https://example.com",
            }

        # 2. 网页截图
        try:
            print("\n" + "=" * 50)
            print("步骤 2/3: 网页截图")
            step_start = time.time()
            context = await demo_screenshot_api(client, context)
            results["steps"]["screenshot_api"] = {
                "success": True,
                "duration": time.time() - step_start,
            }
        except Exception as e:
            print(f"网页截图失败: {e}")
            results["steps"]["screenshot_api"] = {"success": False, "error": str(e)}
            # 保证后续步骤能继续
            screenshots_dir = Path(__file__).parent.parent / "output" / "basic_api"
            screenshots_dir.mkdir(exist_ok=True, parents=True)
            context["screenshots_dir"] = screenshots_dir

        # 3. 生成 PDF
        try:
            print("\n" + "=" * 50)
            print("步骤 3/3: 生成 PDF")
            step_start = time.time()
            context = await demo_pdf_api(client, context)
            results["steps"]["pdf_api"] = {
                "success": True,
                "duration": time.time() - step_start,
            }
        except Exception as e:
            print(f"PDF 生成失败: {e}")
            results["steps"]["pdf_api"] = {"success": False, "error": str(e)}

        # 执行总结
        results["end_time"] = get_current_time()
        results["total_duration"] = time.time() - start_time

        # 计算成功率
        success_count = sum(1 for step in results["steps"].values() if step["success"])
        results["success_rate"] = success_count / len(results["steps"]) * 100

        # 输出路径
        print("\n" + "="*50)
        print(f"演示完成! 总耗时: {results['total_duration']:.2f}秒")
        print(
            f"成功率: {results['success_rate']:.1f}% "
            f"({success_count}/{len(results['steps'])}步)"
        )

        if context.get("screenshots_dir"):
            print(f"截图: {context['screenshots_dir']}")
        if context.get("pdf_dir"):
            print(f"PDF: {context['pdf_dir']}")

    except Exception as e:
        print(f"演示过程中发生严重错误: {e}")
        results["success"] = False
        results["fatal_error"] = str(e)

    finally:
        # 保存结果日志
        results_path = (
            log_dir / f"content_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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

    # 运行基本 API 示例
    await demo_basic_apis()


if __name__ == "__main__":
    asyncio.run(main())
