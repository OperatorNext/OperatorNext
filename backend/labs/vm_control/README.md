# VM 控制模块

VM控制模块提供了一套工具，用于连接到虚拟机、执行鼠标和键盘操作、截取屏幕截图，以及运行自动化任务。该模块主要用于自动化测试、UI操作以及其他需要模拟真实用户行为的场景。

## 🌟 功能特点

- **简单连接**: 轻松连接到基于VNC的虚拟机
- **鼠标操作**: 精确控制鼠标移动和点击
- **键盘输入**: 模拟用户键盘输入和按键
- **屏幕截图**: 捕获虚拟机屏幕截图
- **命令执行**: 直接在虚拟机中执行命令
- **浏览器自动化**: 控制浏览器进行网页操作

## 📋 先决条件

要使用VM控制模块，您需要：

1. Docker与Docker Compose (用于运行虚拟机容器)
2. Python 3.9+
3. 必要的Python依赖库，包括：
   - vncdotool
   - docker-py
   - pillow
   - python-dotenv

## 🛠️ 安装与配置

### 1. 启动VM容器

使用项目根目录的docker-compose.yml启动VM容器：

```bash
docker-compose up -d vmhost
```

### 2. 安装Python依赖

```bash
pip install vncdotool docker pillow python-dotenv
```

### 3. 配置环境变量

可以在项目的.env文件中配置以下环境变量（已为您设置合理默认值）：

```
# VM配置
VM_VNC_HOST=localhost
VM_VNC_PORT=5901
VM_VNC_PASSWORD=ubuntu
```

## 🚀 使用指南

### 基本使用

创建VM客户端并执行操作：

```python
import asyncio
from labs.vm_control import create_vm_client

async def main():
    # 创建VM客户端
    client = await create_vm_client()
    
    try:
        # 获取屏幕截图
        await client.get_screenshot("screenshot.png")
        
        # 移动鼠标并点击
        await client.move_mouse(100, 100)
        await client.click()
        
        # 输入文本
        await client.type_text("Hello, VM!")
        
        # 按下键盘按键
        await client.press_key("Return")
        
    finally:
        # 关闭客户端连接
        await client.close()

asyncio.run(main())
```

### 浏览器自动化

控制VM中的浏览器进行网页操作：

```python
import asyncio
from labs.vm_control import create_vm_client

async def main():
    client = await create_vm_client()
    
    try:
        # 打开Firefox浏览器
        await client.execute_command("DISPLAY=:1 firefox &")
        await asyncio.sleep(3)
        
        # 导航到网页
        await client.run_xdotool("search --onlyvisible --class Firefox windowactivate key ctrl+l")
        await client.type_text("https://www.example.com")
        await client.press_key("Return")
        await asyncio.sleep(3)
        
        # 截取网页截图
        await client.get_screenshot("webpage.png")
        
    finally:
        await client.close()

asyncio.run(main())
```

## 📝 模块API

### VMClient 类

VM客户端类提供与虚拟机交互的主要接口：

- `connect()` - 连接到VM
- `move_mouse(x, y)` - 移动鼠标到指定位置
- `click(button=1)` - 点击鼠标按钮
- `double_click(button=1)` - 双击鼠标按钮
- `type_text(text)` - 输入文本
- `press_key(key)` - 按下键盘按键
- `get_screenshot(save_path=None)` - 获取屏幕截图
- `execute_command(command)` - 在VM中执行命令
- `run_xdotool(command)` - 运行xdotool命令
- `click_at(x, y, button=1)` - 在指定位置点击
- `close()` - 关闭连接

### 辅助函数

- `create_vm_client()` - 创建并初始化VM客户端
- `get_vnc_url()` - 获取VNC服务器URL
- `get_vnc_password()` - 获取VNC服务器密码
- `check_vm_status()` - 检查VM服务状态

## 🔍 示例

查看 `examples` 目录中的示例脚本以获取更多使用指导：

- `simple_vm_operation.py` - 基本VM操作示例
- `browser_automation.py` - 浏览器自动化示例

## 🐞 疑难解答

### 常见问题

1. **无法连接到VM**
   - 确保VM容器已启动: `docker ps | grep vmhost`
   - 检查VNC端口是否可用: `nc -z localhost 5901`
   - 验证VNC密码是否正确

2. **鼠标/键盘操作不生效**
   - 确保VM窗口处于活动状态
   - 检查是否有其他程序捕获了键盘/鼠标事件
   - 尝试先使用`client.run_xdotool("windowactivate")`激活窗口

3. **xdotool命令失败**
   - 确保在VM容器中已安装xdotool
   - 验证DISPLAY环境变量设置正确 