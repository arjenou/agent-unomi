#!/bin/bash
# Azure App Service 启动脚本
# 在启动应用前安装依赖

echo "=== 安装 Python 依赖 ==="

# 检查 requirements.txt 是否存在
if [ -f /home/site/wwwroot/requirements.txt ]; then
    echo "找到 requirements.txt，开始安装依赖..."
    pip install --upgrade pip
    pip install -r /home/site/wwwroot/requirements.txt
    echo "依赖安装完成"
else
    echo "警告: 未找到 requirements.txt"
fi

echo "=== 启动应用 ==="

# Azure 会自动设置 PORT 环境变量
PORT=${PORT:-8000}

# 使用 Python 模块方式启动 uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
