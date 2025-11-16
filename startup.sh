#!/bin/bash
# Azure App Service 启动脚本
# 在启动应用前安装依赖

set -e  # 遇到错误立即退出

echo "=== 当前工作目录 ==="
pwd
echo "=== 列出文件 ==="
ls -la

echo "=== 安装 Python 依赖 ==="

# 切换到应用目录
cd /home/site/wwwroot || cd .

# 检查 requirements.txt 是否存在
if [ -f requirements.txt ]; then
    echo "找到 requirements.txt，开始安装依赖..."
    echo "Python 版本:"
    python --version
    echo "pip 版本:"
    pip --version
    echo "升级 pip..."
    pip install --upgrade pip --user
    echo "安装依赖..."
    pip install --user -r requirements.txt
    echo "验证 uvicorn 安装..."
    python -c "import uvicorn; print('uvicorn 已安装:', uvicorn.__version__)"
    echo "依赖安装完成"
else
    echo "警告: 未找到 requirements.txt"
    echo "当前目录文件列表:"
    ls -la
fi

echo "=== 启动应用 ==="

# Azure 会自动设置 PORT 环境变量
PORT=${PORT:-8000}
echo "使用端口: $PORT"

# 使用 Python 模块方式启动 uvicorn
exec python -m uvicorn main:app --host 0.0.0.0 --port $PORT
