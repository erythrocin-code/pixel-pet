# 像素宠物 - 虚拟宠物养成游戏

一个类似拓麻歌子的像素风格虚拟宠物养成游戏，使用 Python + Kivy 开发。

## 功能特点

- 🎮 像素风格界面，高清细腻的视觉效果
- ⏰ 真实时间同步，昼夜循环系统
- 😴 玩家睡觉模式，宠物也会休息
- 🍎 多种食物系统，影响宠物状态
- 💾 自动存档，离线状态衰减
- 📱 支持 Android 手机

## 游戏玩法

1. **喂食**：选择不同食物喂养宠物，每种食物有不同效果
2. **玩耍**：和宠物互动，提升幸福度（消耗能量）
3. **清洁**：保持宠物清洁，防止生病
4. **休息**：让宠物睡觉恢复能量
5. **治疗**：当宠物生病时进行治疗

## 状态系统

- 🍖 **饱腹度**：会随时间下降，太低会影响健康
- ⭐ **幸福度**：需要玩耍来维持
- ❤️ **健康度**：受其他状态影响，太低会生病
- ✨ **清洁度**：需要定期清洁
- ⚡ **能量值**：玩耍消耗，睡觉恢复

## 时间系统

- 游戏时间与现实时间完全同步
- 背景根据时间变化（早晨/下午/傍晚/夜晚）
- 晚上9点后宠物会犯困
- 支持设置玩家睡眠时间

## 安装说明

### 桌面运行（测试用）

```bash
# 安装依赖
pip install kivy

# 运行游戏
python main.py
```

### Android 构建

#### 方法一：使用 Buildozer（推荐）

1. 安装 Buildozer：
```bash
pip install buildozer
```

2. 安装 Android 依赖（需要 Linux 或 WSL）：
```bash
sudo apt update
sudo apt install -y python3-pip build-essential git zip unzip openjdk-17-jdk python3-setuptools
pip install --user cython
```

3. 构建 APK：
```bash
cd tamagotchi_game
buildozer android debug
```

4. APK 文件在 `bin/` 目录下

#### 方法二：使用 GitHub Actions

1. Fork 此仓库
2. 在 GitHub 仓库设置中启用 Actions
3. 推送代码会自动触发构建
4. 在 Actions 页面下载 APK

## 文件结构

```
tamagotchi_game/
├── main.py           # 主程序入口
├── pet.py            # 宠物类
├── time_manager.py   # 时间管理器
├── save_system.py    # 存档系统
├── pixel_pet.py      # 像素宠物渲染器
├── food_menu.py      # 食物菜单
├── notifications.py  # 通知系统
├── buildozer.spec    # Android 打包配置
└── README.md         # 说明文档
```

## OPPO Find X8s 适配

已针对 OPPO Find X8s 进行优化：
- 支持 1.5K 高分辨率屏幕
- 适配 ColorOS 15 系统
- 支持 16GB 大内存优化
- 兼容 Android 15

## 其他安卓手机兼容性

- 最低支持：Android 7.0 (API 24)
- 推荐配置：Android 10+，4GB+ 内存
- 支持架构：arm64-v8a, armeabi-v7a

## 开发说明

### 添加新食物

在 `food_menu.py` 的 `FOODS` 列表中添加：
```python
{
    'id': 'food_id',
    'name': '🍖 食物名',
    'desc': '效果描述',
    'hunger': 20,  # 饱腹度
    'health': 5,   # 健康度
    'happiness': 10,  # 幸福度（可选）
    'energy': 15   # 能量值（可选）
}
```

### 修改衰减速度

在 `pet.py` 的 `update` 方法中修改时间间隔：
```python
# 饱腹度衰减（每10秒-1）
self.hunger_timer += dt
if self.hunger_timer >= 10:  # 修改这个值
```

## 许可证

MIT License

## 作者

Created with ❤️ by Hermes Agent
