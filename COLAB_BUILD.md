# 使用 Google Colab 构建 APK

如果本地构建遇到问题，可以使用 Google Colab 免费构建 APK。

## 步骤

### 1. 打开 Google Colab

访问 https://colab.research.google.com

### 2. 创建新笔记本

点击"新建笔记本"

### 3. 运行以下代码

```python
# 第一个单元格：安装依赖
!apt-get update
!apt-get install -y \
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

!pip install buildozer cython==0.29.33
```

```python
# 第二个单元格：上传游戏文件
from google.colab import files
import os

# 创建游戏目录
!mkdir -p /content/tamagotchi_game
%cd /content/tamagotchi_game

# 上传文件（或者从 GitHub 克隆）
# 如果您已将代码推送到 GitHub，取消下面的注释：
# !git clone https://github.com/your-username/tamagotchi-game.git .

print("请上传以下文件：")
print("- main.py")
print("- pet.py")
print("- time_manager.py")
print("- save_system.py")
print("- pixel_pet.py")
print("- food_menu.py")
print("- notifications.py")
print("- buildozer.spec")

# 上传文件
uploaded = files.upload()
```

```python
# 第三个单元格：构建 APK
%cd /content/tamagotchi_game
!buildozer android debug
```

```python
# 第四个单元格：下载 APK
from google.colab import files
import glob

apk_files = glob.glob('bin/*.apk')
if apk_files:
    for apk in apk_files:
        files.download(apk)
else:
    print("未找到 APK 文件")
```

### 4. 等待构建完成

首次构建可能需要 20-30 分钟，因为需要下载 Android SDK 和 NDK。

### 5. 下载 APK

构建完成后，APK 文件会自动下载到您的电脑。

## 注意事项

- Google Colab 的免费版有时间限制（通常 12 小时）
- 首次构建后，后续构建会更快（缓存已下载的工具）
- 如果构建失败，尝试重新运行所有单元格

## 故障排除

### 问题：构建失败
**解决方案：**
1. 检查所有文件是否已上传
2. 确保 buildozer.spec 配置正确
3. 查看错误信息并搜索解决方案

### 问题：内存不足
**解决方案：**
1. 在 Colab 中使用 GPU 运行时（运行时 -> 更改运行时类型）
2. 或者减少构建的目标架构

### 问题：下载速度慢
**解决方案：**
1. 使用 Colab Pro（付费版）
2. 或者在本地构建（推荐使用 Linux）
