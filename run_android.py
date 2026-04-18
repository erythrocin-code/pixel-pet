"""
像素宠物游戏 - Android 直接运行版本
使用 QPython 或 Termux 运行

安装说明：
1. 在 Android 手机上安装 QPython 3L（应用商店搜索）
2. 将此文件和所有依赖文件复制到手机
3. 在 QPython 中运行此文件
"""

import os
import sys

# 检查是否在 Android 上运行
def is_android():
    return 'ANDROID_DATA' in os.environ or 'ANDROID_ROOT' in os.environ

# 如果在 Android 上，设置正确的路径
if is_android():
    # QPython 路径
    qpython_path = '/data/data/com.hipipal.qpyplus/files/bin'
    if os.path.exists(qpython_path):
        sys.path.insert(0, qpython_path)
    
    # 设置环境变量
    os.environ['KIVY_LOG_LEVEL'] = 'warning'

# 导入主程序
try:
    from main import TamagotchiApp
    
    if __name__ == '__main__':
        print("=" * 40)
        print("  像素宠物游戏")
        print("  类似拓麻歌子的虚拟宠物养成游戏")
        print("=" * 40)
        print()
        print("功能说明：")
        print("🍎 喂食 - 给宠物喂食")
        print("🎮 玩耍 - 和宠物互动")
        print("🛁 清洁 - 保持宠物干净")
        print("💤 休息 - 让宠物睡觉")
        print("💊 治疗 - 治疗生病的宠物")
        print()
        print("时间系统：")
        print("- 游戏时间与现实时间同步")
        print("- 背景随时间变化")
        print("- 支持睡眠模式")
        print()
        print("正在启动游戏...")
        print()
        
        TamagotchiApp().run()

except ImportError as e:
    print(f"导入错误: {e}")
    print()
    print("请确保已安装 Kivy：")
    print("pip install kivy")
    print()
    print("如果是 Android 设备，请使用 QPython 3L")
    sys.exit(1)
except Exception as e:
    print(f"启动错误: {e}")
    sys.exit(1)
