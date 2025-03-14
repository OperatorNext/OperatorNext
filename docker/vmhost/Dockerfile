FROM ubuntu:22.04

# 避免安装过程中的交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 安装Xfce桌面环境、VNC服务器和必要工具
RUN apt-get update && apt-get install -y \
    xfce4 \
    xfce4-goodies \
    x11vnc \
    xvfb \
    xdotool \
    imagemagick \
    firefox-esr \
    sudo \
    curl \
    wget \
    nano \
    scrot \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # 删除不需要的屏幕锁定和电源管理
    && apt-get remove -y xfce4-screensaver xfce4-power-manager || true

# 创建非root用户
RUN useradd -m -s /bin/bash vnc \
    && echo "vnc:vnc" | chpasswd \
    && usermod -aG sudo vnc \
    && echo "vnc ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 切换到非root用户
USER vnc
WORKDIR /home/vnc

# 创建必要的目录
RUN mkdir -p /home/vnc/.vnc /home/vnc/data

# 设置VNC密码
RUN mkdir -p /home/vnc/.vnc && \
    touch /home/vnc/.vnc/passwd && \
    echo "vncpassword" | x11vnc -storepasswd -use-defs /home/vnc/.vnc/passwd

# 添加启动脚本
COPY --chown=vnc:vnc ./start.sh /home/vnc/start.sh
RUN chmod +x /home/vnc/start.sh

# 暴露VNC端口
EXPOSE 5900

# 运行启动脚本
CMD ["/home/vnc/start.sh"] 