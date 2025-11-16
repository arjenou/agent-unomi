# Azure App Service 快速启动指南

## 🚀 三个关键步骤

### 1️⃣ 配置启动命令

在 Azure Portal 中：
- 进入 App Service → **配置** → **常规设置**
- 找到 **启动命令**
- 输入：
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
- 点击 **保存**

### 2️⃣ 设置环境变量

在 Azure Portal 中：
- 进入 App Service → **配置** → **应用程序设置**
- 添加以下设置：

| 名称 | 值 |
|------|-----|
| `LINE_CHANNEL_SECRET` | 从 LINE Developers Console 获取 |
| `LINE_CHANNEL_ACCESS_TOKEN` | 从 LINE Developers Console 获取 |

- 点击 **保存** 并重启应用

### 3️⃣ 部署代码

选择以下任一方式：

**方式 A: Git 部署（推荐）**
1. Azure Portal → **部署中心**
2. 连接 GitHub 仓库：`https://github.com/arjenou/agent-unomi.git`
3. 选择分支：`main`
4. 保存后自动部署

**方式 B: Azure CLI**
```bash
az webapp up --name unomi-agnet --resource-group unomi --runtime "PYTHON:3.14"
```

## ✅ 验证部署

访问健康检查：
```
https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/health
```

应该返回：`{"status":"healthy"}`

## 📝 配置 LINE Webhook

在 LINE Developers Console：
- Webhook URL: `https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/webhook/`
- 点击 **Verify**
- 启用 **Use webhook**

## 🔍 查看日志

Azure Portal → App Service → **日志流**

或使用 CLI：
```bash
az webapp log tail --name unomi-agnet --resource-group unomi
```

## ⚠️ 常见问题

**应用无法启动？**
- 检查启动命令是否正确
- 查看日志流中的错误信息

**502 Bad Gateway？**
- 确认启动命令中的端口是 8000
- 确认使用 `0.0.0.0` 而不是 `127.0.0.1`

**Webhook 验证失败？**
- 检查 `LINE_CHANNEL_SECRET` 是否正确
- 确认 Webhook URL 以 `/webhook/` 结尾

