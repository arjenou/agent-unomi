# LINE Webhook Service for Azure App Service

这是一个使用 FastAPI 构建的 LINE webhook 服务，用于接收和处理 LINE 消息，可部署到 Microsoft Azure App Service。

## 功能特性

- ✅ 接收 LINE webhook 事件（消息、关注、取消关注、Postback 等）
- ✅ 验证 LINE webhook 签名
- ✅ 自动回复消息
- ✅ 发送推送消息
- ✅ 健康检查端点

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

在 Azure App Service 中设置以下环境变量：

- `LINE_CHANNEL_SECRET`: LINE Channel Secret（从 LINE Developers Console 获取）
- `LINE_CHANNEL_ACCESS_TOKEN`: LINE Channel Access Token（从 LINE Developers Console 获取）
- `PORT`: 端口号（Azure 会自动设置，通常不需要手动配置）

**在 Azure Portal 中设置环境变量：**
1. 进入你的 App Service
2. 选择 "配置" (Configuration)
3. 在 "应用程序设置" (Application settings) 中添加上述变量
4. 保存并重启应用

### 3. 本地开发

创建 `.env` 文件（参考 `.env.example`）：

```bash
LINE_CHANNEL_SECRET=your_channel_secret_here
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
PORT=8000
```

运行应用：

```bash
python main.py
```

或使用 uvicorn：

```bash
uvicorn main:app --reload --port 8000
```

### 4. 部署到 Azure App Service

#### 方法 1: 使用 Azure CLI

```bash
# 登录 Azure
az login

# 创建资源组（如果还没有）
az group create --name unomi --location japaneast

# 部署代码
az webapp up --name unomi-agnet --resource-group unomi --runtime "PYTHON:3.14"
```

#### 方法 2: 使用 Git 部署

1. 在 Azure Portal 中配置部署中心
2. 连接到你的 Git 仓库
3. Azure 会自动部署代码

#### 方法 3: 使用 VS Code Azure 扩展

1. 安装 Azure App Service 扩展
2. 右键项目文件夹
3. 选择 "Deploy to Web App"

### 5. 配置 LINE Webhook URL

在 LINE Developers Console 中：

1. 进入你的 Channel 设置
2. 在 "Messaging API" 页面
3. 设置 Webhook URL 为：`https://your-app-name.azurewebsites.net/webhook/`
4. 启用 "Use webhook"
5. 点击 "Verify" 验证 webhook

## API 端点

### `GET /`
健康检查端点，返回服务状态。

### `GET /health`
健康检查端点。

### `POST /webhook/`
LINE webhook 端点，接收 LINE 发送的事件。

## 处理的事件类型

- **message**: 用户发送消息
- **follow**: 用户关注你的官方账号
- **unfollow**: 用户取消关注
- **postback**: 用户点击按钮或执行操作

## 注意事项

1. **签名验证**: 所有 webhook 请求都会验证签名，确保请求来自 LINE
2. **Reply Token**: Reply Token 只能使用一次，且必须在收到事件后立即使用
3. **Push API**: 需要用户 ID，通常从事件中获取
4. **环境变量**: 确保在 Azure App Service 中正确设置环境变量

## 故障排除

### Webhook 验证失败

- 检查 `LINE_CHANNEL_SECRET` 是否正确设置
- 确保 webhook URL 以 `/webhook/` 结尾
- 检查 Azure App Service 日志

### 无法发送消息

- 检查 `LINE_CHANNEL_ACCESS_TOKEN` 是否正确设置
- 确认 Access Token 未过期
- 检查用户是否已关注你的官方账号（Push API 需要）

### 查看日志

在 Azure Portal 中：
1. 进入 App Service
2. 选择 "日志流" (Log stream) 查看实时日志
3. 或选择 "日志" (Logs) 查看历史日志

## 开发建议

- 使用 LINE Webhook Simulator 测试 webhook
- 在本地使用 ngrok 测试 webhook（`ngrok http 8000`）
- 查看 LINE Developers 文档了解更多 API 功能

## 许可证

MIT

