FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    python3 \
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
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip3 install --upgrade pip
RUN pip3 install buildozer cython==0.29.33 kivy==2.3.1

# 创建工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 设置构建脚本权限
RUN chmod +x build.sh

# 暴露端口（如果需要）
# EXPOSE 8000

# 默认命令：构建 APK
CMD ["buildozer", "android", "debug"]
