# 像素宠物游戏 - 详细安装指南

## 📱 OPPO Find X8s 安装指南

### 方法一：直接安装 APK（推荐）

1. **获取 APK 文件**
   - 从 GitHub Releases 下载预构建的 APK
   - 或者按照下方说明自行构建

2. **安装 APK**
   - 将 `pixel_pet.apk` 文件复制到手机
   - 打开手机的"文件管理器"
   - 找到 APK 文件并点击
   - 如果提示"禁止安装未知来源应用"：
     - 进入 设置 → 安全 → 更多安全设置
     - 开启"允许安装未知来源应用"
   - 点击"安装"

3. **首次运行**
   - 安装完成后点击"打开"
   - 允许必要的权限（如有）
   - 开始游戏！

### 方法二：使用 QPython 运行（无需构建 APK）

1. **安装 QPython**
   - 在应用商店搜索"QPython"
   - 安装 QPython 3L

2. **下载游戏文件**
   - 下载游戏源代码
   - 将所有 .py 文件复制到手机

3. **运行游戏**
   - 打开 QPython
   - 选择"本地" → 找到 main.py
   - 点击运行

---

## 💻 桌面电脑构建 APK

### 前提条件

- Linux 系统（推荐 Ubuntu 22.04）或 macOS
- Python 3.8+
- 至少 10GB 可用磁盘空间
- 稳定的网络连接

### Ubuntu/Debian 构建步骤

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装依赖
sudo apt install -y \
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
    libssl-dev

# 3. 安装 Python 包
pip install --upgrade pip
pip install buildozer cython==0.29.33

# 4. 下载游戏代码
git clone https://github.com/your-username/pixel-pet.git
cd pixel-pet

# 5. 构建 APK
buildozer android debug

# 6. APK 文件在 bin/ 目录
ls bin/*.apk
```

### macOS 构建步骤

```bash
# 1. 安装 Homebrew（如果没有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 安装依赖
brew install python3 git autoconf automake libtool pkg-config cmake

# 3. 安装 Python 包
pip3 install --upgrade pip
pip3 install buildozer cython==0.29.33

# 4. 构建 APK
cd tamagotchi_game
buildozer android debug
```

### 使用 Docker 构建（最简单）

```bash
# 1. 安装 Docker
# 访问 https://docs.docker.com/get-docker/

# 2. 构建镜像
docker-compose build

# 3. 运行构建
docker-compose up

# 4. APK 文件在 bin/ 目录
ls bin/*.apk
```

---

## ☁️ 使用 Google Colab 构建（免费）

适合没有 Linux 环境的用户。

1. 访问 https://colab.research.google.com
2. 创建新笔记本
3. 复制粘贴 COLAB_BUILD.md 中的代码
4. 运行所有单元格
5. 下载生成的 APK

详细步骤请查看 `COLAB_BUILD.md` 文件。

---

## 🔧 故障排除

### 问题：安装时提示"解析包时出现问题"

**原因**：APK 文件损坏或不完整

**解决方案**：
1. 重新下载 APK 文件
2. 确保下载完整（检查文件大小）
3. 如果是自行构建的，重新构建

### 问题：应用闪退

**原因**：可能是权限问题或兼容性问题

**解决方案**：
1. 检查 Android 版本（需要 7.0+）
2. 清除应用数据：
   - 设置 → 应用管理 → 像素宠物 → 存储 → 清除数据
3. 重新安装应用

### 问题：构建时网络错误

**原因**：网络连接问题

**解决方案**：
1. 检查网络连接
2. 尝试使用代理
3. 使用 GitHub Actions 或 Google Colab 构建

### 问题：构建时内存不足

**原因**：系统内存不足

**解决方案**：
1. 关闭其他程序
2. 增加系统内存（或使用 swap）
3. 使用 Docker 限制内存：`docker run --memory=4g ...`

---

## 📞 获取帮助

如果遇到其他问题：

1. 查看 README.md 中的常见问题
2. 在 GitHub 提交 Issue
3. 查看 Kivy 官方文档：https://kivy.org

---

## 🎮 游戏控制说明

### 基本操作

- **喂食**：点击 🍎 按钮，选择食物
- **玩耍**：点击 🎮 按钮
- **清洁**：点击 🛁 按钮
- **休息**：点击 💤 按钮
- **治疗**：点击 💊 按钮（宠物生病时）

### 时间系统

- 游戏时间与现实时间同步
- 背景颜色随时间变化：
  - 早晨（6-12点）：天蓝色
  - 下午（12-18点）：暖黄色
  - 傍晚（18-21点）：橙色
  - 夜晚（21-6点）：深蓝色

### 睡眠模式

- 点击 🌙 按钮进入睡眠模式
- 宠物会一起休息
- 状态衰减速度减半
- 再次打开时显示"早上好"

---

## 📄 许可证

MIT License - 详见 LICENSE 文件
