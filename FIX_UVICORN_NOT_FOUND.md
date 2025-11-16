# 修复 uvicorn: not found 错误

## 🔴 问题

日志显示：
```
/opt/startup/startup.sh: 23: uvicorn: not found
```

**原因：** `uvicorn` 命令不在系统 PATH 中，即使已安装也可能无法直接调用。

## ✅ 解决方案

### 方案 1: 使用 Python 模块方式启动（推荐）

**在 Azure Portal 中：**

1. 进入 **"配置" (Configuration)** → **"堆栈设置" (Stack settings)**
2. 找到 **"启动命令" (Startup command)**
3. 将启动命令改为：
   ```
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```
4. 点击 **"应用" (Apply)**
5. 重启应用

**优点：** 使用 Python 模块方式，确保能找到 uvicorn

### 方案 2: 使用 Python 直接运行（备用）

如果方案 1 不行，可以修改 `main.py` 使其可以直接运行：

启动命令改为：
```
python main.py
```

但需要确保 `main.py` 中的启动代码正确。

### 方案 3: 确保依赖正确安装

问题可能是依赖没有在部署时安装。需要：

1. **确保 `requirements.txt` 在根目录**
2. **重新部署代码**，让 Azure 自动安装依赖
3. **检查部署日志**，确认依赖安装成功

## 🚀 立即修复步骤

1. **Azure Portal** → App Service → **"配置"** → **"堆栈设置"**
2. **启动命令** 改为：`python -m uvicorn main:app --host 0.0.0.0 --port 8000`
3. 点击 **"应用"**
4. 重启应用
5. 等待 1-2 分钟
6. 查看日志流，应该看到应用启动成功

## ✅ 验证

修复后，日志应该显示：
- `Application startup complete.`
- `Uvicorn running on http://0.0.0.0:8000`
- 没有错误信息

然后测试：
```bash
curl https://unomi-agnet-dzg0aghvhsaefybb.japaneast-01.azurewebsites.net/health
```

