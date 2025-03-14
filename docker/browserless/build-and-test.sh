#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}开始构建和测试自定义 Browserless 容器...${NC}"

# 确保在项目根目录
cd "$(dirname "$0")/../.." || exit 1

# 停止任何正在运行的 chrome 容器
echo -e "${YELLOW}停止现有的 chrome 容器...${NC}"
docker-compose stop chrome

# 重新构建自定义 browserless 镜像
echo -e "${YELLOW}构建自定义 Browserless 镜像...${NC}"
docker-compose build chrome

# 启动 chrome 服务
echo -e "${YELLOW}启动自定义 Browserless 服务...${NC}"
docker-compose up -d chrome

# 等待服务启动
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 10

# 检查服务是否健康
echo -e "${YELLOW}检查服务健康状态...${NC}"
HEALTH_STATUS=$(curl -s "http://localhost:13000/metrics?token=browser-token-2024")
if [[ $HEALTH_STATUS == *"cpu"* && $HEALTH_STATUS == *"memory"* ]]; then
    echo -e "${GREEN}服务健康状态正常!${NC}"
else
    echo -e "${RED}服务健康状态异常: $HEALTH_STATUS${NC}"
    echo -e "${RED}请检查日志: docker-compose logs chrome${NC}"
    exit 1
fi

# 运行测试脚本
echo -e "${YELLOW}运行功能测试...${NC}"
cd backend || exit 1
python -m labs.browserless.examples.function_api_demo

echo -e "${GREEN}测试完成!${NC}"
echo -e "${YELLOW}如需查看日志，请运行: docker-compose logs chrome${NC}" 