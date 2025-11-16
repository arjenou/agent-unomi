# 修复 503 Service Unavailable 错误

## 🔴 问题诊断

从日志中可以看到：
```
Error: class uri 'uvicorn.workers.UvicornWorker' invalid or not found
```

**原因：** `uvicorn` 没有正确安装，导致 gunicorn 找不到 `UvicornWorker` 类。

## ✅ 解决方案

### 方案 1: 使用简单的 uvicorn 启动（快速修复）

**在 Azure Portal 中：**

1. 进入 **"配置" (Configuration)** → **"堆栈设置" (Stack settings)**
2. 找到 **"启动命令" (Startup command)**
3. 将启动命令改为：
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
4. 点击 **"应用" (Apply)**
5. 重启应用

**优点：** 简单快速，不需要 gunicorn worker
**缺点：** 单进程，性能较低（但对于 webhook 服务通常足够）

### 方案 2: 确保依赖正确安装（推荐）

**步骤 1: 更新 requirements.txt**

确保 `requirements.txt` 包含：
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.2
python-dotenv==1.0.0
gunicorn==21.2.0
```

**步骤 2: 重新部署代码**

1. 提交更新的 `requirements.txt`：
   ```bash
   git add requirements.txt
   git commit -m "fix: 确保 uvicorn 正确安装"
   git push
   ```

2. 在 Azure Portal → **"部署中心" (Deployment Center)**
   - 点击 **"同步" (Sync)** 重新触发部署
   - 等待部署完成

3. 检查部署日志，确认依赖安装成功

**步骤 3: 使用 gunicorn 启动命令**

启动命令保持为：
```
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 方案 3: 使用标准 gunicorn worker（备用）

如果 uvicorn worker 仍然有问题，可以使用标准 worker：

**启动命令：**
```
gunicorn main:app --workers 4 --bind 0.0.0.0:8000 --timeout 120
```

**注意：** 这不会使用异步 worker，但对于简单的 webhook 服务通常可以工作。

## 🚀 立即修复步骤（推荐方案 1）

1. **Azure Portal** → App Service → **"配置"** → **"堆栈设置"**
2. **启动命令** 改为：`uvicorn main:app --host 0.0.0.0 --port 8000`
3. 点击 **"应用"**
4. 重启应用
5. 等待 1-2 分钟
6. 测试健康检查：`curl https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/health`
7. 在 LINE Developers Console 重新验证 webhook

## ✅ 验证修复

修复后，应该：

1. **健康检查返回正常：**
   ```bash
   curl https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/health
   ```
   应该返回：`{"status":"healthy"}`

2. **日志流显示应用启动成功：**
   - 应该看到：`Application startup complete.`
   - 没有错误信息

3. **LINE Webhook 验证成功：**
   - 在 LINE Developers Console 点击 "Verify"
   - 应该显示成功 ✅

## 📋 检查清单

- [ ] 启动命令已更新
- [ ] 应用已重启
- [ ] 日志流显示应用启动成功
- [ ] 健康检查端点返回正常
- [ ] LINE Webhook 验证成功

