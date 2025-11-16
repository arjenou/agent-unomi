#!/bin/bash
# Azure App Service 启动脚本

# 加载环境变量（如果使用 .env 文件）
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# 启动 FastAPI 应用
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}

