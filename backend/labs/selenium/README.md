# Selenium 实验模块

这个实验模块提供了基于 Selenium Grid 的浏览器自动化能力，并使用桥接模式将抽象和实现分离，实现与 Browserless 的替换关系。

## 架构设计

本模块采用桥接模式设计，将"做什么"和"怎么做"分离：

```
+-----------------------------------+
|                                   |
| BrowserController (高级抽象)        |
| - 页面操作                          |
| - 元素查找                          |
| - 表单操作                          |
+---------------+-------------------+
                |
                v
+-----------------------------------+
|                                   |
| BrowserDriver (实现接口)            |
| - navigate()                      |
| - find_element()                  |
| - click()                         |
| - type()                          |
+---------------+-------------------+
                |
    +-----------+-----------+
    |                       |
    v                       v
+-------------+     +---------------+
|             |     |               |
| SeleniumDriver |  | BrowserlessDriver |
|             |     |               |
+-------------+     +---------------+
```

## 环境配置

已在 docker-compose.yml 中配置了 Selenium Grid 服务：
- Selenium Hub: http://selenium-hub:4444
- 浏览器节点: 
  - Chromium: 支持 x86_64 和 ARM 架构 (在 ARM 架构上替代 Chrome)
  - Firefox: 支持 x86_64 和 ARM 架构
  - Edge: 仅支持 x86_64 架构 (在 Apple Silicon Mac 上不可用)
- VNC 可视化: 
  - Chromium: http://localhost:7900
  - Firefox: http://localhost:7901
  - Edge: http://localhost:7902 (仅 x86_64 架构可用)

## 使用方法

### 基本使用

```python
import asyncio
from labs.selenium.factory import create_browser_controller

async def main():
    # 创建浏览器控制器 (默认使用 Selenium Chromium)
    controller = await create_browser_controller()
    
    try:
        # 打开网页
        await controller.navigate("https://www.example.com")
        
        # 查找元素
        element = await controller.find_element_by_css("h1")
        
        # 获取文本
        text = await controller.get_text(element)
        print(f"页面标题: {text}")
        
        # 点击链接
        link = await controller.find_element_by_text("More information")
        await controller.click(link)
        
        # 等待新页面加载
        await controller.wait_for_navigation()
        
        # 截图
        await controller.save_screenshot("example.png")
        
    finally:
        # 关闭浏览器
        await controller.close()

asyncio.run(main())
```

### 切换浏览器

```python
# 使用 Firefox
controller = await create_browser_controller(browser="firefox")

# 使用 Chromium (在ARM架构上代替Chrome)
controller = await create_browser_controller(browser="chromium")

# 使用 Edge (注意: 在 ARM 架构如 M1/M2 Mac 上不可用)
controller = await create_browser_controller(browser="edge")
```

### 指定自定义选项

```python
options = {
    "headless": False,
    "window_size": (1920, 1080),
    "implicit_wait": 10
}
controller = await create_browser_controller(options=options)
```

## 示例

查看 `examples` 目录中的示例脚本以获取更多使用指导：

- `basic_operations.py` - 基本操作示例
- `form_automation.py` - 表单自动化示例

## 注意事项

1. 需要先启动 Selenium Grid 服务：
   - 对于 x86_64 架构：`docker-compose up -d selenium-hub selenium-chrome selenium-firefox selenium-edge`
   - 对于 ARM 架构 (Apple Silicon Mac)：`docker-compose up -d selenium-hub selenium-chromium selenium-firefox`
2. 要查看浏览器界面，可以访问 VNC 可视化界面：http://localhost:7900
3. 在 ARM 架构 (M系列芯片) 上：
   - 使用 Chromium 代替 Chrome (Google 不为 Linux/ARM 平台构建 Chrome)
   - Firefox 可直接使用
   - Edge 暂不支持 (Microsoft 不为 Linux/ARM 平台构建 Edge)
4. 若需要使用不支持的浏览器，可考虑：
   - 在 x86_64 架构机器上运行
   - 使用兼容的浏览器替代（如用 Chromium 替代 Chrome） 