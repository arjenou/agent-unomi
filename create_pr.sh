#!/bin/bash
# 创建 Pull Request 的辅助脚本

echo "=== 创建 Pull Request 步骤 ==="
echo ""

# 检查是否有远程仓库
if git remote | grep -q origin; then
    echo "✓ 检测到远程仓库"
    REMOTE_URL=$(git remote get-url origin)
    echo "  远程仓库: $REMOTE_URL"
    echo ""
    echo "推送分支到远程..."
    git push -u origin feature/add-line-webhook-service
    echo ""
    echo "✓ 分支已推送！"
    echo ""
    echo "接下来："
    echo "1. 访问你的 Git 平台（GitHub/GitLab/Azure DevOps）"
    echo "2. 你会看到提示创建 Pull Request"
    echo "3. 点击创建 PR，选择 base: main <- compare: feature/add-line-webhook-service"
else
    echo "⚠ 未检测到远程仓库"
    echo ""
    echo "请先创建远程仓库，然后运行以下命令："
    echo ""
    echo "  # GitHub 示例"
    echo "  git remote add origin https://github.com/your-username/unomi-agent.git"
    echo "  git push -u origin main"
    echo "  git push -u origin feature/add-line-webhook-service"
    echo ""
    echo "  # 或者 Azure DevOps 示例"
    echo "  git remote add origin https://dev.azure.com/your-org/your-project/_git/unomi-agent"
    echo "  git push -u origin main"
    echo "  git push -u origin feature/add-line-webhook-service"
    echo ""
    echo "然后访问你的 Git 平台创建 Pull Request"
fi

