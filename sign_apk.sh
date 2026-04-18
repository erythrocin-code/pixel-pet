#!/bin/bash
# APK签名脚本

set -e

echo "=========================================="
echo "  APK 签名工具"
echo "=========================================="

# 检查参数
if [ $# -lt 1 ]; then
    echo "用法: $0 <apk文件>"
    echo "例如: $0 bin/pixel_pet-1.0.0-debug.apk"
    exit 1
fi

APK_FILE="$1"
SIGNED_APK="${APK_FILE%.apk}-signed.apk"
KEYSTORE="pixel_pet.keystore"
KEY_ALIAS="pixel_pet"

# 检查APK文件是否存在
if [ ! -f "$APK_FILE" ]; then
    echo "错误: APK文件不存在: $APK_FILE"
    exit 1
fi

echo ""
echo "步骤 1: 生成签名密钥"
echo "------------------------"

if [ ! -f "$KEYSTORE" ]; then
    echo "生成新的签名密钥..."
    keytool -genkey -v \
        -keystore "$KEYSTORE" \
        -alias "$KEY_ALIAS" \
        -keyalg RSA \
        -keysize 2048 \
        -validity 10000 \
        -storepass "pixel123" \
        -keypass "pixel123" \
        -dname "CN=Pixel Pet, OU=Development, O=Pixel Pet, L=Beijing, ST=Beijing, C=CN"
    echo "密钥已生成: $KEYSTORE"
else
    echo "使用现有密钥: $KEYSTORE"
fi

echo ""
echo "步骤 2: 对齐APK"
echo "------------------------"

ALIGNED_APK="${APK_FILE%.apk}-aligned.apk"
if command -v zipalign &> /dev/null; then
    echo "使用 zipalign 对齐..."
    zipalign -v 4 "$APK_FILE" "$ALIGNED_APK"
else
    echo "zipalign 未找到，跳过对齐步骤"
    ALIGNED_APK="$APK_FILE"
fi

echo ""
echo "步骤 3: 签名APK"
echo "------------------------"

echo "正在签名..."
apksigner sign \
    --ks "$KEYSTORE" \
    --ks-key-alias "$KEY_ALIAS" \
    --ks-pass pass:"pixel123" \
    --key-pass pass:"pixel123" \
    --out "$SIGNED_APK" \
    "$ALIGNED_APK"

echo ""
echo "步骤 4: 验证签名"
echo "------------------------"

if command -v apksigner &> /dev/null; then
    apksigner verify --verbose "$SIGNED_APK"
else
    echo "apksigner 未找到，跳过验证"
fi

echo ""
echo "=========================================="
echo "  签名完成！"
echo "=========================================="
echo ""
echo "原始APK: $APK_FILE"
echo "签名APK: $SIGNED_APK"
echo ""
echo "安装说明："
echo "1. 将 $SIGNED_APK 传输到手机"
echo "2. 在手机上点击安装"
echo ""
