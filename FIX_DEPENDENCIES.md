# 修复依赖未安装问题

## 🔴 问题

错误：`No module named uvicorn`

**原因：** Azure 在部署时没有自动安装 `requirements.txt` 中的依赖。

从日志可以看到：
- `WARNING: Could not find virtual environment directory /home/site/wwwroot/antenv.`
- `WARNING: Could not find package directory /home/site/wwwroot/_oryx_packages_.`

这说明依赖没有被安装。

## ✅ 解决方案

### 方案 1: 使用启动脚本自动安装依赖（推荐）

我已经创建了 `startup.sh` 脚本，它会在启动应用前自动安装依赖。

**在 Azure Portal 中：**

1. 进入 **"配置" (Configuration)** → **"堆栈设置" (Stack settings)**
2. 找到 **"启动命令" (Startup command)**
3. 将启动命令改为：
   ```
   bash startup.sh
   ```
4. 点击 **"应用" (Apply)**
5. 重新部署代码（确保 `startup.sh` 已部署）
6. 重启应用

### 方案 2: 在启动命令中直接安装依赖

**启动命令：**
```bash
pip install -r requirements.txt && python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 方案 3: 确保代码正确部署

1. **提交并推送代码：**
   ```bash
   git add startup.sh requirements.txt
   git commit -m "fix: 添加启动脚本自动安装依赖"
   git push
   ```

2. **在 Azure Portal → "部署中心" (Deployment Center)：**
   - 点击 **"同步" (Sync)** 重新触发部署
   - 查看部署日志，确认 `requirements.txt` 被处理

3. **检查部署日志：**
   - 应该看到类似 "Installing dependencies from requirements.txt" 的消息

## 🚀 立即修复步骤

### 步骤 1: 更新启动命令

在 Azure Portal：
1. **"配置"** → **"堆栈设置"**
2. **启动命令** 改为：`bash startup.sh`
3. 点击 **"应用"**

### 步骤 2: 重新部署代码

```bash
# 在本地
git add startup.sh
git commit -m "fix: 添加启动脚本自动安装依赖"
git push
```

然后在 Azure Portal → **"部署中心"** → 点击 **"同步"**

### 步骤 3: 重启应用

等待部署完成后，重启应用。

## ✅ 验证

修复后，日志应该显示：
- `找到 requirements.txt，开始安装依赖...`
- `依赖安装完成`
- `Application startup complete.`
- `Uvicorn running on http://0.0.0.0:8000`

## 📋 检查清单

- [ ] `startup.sh` 文件已创建并提交
- [ ] `requirements.txt` 在根目录
- [ ] 启动命令已更新为 `bash startup.sh`
- [ ] 代码已重新部署
- [ ] 应用已重启
- [ ] 日志显示依赖安装成功
- [ ] 应用启动成功

