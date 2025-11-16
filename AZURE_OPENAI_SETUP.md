# Azure OpenAI 集成配置指南

## 📋 概述

已集成 Azure OpenAI 到 LINE webhook 服务。当用户发送消息时，系统会：
1. 接收用户消息
2. 将消息发送到 Azure OpenAI (gpt-4o)
3. AI 生成智能回复
4. 将 AI 回复发送回 LINE 用户

## 🔧 配置步骤

### 1. 在 Azure Portal 中添加环境变量

在 Azure App Service 的环境变量中添加以下配置：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `AZURE_OPENAI_ENDPOINT` | `https://unomi-agent-ai.openai.azure.com` | Azure OpenAI 端点 |
| `AZURE_OPENAI_API_KEY` | `你的API密钥` | API 密钥（从 Azure Portal 获取） |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | `gpt-4o` | 部署名称（可选，默认 gpt-4o） |
| `AZURE_OPENAI_API_VERSION` | `2025-01-01-preview` | API 版本（可选，默认 2025-01-01-preview） |

### 2. 在 Azure Portal 中设置

1. 进入 App Service (`unomi-agnet`)
2. 点击 **"配置" (Configuration)** → **"环境变量" (Environment variables)**
3. 点击 **"+ 添加" (+ Add)**
4. 添加上述 4 个环境变量
5. 点击 **"应用" (Apply)**
6. 重启应用

### 3. 验证配置

重启后，查看日志流，应该看到应用正常启动。

## 🧪 测试

1. 用 LINE 扫描你的官方账号的 QR 码
2. 关注你的官方账号
3. 发送一条消息（例如："你好，介绍一下你自己"）
4. 应该收到 AI 生成的智能回复

## ⚙️ 自定义 AI 行为

### 修改系统提示词

在 `main.py` 的 `generate_ai_response` 函数中，可以修改系统提示词：

```python
{
    "role": "system",
    "content": "你是一个友好、专业的助手。请用简洁、自然的中文回复用户的消息。"
}
```

例如，可以改为：
- `"你是一个专业的客服助手，专门帮助用户解决问题。"`
- `"你是一个幽默风趣的聊天机器人，用轻松愉快的语气和用户聊天。"`
- `"你是一个技术专家，擅长回答编程和技术问题。"`

### 调整 AI 参数

在 `generate_ai_response` 函数中可以调整：

- `temperature`: 控制回复的创造性（0.0-1.0，默认 0.7）
  - 较低值：更保守、一致的回复
  - 较高值：更创造性、多样化的回复

- `max_tokens`: 最大回复长度（默认 500）
  - 增加：允许更长的回复
  - 减少：限制回复长度

## 🔍 故障排查

### AI 没有回复

1. **检查环境变量**：
   - 确认 `AZURE_OPENAI_ENDPOINT` 和 `AZURE_OPENAI_API_KEY` 已设置
   - 确认值正确（没有多余空格）

2. **查看日志**：
   - 在 Azure Portal → **"日志流" (Log stream)**
   - 查找 "AI 生成回复失败" 的错误信息

3. **测试 API 连接**：
   - 确认 Azure OpenAI 部署状态为 "成功"
   - 确认 API 密钥有效

### 回复太慢

- AI 生成回复可能需要几秒钟
- 如果超时，会返回默认回复
- 可以调整 `httpx.AsyncClient(timeout=30.0)` 的超时时间

### 回复不符合预期

- 修改系统提示词
- 调整 `temperature` 参数
- 检查用户消息是否被正确传递

## 📝 当前配置

- **模型**: gpt-4o
- **API 版本**: 2025-01-01-preview
- **Temperature**: 0.7
- **Max Tokens**: 500
- **超时**: 30 秒

## 🔐 安全提示

- **不要**在代码中硬编码 API 密钥
- **始终**使用环境变量存储敏感信息
- **定期**轮换 API 密钥
- **监控**API 使用量和成本

