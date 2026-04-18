"""
存档系统 - 处理游戏保存和加载
"""

import os
import json
from datetime import datetime


class SaveSystem:
    """存档系统类"""
    
    def __init__(self):
        # 确定存档目录
        if 'ANDROID_DATA' in os.environ:
            # Android系统
            self.save_dir = '/data/data/com.tamagotchi.pixel_pet/files'
        else:
            # 桌面系统
            self.save_dir = os.path.expanduser('~/.pixel_pet')
        
        # 确保目录存在
        os.makedirs(self.save_dir, exist_ok=True)
        
        self.save_file = os.path.join(self.save_dir, 'save.json')
        self.settings_file = os.path.join(self.save_dir, 'settings.json')
    
    def has_save(self):
        """检查是否有存档"""
        return os.path.exists(self.save_file)
    
    def save(self, data):
        """保存游戏数据"""
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
    
    def load(self):
        """加载游戏数据"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载失败: {e}")
        return None
    
    def get_offline_time(self):
        """获取离线时长（秒）"""
        data = self.load()
        if data and 'save_time' in data:
            try:
                save_time = datetime.fromisoformat(data['save_time'])
                delta = datetime.now() - save_time
                return delta.total_seconds()
            except (ValueError, KeyError):
                pass
        return 0
    
    def save_settings(self, settings):
        """保存设置"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存设置失败: {e}")
            return False
    
    def load_settings(self):
        """加载设置"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载设置失败: {e}")
        return None
    
    def delete_save(self):
        """删除存档"""
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
            return True
        except Exception as e:
            print(f"删除存档失败: {e}")
            return False
    
    def get_save_info(self):
        """获取存档信息"""
        data = self.load()
        if data and 'pet' in data:
            pet_data = data['pet']
            return {
                'name': pet_data.get('name', '未知'),
                'age_days': pet_data.get('age_days', 0),
                'stage': pet_data.get('stage', 'baby'),
                'save_time': data.get('save_time', '未知')
            }
        return None
