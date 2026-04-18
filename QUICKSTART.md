# 🎮 像素宠物游戏 - 快速开始指南

## 📦 已创建的文件

### 核心游戏文件
- `main.py` - 主程序入口（Kivy 应用）
- `pet.py` - 宠物类（核心游戏逻辑）
- `time_manager.py` - 时间管理器
- `save_system.py` - 存档系统
- `pixel_pet.py` - 像素宠物渲染器
- `food_menu.py` - 食物菜单
- `notifications.py` - 通知系统

### 构建相关
- `buildozer.spec` - Android 打包配置
- `build.sh` - Linux/macOS 构建脚本
- `Dockerfile` - Docker 构建配置
- `docker-compose.yml` - Docker Compose 配置
- `.github/workflows/build.yml` - GitHub Actions 自动构建

### 文档
- `README.md` - 项目说明
- `INSTALL.md` - 详细安装指南
- `COLAB_BUILD.md` - Google Colab 构建指南

### 特殊版本
- `run_android.py` - Android 直接运行版本
- `web_version.html` - 网页版本（立即可玩！）

---

## 🚀 立即开始（3种方式）

### 方式一：网页版（最简单，立即可玩！）

1. 打开 `web_version.html` 文件
2. 直接在浏览器中玩！
3. 支持手机浏览器

**特点：**
- ✅ 无需安装任何软件
- ✅ 自动存档到浏览器
- ✅ 支持所有功能
- ✅ 响应式设计，适配手机

---

### 方式二：桌面版（用于测试）

```bash
# 安装依赖
pip install kivy

# 运行游戏
python main.py
```

---

### 方式三：Android APK（手机安装）

#### 方法 A：使用 Google Colab（推荐，免费）

1. 访问 https://colab.research.google.com
2. 创建新笔记本
3. 复制 `COLAB_BUILD.md` 中的代码
4. 运行并下载 APK

#### 方法 B：使用 Docker

```bash
# 构建 Docker 镜像
docker-compose build

# 运行构建
docker-compose up

# APK 文件在 bin/ 目录
```

#### 方法 C：本地构建（需要 Linux）

```bash
# 运行构建脚本
./build.sh
```

---

## 📱 OPPO Find X8s 安装

1. 下载 APK 文件到手机
2. 打开"文件管理器"
3. 找到 APK 文件并点击
4. 如果提示"未知来源"，进入 设置 → 安全 → 允许安装
5. 点击"安装"
6. 完成！

---

## 🎯 游戏功能

### 基本操作
- 🍎 **喂食**：6种不同食物，各有不同效果
- 🎮 **玩耍**：增加幸福度，消耗能量
- 🛁 **清洁**：保持宠物干净
- 💤 **休息**：让宠物睡觉恢复能量
- 💊 **治疗**：治愈生病的宠物

### 状态系统
- 🍖 饱腹度：会随时间下降
- ⭐ 幸福度：需要玩耍来维持
- ❤️ 健康度：受其他状态影响
- ✨ 清洁度：需要定期清洁
- ⚡ 能量值：玩耍消耗，睡觉恢复

### 时间系统
- 游戏时间与现实时间完全同步
- 背景颜色随时间变化（早晨/下午/傍晚/夜晚）
- 晚上9点后宠物会犯困
- 支持玩家睡眠模式

### 离线处理
- 自动存档
- 离线时状态会衰减
- 长时间离线后宠物会很想你

---

## 📂 项目结构

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
├── build.sh             # 构建脚本
├── Dockerfile           # Docker 配置
├── docker-compose.yml   # Docker Compose
├── web_version.html     # 网页版本 ⭐
├── run_android.py       # Android 运行
├── README.md            # 说明文档
├── INSTALL.md           # 安装指南
└── COLAB_BUILD.md       # Colab 构建
```

---

## 💡 提示

1. **最快体验**：直接打开 `web_version.html` 开始玩
2. **手机安装**：使用 Google Colab 构建 APK
3. **开发测试**：桌面运行 `python main.py`

---

## 🔧 遇到问题？

1. 查看 `INSTALL.md` 中的故障排除
2. 确保 Python 3.8+ 和 Kivy 已安装
3. 网页版无需任何依赖，可直接使用

---

## 📄 许可证

MIT License

---

**祝你和你的像素宠物玩得开心！** 🐸💚
