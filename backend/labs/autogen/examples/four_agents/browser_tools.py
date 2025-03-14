"""
浏览器工具函数

提供浏览器操作相关的工具函数，用于网络浏览、内容提取、表单操作等。
"""

import asyncio

from .sessions import BrowserSession


async def open_website(url: str, wait_for_load: bool = True) -> str:
    """
    使用Selenium在会话中打开网站并获取内容

    Args:
        url: 要访问的网站URL
        wait_for_load: 是否等待页面完全加载，默认为True

    Returns:
        str: 操作结果描述和页面内容
    """
    # 获取或创建浏览器会话
    session = await BrowserSession.get_instance()

    try:
        # 确保控制器已初始化
        if not session.controller:
            return "错误: Selenium浏览器未初始化"

        # 访问网页
        print(f"🌐 正在访问网站: {url}")
        await session.controller.navigate(url)

        # 更新会话状态
        session.current_url = await session.controller.get_current_url()

        # 获取页面标题
        session.current_title = await session.controller.get_title()
        print(f"📄 页面标题: {session.current_title}")

        # 等待额外加载
        if wait_for_load:
            # 等待2秒让页面完全加载
            await asyncio.sleep(2)
            print("✅ 页面加载完成")

        # 获取页面文本内容
        body_text = await session.controller.execute_js(
            "return document.body.innerText;"
        )

        # 构建结果消息
        result = (
            f"成功访问网站: {url}\n"
            f"页面标题: {session.current_title}\n\n"
            f"页面文本内容:\n{body_text[:5000]}..."
            if len(body_text) > 5000
            else body_text
        )

        return result

    except Exception as e:
        error_msg = f"访问网站时出错: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


async def search_on_web(query: str, search_engine: str = "bing") -> str:
    """
    在搜索引擎上执行搜索，并返回搜索结果

    Args:
        query: 搜索查询内容
        search_engine: 搜索引擎选择 (bing, google, duckduckgo)

    Returns:
        str: 搜索结果和操作状态描述
    """
    session = await BrowserSession.get_instance()

    # 根据搜索引擎选择URL和选择器
    engines = {
        "bing": {
            "url": "https://www.bing.com",
            "search_box": "#sb_form_q",
            "search_button": "#search_icon",
            "results_selector": "#b_results",
        },
        "google": {
            "url": "https://www.google.com",
            "search_box": "input[name='q']",
            "search_button": "input[name='btnK']",
            "results_selector": "#search",
        },
        "duckduckgo": {
            "url": "https://duckduckgo.com",
            "search_box": "#search_form_input_homepage",
            "search_button": "#search_button_homepage",
            "results_selector": "#links",
        },
    }

    if search_engine.lower() not in engines:
        return f"错误: 不支持的搜索引擎 '{search_engine}'，支持的引擎有: {', '.join(engines.keys())}"

    engine_data = engines[search_engine.lower()]

    try:
        # 确保控制器已初始化
        if not session.controller:
            return "错误: Selenium浏览器未初始化"

        # 访问搜索引擎
        print(f"🔍 访问搜索引擎: {search_engine}")
        await session.controller.navigate(engine_data["url"])
        await asyncio.sleep(2)  # 等待页面加载

        # 输入搜索查询
        print(f"⌨️ 输入搜索查询: {query}")
        search_box = await session.controller.find_element_by_css(
            engine_data["search_box"]
        )
        if not search_box:
            return f"错误: 未找到搜索框 {engine_data['search_box']}"

        await session.controller.type_text(search_box, query)
        await asyncio.sleep(1)  # 等待输入完成

        # 点击搜索按钮
        print("🖱️ 点击搜索按钮")
        search_button = await session.controller.find_element_by_css(
            engine_data["search_button"]
        )
        if search_button:
            await session.controller.click(search_button)
        else:
            # 如果找不到按钮，尝试按回车键
            await session.controller.press_key("Enter")

        # 等待搜索结果加载
        print("⏳ 等待搜索结果加载...")
        await asyncio.sleep(3)

        # 获取当前URL（可能已重定向到结果页）
        current_url = await session.controller.get_current_url()
        session.current_url = current_url

        # 更新页面标题
        session.current_title = await session.controller.get_title()

        # 尝试获取搜索结果
        print("📑 提取搜索结果...")

        # 使用JavaScript获取搜索结果文本
        results_js = f"""
        const resultsElem = document.querySelector('{engine_data["results_selector"]}');
        if (resultsElem) {{
            // 提取前10个搜索结果
            const items = resultsElem.querySelectorAll('li, .g, .result');
            let results = [];
            let count = 0;
            
            for (let i = 0; i < items.length && count < 10; i++) {{
                const item = items[i];
                // 跳过广告或无关元素
                if (item.textContent.trim().length > 0 && 
                    !item.querySelector('[data-ad]') && 
                    !item.classList.contains('ad')) {{
                    results.push(item.innerText);
                    count++;
                }}
            }}
            
            return results.join('\\n\\n---\\n\\n');
        }} else {{
            return "未找到搜索结果元素";
        }}
        """
        results_text = await session.controller.execute_js(results_js)

        # 构建返回结果
        if not results_text or results_text == "未找到搜索结果元素":
            # 如果找不到结果元素，尝试获取整个页面内容
            body_text = await session.controller.execute_js(
                "return document.body.innerText;"
            )
            # 只返回页面内容的一部分作为结果
            content = body_text[:8000] + ("..." if len(body_text) > 8000 else "")
            return f"搜索查询: {query}\n在 {search_engine} 上的搜索结果 (未能精确提取，显示页面内容):\n\n{content}"
        else:
            return (
                f"搜索查询: {query}\n在 {search_engine} 上的搜索结果:\n\n{results_text}"
            )

    except Exception as e:
        error_msg = f"搜索过程中出错: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


async def screenshot(selector: str = None, filename: str = None) -> str:
    """
    对当前页面或特定元素进行截图

    Args:
        selector: 可选，CSS选择器，指定要截图的元素。为None时截取整个页面
        filename: 可选，截图文件名。为None时使用默认命名

    Returns:
        str: 操作结果描述
    """
    session = await BrowserSession.get_instance()

    try:
        # 确保控制器已初始化
        if not session.controller:
            return "错误: Selenium浏览器未初始化"

        # 设置默认文件名
        if not filename:
            current_url = await session.controller.get_current_url()
            domain = current_url.split("//")[-1].split("/")[0].replace(".", "_")
            filename = f"screenshot_{domain}.png"

        # 确保文件名有.png扩展名
        if not filename.lower().endswith(".png"):
            filename += ".png"

        # 执行截图
        if selector:
            print(f"📷 对元素 {selector} 进行截图...")
            element = await session.controller.find_element_by_css(selector)
            if not element:
                return f"错误: 未找到元素 {selector}"

            await session.controller.screenshot_element(element, filename)
        else:
            print("📷 对整个页面进行截图...")
            await session.controller.screenshot(filename)

        return f"✅ 截图已保存: {filename}"

    except Exception as e:
        error_msg = f"截图过程中出错: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


async def type_text(selector: str, text: str) -> str:
    """
    在指定元素中输入文本

    Args:
        selector: CSS选择器，用于定位要输入文本的元素
        text: 要输入的文本内容

    Returns:
        str: 操作结果描述
    """
    # 获取当前浏览器会话
    session = await BrowserSession.get_instance()

    try:
        # 确保控制器已初始化
        if not session.controller:
            return "错误: Selenium浏览器未初始化"

        # 查找元素
        print(f"🔍 查找元素: {selector}")
        element = await session.controller.find_element_by_css(selector)

        if not element:
            return f"错误: 未找到元素 {selector}"

        # 输入文本
        print(f"⌨️ 在 {selector} 中输入文本: {text}")
        await session.controller.type_text(element, text)

        # 获取元素相关信息
        element_info = await session.controller.execute_js(
            f"const el = document.querySelector('{selector}'); "
            + "return { tag: el.tagName, id: el.id, class: el.className };"
        )

        return f"已成功在 {selector} 中输入文本: '{text}'\n元素信息: {element_info}"

    except Exception as e:
        error_msg = f"输入文本时出错: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


async def execute_js(script: str, selector: str = None) -> str:
    """
    执行JavaScript代码

    Args:
        script: 要执行的JavaScript代码
        selector: 可选的CSS选择器，如果提供，将在该元素上下文中执行脚本

    Returns:
        str: 操作结果描述和脚本执行结果
    """
    # 获取当前浏览器会话
    session = await BrowserSession.get_instance()

    try:
        # 确保控制器已初始化
        if not session.controller:
            return "错误: Selenium浏览器未初始化"

        # 准备执行脚本
        print(
            f"🔧 执行JavaScript代码{' (针对选择器: ' + selector + ')' if selector else ''}"
        )

        # 实际执行脚本
        if selector:
            # 首先查找元素
            element = await session.controller.find_element_by_css(selector)
            if not element:
                return f"错误: 未找到元素 {selector}"

            # 在元素上下文中执行脚本
            modified_script = f"const el = arguments[0]; {script}"
            result = await session.controller.execute_js(modified_script, element)
        else:
            # 在页面上下文中执行脚本
            result = await session.controller.execute_js(script)

        # 更新URL和标题，以防脚本导航到新页面
        session.current_url = await session.controller.get_current_url()
        session.current_title = await session.controller.get_title()

        return f"已成功执行JavaScript代码\n执行结果: {result}"

    except Exception as e:
        error_msg = f"执行JavaScript代码时出错: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


async def get_page_content(content_type: str = "both") -> str:
    """
    获取当前页面的内容，包括HTML源码或DOM结构

    Args:
        content_type: 内容类型，可选值: "html"(HTML源码), "text"(页面文本), "dom"(DOM结构), "both"(HTML和文本)

    Returns:
        str: 页面内容
    """
    # 获取当前浏览器会话
    session = await BrowserSession.get_instance()

    try:
        # 确保控制器已初始化
        if not session.controller:
            return "错误: Selenium浏览器未初始化"

        # 获取页面信息
        current_url = await session.controller.get_current_url()
        page_title = await session.controller.get_title()

        result = f"当前页面: {current_url}\n标题: {page_title}\n\n"

        # 根据请求的内容类型获取页面内容
        if content_type in ["html", "both"]:
            # 获取HTML源码
            html_source = await session.controller.execute_js(
                "return document.documentElement.outerHTML;"
            )
            result += f"HTML源码:\n```html\n{html_source[:5000]}"
            if len(html_source) > 5000:
                result += f"\n... (截断，共{len(html_source)}字符) ..."
            result += "\n```\n\n"

        if content_type in ["text", "both"]:
            # 获取页面文本内容
            text_content = await session.controller.execute_js(
                "return document.body.innerText;"
            )
            result += f"页面文本内容:\n```\n{text_content[:5000]}"
            if len(text_content) > 5000:
                result += f"\n... (截断，共{len(text_content)}字符) ..."
            result += "\n```\n\n"

        if content_type == "dom":
            # 获取简化的DOM结构
            dom_struct = await session.controller.execute_js("""
            function getSimplifiedDOM(node, depth = 0, maxDepth = 5) {
                if (depth > maxDepth) return "...";
                
                let result = "";
                const indent = "  ".repeat(depth);
                
                if (node.nodeType === 1) { // Element node
                    let attrs = "";
                    if (node.id) attrs += ` id="${node.id}"`;
                    if (node.className) attrs += ` class="${node.className}"`;
                    
                    result += `${indent}<${node.tagName.toLowerCase()}${attrs}>\\n`;
                    
                    // Process children
                    for (let i = 0; i < node.childNodes.length; i++) {
                        result += getSimplifiedDOM(node.childNodes[i], depth + 1, maxDepth);
                    }
                    
                    result += `${indent}</${node.tagName.toLowerCase()}>\\n`;
                }
                return result;
            }
            
            return getSimplifiedDOM(document.documentElement, 0, 3);
            """)
            result += f"简化的DOM结构:\n```html\n{dom_struct[:5000]}"
            if len(dom_struct) > 5000:
                result += f"\n... (截断，共{len(dom_struct)}字符) ..."
            result += "\n```"

        return result

    except Exception as e:
        error_msg = f"获取页面内容时出错: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg
