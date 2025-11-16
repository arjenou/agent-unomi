# 故障排查指南

## ❌ 当前问题：Application Error

应用返回了 "Application Error" 页面，说明应用没有正确启动。

## 🔍 排查步骤

### 1. 检查应用日志

**在 Azure Portal 中：**

1. 进入 App Service (`unomi-agnet`)
2. 点击左侧 **"日志流" (Log stream)**
3. 查看实时日志输出
4. 查找错误信息

**或使用 Azure CLI：**

```bash
az webapp log tail --name unomi-agnet --resource-group unomi
```

### 2. 检查启动命令

**在 Azure Portal 中：**

1. 进入 **"配置" (Configuration)** → **"堆栈设置" (Stack settings)**
2. 确认 **"启动命令" (Startup command)** 是：
   ```
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```
3. 如果不同，更新为上面的命令
4. 点击 **"应用" (Apply)**
5. 重启应用

### 3. 检查代码部署

**确认代码已正确部署：**

1. 在 Azure Portal → **"部署中心" (Deployment Center)**
2. 查看 **"部署日志" (Deployment logs)**
3. 确认部署成功，没有错误

### 4. 检查依赖项

**可能的问题：**
- `requirements.txt` 中的依赖没有正确安装
- gunicorn 或 uvicorn 没有安装

**解决方案：**

1. 在 Azure Portal → **"高级工具" (Advanced Tools)** → **"Go"**
2. 打开 **"SSH"** 或 **"Bash"**
3. 检查 Python 环境：
   ```bash
   python --version
   pip list
   ```

### 5. 检查文件结构

**确认 `main.py` 文件存在：**

在 Azure Portal → **"高级工具" (Advanced Tools)** → **"SSH"**：

```bash
ls -la
cat main.py
```

### 6. 常见错误和解决方案

#### 错误：ModuleNotFoundError

**原因：** 依赖项没有安装

**解决：**
1. 确认 `requirements.txt` 已部署
2. 在部署中心查看构建日志
3. 可能需要手动安装依赖

#### 错误：gunicorn: command not found

**原因：** gunicorn 没有安装

**解决：**
1. 确认 `requirements.txt` 包含 `gunicorn==21.2.0`
2. 重新部署代码

#### 错误：Address already in use

**原因：** 端口冲突

**解决：**
1. 检查启动命令中的端口
2. 确保使用 `0.0.0.0:8000` 或 `0.0.0.0:$PORT`

#### 错误：Application failed to start

**原因：** 代码有语法错误或运行时错误

**解决：**
1. 查看应用日志
2. 检查 `main.py` 是否有错误
3. 本地测试代码是否正常运行

## 🔧 快速修复步骤

### 步骤 1: 重启应用

在 Azure Portal：
1. 进入 App Service → **"概述" (Overview)**
2. 点击 **"重启" (Restart)** 按钮
3. 等待应用重启

### 步骤 2: 检查日志

1. 打开 **"日志流" (Log stream)**
2. 查看启动过程中的错误信息
3. 复制错误信息用于排查

### 步骤 3: 验证启动命令

1. 进入 **"配置" (Configuration)** → **"堆栈设置" (Stack settings)**
2. 确认启动命令正确
3. 保存并重启

### 步骤 4: 重新部署

如果以上步骤都不行，尝试重新部署：

1. 在 Azure Portal → **"部署中心" (Deployment Center)**
2. 点击 **"同步" (Sync)** 或重新触发部署
3. 等待部署完成
4. 检查部署日志

## 📋 检查清单

- [ ] 应用状态为"正在运行"
- [ ] 启动命令已正确配置
- [ ] 环境变量已设置（LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN）
- [ ] 代码已成功部署
- [ ] 查看日志流，没有错误信息
- [ ] `main.py` 文件存在
- [ ] `requirements.txt` 文件存在
- [ ] 依赖项已安装

## 💡 调试技巧

### 使用 Azure CLI 查看详细信息

```bash
# 查看应用配置
az webapp config show --name unomi-agnet --resource-group unomi

# 查看启动命令
az webapp config show --name unomi-agnet --resource-group unomi --query linuxFxVersion

# 查看环境变量
az webapp config appsettings list --name unomi-agnet --resource-group unomi

# 下载日志
az webapp log download --name unomi-agnet --resource-group unomi --log-file app-logs.zip
```

### 本地测试

在部署到 Azure 之前，先在本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export LINE_CHANNEL_SECRET="your_secret"
export LINE_CHANNEL_ACCESS_TOKEN="your_token"

# 运行应用
python main.py

# 或使用 gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🆘 需要帮助？

如果以上步骤都无法解决问题，请提供：
1. 日志流中的错误信息
2. 部署日志
3. 启动命令配置
4. 环境变量配置（隐藏敏感值）

