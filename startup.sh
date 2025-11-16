#!/bin/bash
# Azure App Service 启动脚本

# Azure 会自动设置 PORT 环境变量
# 如果未设置，默认使用 8000
PORT=${PORT:-8000}

# 启动 FastAPI 应用
# 使用 gunicorn 作为 WSGI 服务器，uvicorn worker 处理异步请求
gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:$PORT \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

