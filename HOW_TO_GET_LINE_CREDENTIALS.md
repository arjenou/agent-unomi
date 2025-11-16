# 如何获取 LINE 凭证并配置到 Azure

## 📍 步骤 1: 获取 LINE_CHANNEL_SECRET

在 LINE Developers Console 中：

1. **进入 Basic settings 页面**
   - 在左侧导航栏，点击 **"Basic settings"**（基础设置）
   - 或者直接访问：`https://developers.line.biz/console/channel/2005501631/basic/`

2. **找到 Channel Secret**
   - 在页面中找到 **"Channel secret"** 字段
   - 点击右侧的 **"显示" (Show)** 或 **"复制" (Copy)** 按钮
   - 复制这个值（通常是一串很长的字母数字字符串）

   **注意：** Channel Secret 和 Channel Access Token 是不同的！
   - **Channel Secret**: 用于验证 webhook 签名（在 Basic settings 页面）
   - **Channel Access Token**: 用于发送消息（在 Messaging API 页面）

## 📍 步骤 2: 获取 LINE_CHANNEL_ACCESS_TOKEN

你已经有了这个！在 Messaging API 页面：

1. 找到 **"Channel access token"** 部分
2. 你会看到 **"Channel access token (long-lived)"**
3. 复制这个值（你已经有了：`qnqgTK1jZDKNSu8XwWNchiJTrnwmRaUNlzMoo/0bpNbQl98qpfWVusrFXUAytPDuqPsvMWEkS1fVUooBdV5WeMnOMr23kuimwjEzQXdFPF59T3C0Ijx0WeC7p9QKhOsBcfQl/XuMvLnys06pMJLyLAdB04t89/1O/w1cDnyilFU=`）

## 📍 步骤 3: 在 Azure Portal 中添加环境变量

你现在已经在 Azure Portal 的 **"环境变量" (Environment variables)** 页面了！

### 添加 LINE_CHANNEL_SECRET

1. 点击 **"+ 添加" (+ Add)** 按钮
2. 在弹出窗口中：
   - **名称 (Name)**: 输入 `LINE_CHANNEL_SECRET`
   - **值 (Value)**: 粘贴你从 LINE Developers Console Basic settings 页面复制的 Channel Secret
3. 点击 **"确定" (OK)**

### 确认 LINE_CHANNEL_ACCESS_TOKEN

你已经添加了 `LINE_CHANNEL_ACCESS_TOKEN`，确认一下值是否正确：
- 值应该是：`qnqgTK1jZDKNSu8XwWNchiJTrnwmRaUNlzMoo/0bpNbQl98qpfWVusrFXUAytPDuqPsvMWEkS1fVUooBdV5WeMnOMr23kuimwjEzQXdFPF59T3C0Ijx0WeC7p9QKhOsBcfQl/XuMvLnys06pMJLyLAdB04t89/1O/w1cDnyilFU=`

### 保存更改

1. 确认两个环境变量都已添加：
   - ✅ `LINE_CHANNEL_SECRET`（新添加的）
   - ✅ `LINE_CHANNEL_ACCESS_TOKEN`（已存在）

2. 点击页面底部的 **"应用" (Apply)** 或 **"保存" (Save)** 按钮

3. 系统会提示重启应用，点击 **"继续" (Continue)** 或 **"确定" (OK)**

## ✅ 验证配置

配置完成后，你可以：

1. **测试健康检查端点**：
   ```
   https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/health
   ```

2. **在 LINE Developers Console 验证 Webhook**：
   - 进入 Messaging API 页面
   - 点击 Webhook URL 旁边的 **"Verify"** 按钮
   - 应该显示验证成功

3. **查看应用日志**：
   - Azure Portal → App Service → **"日志流" (Log stream)**
   - 查看是否有错误信息

## 🔍 快速参考

| 变量名 | 在哪里找到 | 用途 |
|--------|-----------|------|
| `LINE_CHANNEL_SECRET` | LINE Developers Console → **Basic settings** | 验证 webhook 签名 |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Developers Console → **Messaging API** | 发送消息到 LINE |

## ⚠️ 常见问题

**Q: 找不到 Channel Secret？**
- 确保你在 **Basic settings** 页面，不是 Messaging API 页面
- 如果看不到，可能需要点击 **"显示" (Show)** 按钮来显示隐藏的值

**Q: 环境变量添加后不生效？**
- 确保点击了 **"保存"** 或 **"应用"** 按钮
- 重启应用（Azure 通常会提示你重启）

**Q: Webhook 验证失败？**
- 检查 `LINE_CHANNEL_SECRET` 是否正确复制（不要有多余的空格）
- 确认应用已重启
- 查看应用日志中的错误信息

