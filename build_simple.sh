#!/bin/bash
# 一键构建脚本 - 适用于有Java环境的系统

set -e

echo "=========================================="
echo "  像素宠物 APK 一键构建脚本"
echo "=========================================="

# 检查Java
if ! command -v java &> /dev/null; then
    echo "错误: 需要安装 Java"
    echo "请访问 https://www.oracle.com/java/technologies/downloads/ 下载安装"
    echo "或使用: brew install openjdk@17"
    exit 1
fi

# 创建临时目录
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "下载游戏源代码..."
# 这里应该是从GitHub下载，但现在我们使用本地文件
cp -r ~/tamagotchi_game/* .

echo "安装依赖..."
pip install buildozer cython==0.29.33

echo "构建APK..."
buildozer android debug

echo "复制APK到下载目录..."
cp bin/*.apk ~/Downloads/pixel_pet.apk

echo "完成！APK已保存到 ~/Downloads/pixel_pet.apk"

# 清理
rm -rf "$TEMP_DIR"
