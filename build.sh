#!/bin/bash
# 像素宠物游戏 - Android APK 构建脚本
# 适用于 Ubuntu/Debian 系统

set -e

echo "=========================================="
echo "  像素宠物游戏 - Android APK 构建脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否在正确的目录
if [ ! -f "main.py" ]; then
    echo -e "${RED}错误: 请在游戏目录下运行此脚本${NC}"
    exit 1
fi

# 检查系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "检测到 Linux 系统"
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "检测到 macOS 系统"
    OS="macos"
else
    echo -e "${YELLOW}警告: 未测试的系统类型，可能会有问题${NC}"
    OS="unknown"
fi

# 安装依赖函数
install_dependencies_linux() {
    echo "安装 Linux 依赖..."
    sudo apt-get update
    sudo apt-get install -y \
        python3-pip \
        python3-venv \
        build-essential \
        git \
        zip \
        unzip \
        openjdk-17-jdk \
        autoconf \
        libtool \
        pkg-config \
        zlib1g-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libtinfo5 \
        cmake \
        libffi-dev \
        libssl-dev \
        lld
}

install_dependencies_macos() {
    echo "安装 macOS 依赖..."
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}Homebrew 未安装，正在安装...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    brew install \
        python3 \
        git \
        autoconf \
        automake \
        libtool \
        pkg-config \
        cmake
}

# 安装 Python 依赖
install_python_deps() {
    echo "安装 Python 依赖..."
    pip3 install --upgrade pip
    pip3 install buildozer cython==0.29.33
}

# 构建 APK
build_apk() {
    echo "开始构建 APK..."
    echo -e "${YELLOW}注意: 首次构建会下载 Android SDK 和 NDK，可能需要较长时间${NC}"
    
    # 清理之前的构建
    if [ -d ".buildozer" ]; then
        echo "清理之前的构建缓存..."
        rm -rf .buildozer
    fi
    
    if [ -d "bin" ]; then
        rm -rf bin
    fi
    
    # 构建
    buildozer android debug
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}构建成功！${NC}"
        echo "APK 文件位于: bin/"
        ls -la bin/*.apk
    else
        echo -e "${RED}构建失败，请检查错误信息${NC}"
        exit 1
    fi
}

# 主流程
echo ""
echo "步骤 1: 检查并安装依赖"
echo "------------------------"

if [ "$OS" == "linux" ]; then
    read -p "是否安装系统依赖? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_dependencies_linux
    fi
elif [ "$OS" == "macos" ]; then
    read -p "是否安装系统依赖? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_dependencies_macos
    fi
fi

echo ""
echo "步骤 2: 安装 Python 依赖"
echo "------------------------"
read -p "是否安装 Python 依赖? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    install_python_deps
fi

echo ""
echo "步骤 3: 构建 APK"
echo "----------------"
read -p "是否开始构建 APK? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    build_apk
fi

echo ""
echo "=========================================="
echo "  构建完成！"
echo "=========================================="
echo ""
echo "APK 文件位于: bin/"
echo "您可以将 APK 文件传输到手机进行安装"
echo ""
echo "安装说明:"
echo "1. 将 APK 文件复制到手机"
echo "2. 在手机上打开文件管理器"
echo "3. 找到 APK 文件并点击安装"
echo "4. 如果提示\"未知来源\"，请在设置中允许安装"
echo ""
