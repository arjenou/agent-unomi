#!/bin/bash
# Azure App Service 启动命令
# 在 Azure Portal → 配置 → 常规设置 → 启动命令 中直接使用此命令

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

