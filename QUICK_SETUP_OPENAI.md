# Azure OpenAI 快速配置

## 🚀 立即配置步骤

### 1. 在 Azure Portal 添加环境变量

进入 App Service (`unomi-agnet`) → **"配置"** → **"环境变量"**

添加以下 4 个环境变量：

| 变量名 | 值 |
|--------|-----|
| `AZURE_OPENAI_ENDPOINT` | `https://unomi-agent-ai.openai.azure.com` |
| `AZURE_OPENAI_API_KEY` | `你的API密钥` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | `gpt-4o` |
| `AZURE_OPENAI_API_VERSION` | `2025-01-01-preview` |

### 2. 保存并重启

1. 点击 **"应用" (Apply)**
2. 重启应用

### 3. 重新部署代码

在 **"部署中心" (Deployment Center)** 点击 **"同步" (Sync)** 重新部署代码（安装新的 openai 依赖）

### 4. 测试

1. 用 LINE 发送消息
2. 应该收到 AI 生成的智能回复！

## ✅ 完成！

现在你的 LINE bot 已经集成了 Azure OpenAI，可以智能回复用户消息了。

