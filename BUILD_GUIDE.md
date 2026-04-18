# 像素宠物游戏 - APK 构建指南

## 当前状态

由于当前网络环境限制，本地构建APK遇到了困难。以下是获取APK的解决方案。

---

## 方案一：在其他电脑上构建（推荐）

### 需要的环境：
- Ubuntu 20.04+ 或 macOS（有Homebrew）
- Python 3.8+
- Java 17
- 稳定的网络连接

### 步骤：

1. **下载游戏代码**
   - 将 `~/tamagotchi_game.zip` 复制到目标电脑
   - 解压：`unzip tamagotchi_game.zip`

2. **安装依赖**
   ```bash
   # Ubuntu
   sudo apt update
   sudo apt install -y python3-pip build-essential git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

   # macOS
   brew install python3 git autoconf automake libtool pkg-config cmake openjdk@17
   ```

3. **安装Python包**
   ```bash
   pip3 install buildozer cython
   ```

4. **构建APK**
   ```bash
   cd tamagotchi_game
   buildozer android debug
   ```

5. **APK位置**
   - 构建完成后，APK在 `bin/` 目录中
   - 文件名类似：`pixel_pet-1.0.0-debug.apk`

---

## 方案二：使用在线构建服务

### GitHub Actions（免费）

1. **注册GitHub账号**
   - 访问 https://github.com 注册

2. **创建新仓库**
   - 仓库名：pixel-pet

3. **上传代码**
   - 将 `~/tamagotchi_game/` 中的所有文件上传

4. **自动构建**
   - 推送后，GitHub Actions会自动构建
   - 等待15-30分钟

5. **下载APK**
   - 访问仓库的Actions页面
   - 下载构建产物

---

## 方案三：使用Google Colab（免费）

1. 访问 https://colab.research.google.com
2. 创建新笔记本
3. 运行以下代码：

```python
# 单元格1：安装依赖
!apt-get update
!apt-get install -y python3-pip build-essential git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
!pip install buildozer cython
```

```python
# 单元格2：上传游戏代码
from google.colab import files
!mkdir -p /content/tamagotchi_game
%cd /content/tamagotchi_game
uploaded = files.upload()  # 上传所有.py文件和buildozer.spec
```

```python
# 单元格3：构建APK
!buildozer android debug
```

```python
# 单元格4：下载APK
from google.colab import files
import glob
for apk in glob.glob('bin/*.apk'):
    files.download(apk)
```

---

## 游戏文件清单

确保上传以下文件：

```
tamagotchi_game/
├── main.py              # 主程序
├── pet.py               # 宠物类
├── time_manager.py      # 时间管理
├── save_system.py       # 存档系统
├── pixel_pet.py         # 像素渲染
├── food_menu.py         # 食物菜单
├── notifications.py     # 通知系统
└── buildozer.spec       # 构建配置
```

---

## 安装APK到手机

1. 将APK文件传输到OPPO Find X8s
2. 打开"文件管理器"
3. 找到APK文件并点击
4. 如果提示"未知来源"：
   - 设置 → 安全 → 允许安装未知来源应用
5. 点击"安装"

---

## 网页版（立即可玩）

如果想立即体验游戏，可以使用网页版：

```bash
# 在手机浏览器中打开
open ~/tamagotchi_game/web_version.html
```

网页版功能完整，支持：
- 喂食、玩耍、清洁、休息、治疗
- 真实时间同步
- 昼夜循环
- 睡眠模式
- 自动存档

---

## 需要帮助？

如果遇到问题，请告诉我：
1. 你使用的是哪种方案？
2. 遇到了什么错误？
3. 你的操作系统是什么？
