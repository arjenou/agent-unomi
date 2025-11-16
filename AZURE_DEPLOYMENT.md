# Azure App Service 部署指南

## 步骤 1: 配置启动命令

在 Azure Portal 中配置启动命令：

1. 进入你的 App Service (`unomi-agnet`)
2. 选择 **"配置" (Configuration)** → **"常规设置" (General settings)**
3. 找到 **"启动命令" (Startup Command)** 字段
4. 输入以下命令：

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**注意：** Azure 会自动设置 `PORT` 环境变量，但 gunicorn 命令中我们使用固定端口 8000。如果 Azure 使用其他端口，可以使用：

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

5. 点击 **"保存" (Save)**

## 步骤 2: 配置环境变量

在 Azure Portal 中设置应用程序设置：

1. 进入 **"配置" (Configuration)** → **"应用程序设置" (Application settings)**
2. 点击 **"+ 新建应用程序设置" (+ New application setting)**
3. 添加以下设置：

| 名称 | 值 | 说明 |
|------|-----|------|
| `LINE_CHANNEL_SECRET` | 你的 Channel Secret | 从 LINE Developers Console 获取 |
| `LINE_CHANNEL_ACCESS_TOKEN` | 你的 Channel Access Token | 从 LINE Developers Console 获取 |
| `PORT` | `8000` | 端口号（可选，Azure 会自动设置）|

4. 点击 **"保存" (Save)**
5. 系统会提示重启应用，点击 **"继续" (Continue)**

## 步骤 3: 部署代码

### 方法 A: 使用 Azure CLI（推荐）

```bash
# 登录 Azure
az login

# 设置默认订阅（如果需要）
az account set --subscription "8c28e7f8-c834-42bb-b317-69ebe04c5277"

# 部署代码
az webapp up --name unomi-agnet --resource-group unomi --runtime "PYTHON:3.14"
```

### 方法 B: 使用 Git 部署

1. 在 Azure Portal 中：
   - 进入 App Service → **"部署中心" (Deployment Center)**
   - 选择 **"GitHub"** 或 **"本地 Git"**
   - 连接到你的仓库：`https://github.com/arjenou/agent-unomi.git`
   - 选择分支：`main` 或 `feature/add-line-webhook-service`
   - 点击 **"保存" (Save)**

2. Azure 会自动部署代码

### 方法 C: 使用 VS Code

1. 安装 **Azure App Service** 扩展
2. 在 VS Code 中：
   - 按 `F1` 打开命令面板
   - 输入 "Azure App Service: Deploy to Web App"
   - 选择你的 App Service
   - 选择要部署的文件夹

### 方法 D: 使用 ZIP 部署

```bash
# 创建 ZIP 文件（排除不需要的文件）
zip -r deploy.zip . -x "*.git*" -x "*.env" -x "__pycache__/*" -x "*.pyc"

# 使用 Azure CLI 部署
az webapp deployment source config-zip \
  --resource-group unomi \
  --name unomi-agnet \
  --src deploy.zip
```

## 步骤 4: 验证部署

### 检查应用状态

1. 在 Azure Portal 中：
   - 进入 App Service → **"概述" (Overview)**
   - 查看 **"状态" (Status)** 应该是 **"正在运行" (Running)**

### 测试健康检查端点

访问以下 URL：

```
https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/
```

或

```
https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/health
```

应该返回：
```json
{
  "status": "ok",
  "service": "LINE Webhook Service",
  "message": "服务正在运行"
}
```

### 查看日志

1. 在 Azure Portal 中：
   - 进入 App Service → **"日志流" (Log stream)**
   - 查看实时日志输出

2. 或使用 Azure CLI：
```bash
az webapp log tail --name unomi-agnet --resource-group unomi
```

## 步骤 5: 配置 LINE Webhook

1. 访问 LINE Developers Console
2. 进入你的 Channel → **"Messaging API"**
3. 设置 **Webhook URL**：
   ```
   https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/webhook/
   ```
4. 点击 **"Verify"** 验证 webhook
5. 启用 **"Use webhook"** 开关

## 常见问题排查

### 问题 1: 应用无法启动

**检查：**
- 启动命令是否正确
- `requirements.txt` 是否包含所有依赖
- 查看日志中的错误信息

**解决：**
```bash
# 查看详细日志
az webapp log download --name unomi-agnet --resource-group unomi --log-file app-logs.zip
```

### 问题 2: 502 Bad Gateway

**可能原因：**
- 应用未正确启动
- 端口配置错误
- 启动命令错误

**解决：**
- 检查启动命令中的端口号
- 确保使用 `0.0.0.0` 而不是 `127.0.0.1`
- 检查应用日志

### 问题 3: Webhook 验证失败

**检查：**
- `LINE_CHANNEL_SECRET` 是否正确设置
- Webhook URL 是否正确（必须以 `/webhook/` 结尾）
- 应用是否正在运行

**解决：**
- 在 Azure Portal 中验证环境变量
- 测试健康检查端点
- 查看应用日志

### 问题 4: 无法发送消息

**检查：**
- `LINE_CHANNEL_ACCESS_TOKEN` 是否正确设置
- Access Token 是否过期
- 用户是否已关注你的官方账号

**解决：**
- 在 LINE Developers Console 重新生成 Access Token
- 更新 Azure 中的环境变量
- 重启应用

## 快速检查清单

- [ ] 启动命令已配置
- [ ] 环境变量已设置（LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN）
- [ ] 代码已部署
- [ ] 应用状态为"正在运行"
- [ ] 健康检查端点返回正常
- [ ] LINE Webhook URL 已配置
- [ ] Webhook 验证通过

## 有用的 Azure CLI 命令

```bash
# 查看应用状态
az webapp show --name unomi-agnet --resource-group unomi --query state

# 重启应用
az webapp restart --name unomi-agnet --resource-group unomi

# 查看应用设置
az webapp config appsettings list --name unomi-agnet --resource-group unomi

# 更新应用设置
az webapp config appsettings set --name unomi-agnet --resource-group unomi --settings LINE_CHANNEL_SECRET="your_secret"

# 查看启动命令
az webapp config show --name unomi-agnet --resource-group unomi --query linuxFxVersion

# 设置启动命令
az webapp config set --name unomi-agnet --resource-group unomi --startup-file "gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"
```

