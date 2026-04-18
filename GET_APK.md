# 像素宠物游戏 - 获取APK的最简单方法

## 方法一：使用 GitHub Actions（推荐，最简单）

### 步骤：

1. **创建 GitHub 账号**（如果没有）
   - 访问 https://github.com 注册

2. **创建新仓库**
   - 点击右上角 "+" → "New repository"
   - 仓库名：pixel-pet
   - 选择 "Public"
   - 点击 "Create repository"

3. **上传代码**
   - 下载并安装 GitHub Desktop：https://desktop.github.com/
   - 或者使用命令行：
   ```bash
   git clone https://github.com/你的用户名/pixel-pet.git
   cd pixel-pet
   # 将 ~/tamagotchi_game/ 中的所有文件复制到这里
   git add .
   git commit -m "Initial commit"
   git push
   ```

4. **自动构建**
   - 推送代码后，GitHub Actions 会自动开始构建
   - 访问：https://github.com/你的用户名/pixel-pet/actions
   - 等待构建完成（约15-30分钟）

5. **下载APK**
   - 构建完成后，点击最新的 workflow run
   - 在 "Artifacts" 部分下载 "pixel-pet-apk"
   - 解压后得到 APK 文件

6. **安装到手机**
   - 将 APK 传输到手机
   - 在手机上点击安装

---

## 方法二：使用 Google Colab（无需 GitHub）

### 步骤：

1. 访问 https://colab.research.google.com
2. 点击 "新建笔记本"
3. 复制粘贴以下代码并运行：

```python
# 第一个单元格
!apt-get update
!apt-get install -y python3-pip build-essential git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
!pip install buildozer cython==0.29.33
```

```python
# 第二个单元格 - 上传游戏文件
from google.colab import files
import os

!mkdir -p /content/tamagotchi_game
%cd /content/tamagotchi_game

print("请上传以下文件：")
print("- main.py, pet.py, time_manager.py")
print("- save_system.py, pixel_pet.py")
print("- food_menu.py, notifications.py")
print("- buildozer.spec")

uploaded = files.upload()
```

```python
# 第三个单元格 - 构建APK
%cd /content/tamagotchi_game
!buildozer android debug
```

```python
# 第四个单元格 - 下载APK
from google.colab import files
import glob

apk_files = glob.glob('bin/*.apk')
for apk in apk_files:
    files.download(apk)
```

4. 等待构建完成
5. APK 会自动下载到你的电脑

---

## 方法三：使用在线构建服务

访问 https://buildozer.io （如果可用）
- 上传游戏代码
- 在线构建
- 下载APK

---

## 已创建的文件

所有游戏代码已在 `~/tamagotchi_game/` 目录中：

```
tamagotchi_game/
├── main.py              # 主程序
├── pet.py               # 宠物类
├── time_manager.py      # 时间管理
├── save_system.py       # 存档系统
├── pixel_pet.py         # 像素渲染
├── food_menu.py         # 食物菜单
├── notifications.py     # 通知系统
├── buildozer.spec       # Android 配置
├── .github/workflows/   # GitHub Actions 配置
│   └── build.yml        # 自动构建配置
└── README.md            # 说明文档
```

---

## 网页版（立即可玩！）

如果想立即体验游戏，可以打开网页版：

```bash
open ~/tamagotchi_game/web_version.html
```

或在浏览器中打开 `~/tamagotchi_game/web_version.html`

---

## 需要帮助？

如果遇到问题，请告诉我：
1. 你是否有 GitHub 账号？
2. 你是否有编程经验？
3. 你更倾向于使用哪种方法？

我可以提供更详细的指导。
