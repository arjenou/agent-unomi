# Azure 环境变量配置指南

## 🎯 当前状态

根据你的 Azure Portal 页面，你已经：
- ✅ 添加了 `LINE_CHANNEL_ACCESS_TOKEN`
- ❌ 还需要添加 `LINE_CHANNEL_SECRET`

## 📝 详细步骤

### 1. 获取 LINE_CHANNEL_SECRET

**在 LINE Developers Console：**

1. 打开：https://developers.line.biz/console/channel/2005501631/basic/
2. 或者：
   - 在左侧导航栏点击 **"Basic settings"**
   - 找到 **"Channel secret"** 字段
   - 点击 **"显示" (Show)** 或 **"复制" (Copy)**
   - 复制这个值

### 2. 在 Azure Portal 添加环境变量

你现在已经在 **"环境变量" (Environment variables)** 页面：

1. **点击 "+ 添加" (+ Add) 按钮**

2. **填写新环境变量：**
   ```
   名称: LINE_CHANNEL_SECRET
   值: [粘贴你从 LINE Developers Console 复制的 Channel Secret]
   ```

3. **点击 "确定" (OK)**

4. **确认两个变量都存在：**
   - `LINE_CHANNEL_ACCESS_TOKEN` ✅（已存在）
   - `LINE_CHANNEL_SECRET` ✅（刚添加的）

5. **点击页面底部的 "应用" (Apply) 按钮**

6. **系统会提示重启应用，点击 "继续" (Continue)**

## 📋 环境变量清单

确保以下两个环境变量都已设置：

| 变量名 | 状态 | 值的位置 |
|--------|------|---------|
| `LINE_CHANNEL_SECRET` | ⏳ 待添加 | LINE Developers Console → Basic settings |
| `LINE_CHANNEL_ACCESS_TOKEN` | ✅ 已添加 | LINE Developers Console → Messaging API |

## 🔗 快速链接

- **LINE Basic settings**: https://developers.line.biz/console/channel/2005501631/basic/
- **LINE Messaging API**: https://developers.line.biz/console/channel/2005501631/messaging-api/
- **Azure App Service**: https://portal.azure.com/#@wangyunjie1101gmail.onmicrosoft.com/resource/subscriptions/8c28e7f8-c834-42bb-b317-69ebe04c5277/resourceGroups/unomi/providers/Microsoft.Web/sites/unomi-agnet

## ✅ 完成后验证

1. **检查环境变量**：
   - 在 Azure Portal 确认两个变量都已显示

2. **测试应用**：
   - 访问：https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/health
   - 应该返回：`{"status":"healthy"}`

3. **验证 Webhook**：
   - 在 LINE Developers Console → Messaging API
   - 点击 Webhook URL 旁边的 **"Verify"** 按钮
   - 应该显示验证成功 ✅

