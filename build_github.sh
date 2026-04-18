#!/bin/bash
# 在线构建APK脚本 - 使用GitHub Actions

set -e

echo "=========================================="
echo "  使用 GitHub Actions 构建 APK"
echo "=========================================="

# 检查是否有git
if ! command -v git &> /dev/null; then
    echo "错误: 需要安装 git"
    exit 1
fi

# 创建临时目录
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "步骤 1: 创建GitHub仓库结构"
echo "------------------------"

# 复制游戏文件
cp -r ~/tamagotchi_game/* .

# 初始化git仓库
git init
git add .
git commit -m "Initial commit - Pixel Pet Game"

echo ""
echo "步骤 2: 推送到GitHub（需要GitHub账号）"
echo "------------------------"
echo "请按照以下步骤操作："
echo ""
echo "1. 在 GitHub 上创建一个新仓库（比如 pixel-pet）"
echo "2. 运行以下命令："
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/pixel-pet.git"
echo "   git push -u origin main"
echo ""
echo "3. 推送后，GitHub Actions 会自动开始构建"
echo "4. 构建完成后，在仓库的 Actions 页面下载 APK"
echo ""
echo "或者使用下面的自动脚本..."

# 询问是否继续
read -p "是否已创建GitHub仓库？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "请先创建GitHub仓库，然后重新运行此脚本"
    exit 0
fi

read -p "请输入GitHub仓库URL（如 https://github.com/user/repo.git）: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "错误: 仓库URL不能为空"
    exit 1
fi

echo ""
echo "步骤 3: 推送代码"
echo "------------------------"

git remote add origin "$REPO_URL"
git push -u origin main 2>&1 || {
    echo ""
    echo "推送失败。可能需要认证。"
    echo "请手动推送："
    echo "cd $TEMP_DIR"
    echo "git push -u origin main"
    exit 1
}

echo ""
echo "=========================================="
echo "  推送成功！"
echo "=========================================="
echo ""
echo "GitHub Actions 正在构建 APK..."
echo "请访问以下链接查看构建进度："
echo ""
REPO_PATH=$(echo "$REPO_URL" | sed 's/\.git$//' | sed 's/https:\/\/github.com\///')
echo "https://github.com/$REPO_PATH/actions"
echo ""
echo "构建完成后，点击最新的 workflow run，"
echo "在 Artifacts 部分下载 'pixel-pet-apk'"
echo ""
echo "下载后，将 APK 文件复制到："
echo "~/Downloads/"
echo ""
