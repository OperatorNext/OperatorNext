#!/bin/bash

# 设置环境变量
export DISPLAY=:1
export DISPLAY_WIDTH=${DISPLAY_WIDTH:-1280}
export DISPLAY_HEIGHT=${DISPLAY_HEIGHT:-800}
export DISPLAY_DEPTH=${DISPLAY_DEPTH:-24}
export VNC_PASSWORD=${VNC_PASSWORD:-vncpassword}

# 更新VNC密码（如果有提供环境变量）
if [[ "$VNC_PASSWORD" != "vncpassword" ]]; then
    echo "$VNC_PASSWORD" | x11vnc -storepasswd -use-defs ~/.vnc/passwd
fi

echo "启动 Xvfb..."
Xvfb :1 -screen 0 ${DISPLAY_WIDTH}x${DISPLAY_HEIGHT}x${DISPLAY_DEPTH} -ac +extension GLX +render -noreset &
sleep 2

echo "启动 Xfce 桌面环境..."
startxfce4 &
sleep 2

echo "启动 VNC 服务器..."
x11vnc -display :1 -rfbauth ~/.vnc/passwd -forever -shared -rfbport 5900 -bg -o ~/.vnc/x11vnc.log

echo "配置环境完成！"
echo "可以通过VNC客户端连接到端口5900访问桌面"
echo "VNC服务器日志在 ~/.vnc/x11vnc.log"

# 避免容器退出
tail -f /dev/null 