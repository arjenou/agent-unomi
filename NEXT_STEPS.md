# 下一步操作指南

## ✅ 已完成

- [x] 配置启动命令：`gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`
- [x] 添加环境变量：`LINE_CHANNEL_SECRET`
- [x] 添加环境变量：`LINE_CHANNEL_ACCESS_TOKEN`

## 🚀 下一步：部署代码

### 方法 1: 使用 Azure Portal Git 部署（推荐）

1. **在 Azure Portal 中：**
   - 进入你的 App Service (`unomi-agnet`)
   - 点击左侧 **"部署中心" (Deployment Center)**
   - 选择 **"GitHub"** 作为源
   - 点击 **"授权" (Authorize)** 连接你的 GitHub 账号
   - 选择：
     - **组织**: `arjenou`
     - **项目**: `agent-unomi`
     - **分支**: `main` 或 `feature/add-line-webhook-service`
   - 点击 **"保存" (Save)**

2. **Azure 会自动部署代码**
   - 部署过程可能需要几分钟
   - 可以在 "部署中心" 页面查看部署状态

### 方法 2: 使用 Azure CLI

```bash
# 确保已登录
az login

# 部署代码
az webapp up --name unomi-agnet --resource-group unomi --runtime "PYTHON:3.14"
```

### 方法 3: 使用 VS Code

1. 安装 **Azure App Service** 扩展
2. 在 VS Code 中：
   - 按 `F1` 打开命令面板
   - 输入 "Azure App Service: Deploy to Web App"
   - 选择 `unomi-agnet`
   - 选择要部署的文件夹

## ✅ 验证部署

### 1. 检查应用状态

在 Azure Portal 中：
- 进入 App Service → **"概述" (Overview)**
- 查看 **"状态" (Status)** 应该是 **"正在运行" (Running)**

### 2. 测试健康检查端点

在浏览器中访问：

```
https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/health
```

应该返回：
```json
{"status":"healthy"}
```

或访问：
```
https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/
```

应该返回：
```json
{
  "status": "ok",
  "service": "LINE Webhook Service",
  "message": "服务正在运行"
}
```

### 3. 查看应用日志

在 Azure Portal 中：
- 进入 App Service → **"日志流" (Log stream)**
- 查看实时日志，确认应用已启动
- 应该看到类似：`Starting gunicorn...` 和 `Application startup complete.`

## 📝 配置 LINE Webhook

### 1. 在 LINE Developers Console 中：

1. 进入 **Messaging API** 页面
2. 找到 **"Webhook settings"** 部分
3. 确认 **Webhook URL** 是：
   ```
   https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/webhook/
   ```
4. 点击 **"Verify"** 按钮验证 webhook
   - ✅ 如果验证成功，会显示 "Success"
   - ❌ 如果失败，检查应用日志

5. 确保 **"Use webhook"** 开关是 **启用** 状态

### 2. 测试 Webhook

1. 用 LINE 扫描你的官方账号的 QR 码
2. 关注你的官方账号
3. 发送一条消息（例如："你好"）
4. 应该收到自动回复："收到您的消息: 你好"

## 🔍 故障排查

### 如果健康检查失败（502/503/404）

1. **检查启动命令是否正确**
   - Azure Portal → 配置 → 堆栈设置
   - 确认启动命令已保存

2. **查看应用日志**
   - Azure Portal → 日志流
   - 查看错误信息

3. **检查环境变量**
   - Azure Portal → 配置 → 环境变量
   - 确认两个变量都存在且值正确

### 如果 Webhook 验证失败

1. **检查应用是否运行**
   - 访问健康检查端点
   - 查看日志流

2. **检查 LINE_CHANNEL_SECRET**
   - 确认值正确（没有多余空格）
   - 确认是从 Basic settings 页面复制的

3. **检查 Webhook URL**
   - 必须以 `/webhook/` 结尾
   - 必须是 HTTPS

### 如果无法发送消息

1. **检查 LINE_CHANNEL_ACCESS_TOKEN**
   - 确认值正确
   - 确认未过期

2. **检查用户是否已关注**
   - Push API 需要用户先关注你的官方账号

## 📋 完整检查清单

- [ ] 代码已部署到 Azure
- [ ] 应用状态为"正在运行"
- [ ] 健康检查端点返回正常
- [ ] 应用日志显示启动成功
- [ ] LINE Webhook URL 已配置
- [ ] Webhook 验证成功
- [ ] "Use webhook" 已启用
- [ ] 测试发送消息并收到回复

## 🎉 完成！

如果以上所有步骤都完成，你的 LINE webhook 服务就已经成功运行了！

现在可以：
- 接收用户消息
- 自动回复消息
- 发送推送消息
- 处理关注/取消关注事件

