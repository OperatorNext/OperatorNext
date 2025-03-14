#!/bin/bash

# 启动VNC服务器
vncserver :1 -geometry 1280x800 -depth 24

# 启动NoVNC网页代理
/usr/share/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 0.0.0.0:6080 &

# 设置一个循环来保持容器运行
while true; do
    sleep 10
    # 检查VNC服务器是否还在运行
    if ! pgrep "Xtigervnc" > /dev/null; then
        echo "VNC server has stopped, restarting..."
        vncserver :1 -geometry 1280x800 -depth 24
    fi
    # 检查NoVNC代理是否还在运行
    if ! pgrep "novnc_proxy" > /dev/null; then
        echo "NoVNC proxy has stopped, restarting..."
        /usr/share/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 0.0.0.0:6080 &
    fi
done 