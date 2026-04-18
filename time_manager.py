"""
时间管理器 - 处理昼夜循环和玩家睡眠模式
"""

from datetime import datetime, timedelta


class TimeManager:
    """时间管理器类"""
    
    def __init__(self):
        self.player_sleep_start = 23  # 默认23点睡觉
        self.player_sleep_end = 7     # 默认7点起床
        self.is_player_sleeping = False
        self.sleep_start_time = None
    
    def reset(self):
        """重置时间管理器"""
        self.is_player_sleeping = False
        self.sleep_start_time = None
    
    def get_time_of_day(self):
        """获取当前时间段"""
        hour = datetime.now().hour
        
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        elif 18 <= hour < 21:
            return 'evening'
        else:
            return 'night'
    
    def is_pet_sleep_time(self):
        """判断是否是宠物该睡觉的时间"""
        hour = datetime.now().hour
        return hour >= 21 or hour < 6
    
    def is_player_bedtime(self):
        """判断是否是玩家设定的睡觉时间"""
        hour = datetime.now().hour
        if self.player_sleep_start > self.player_sleep_end:
            # 跨午夜的情况，比如23点到7点
            return hour >= self.player_sleep_start or hour < self.player_sleep_end
        else:
            # 不跨午夜的情况
            return self.player_sleep_start <= hour < self.player_sleep_end
    
    def set_sleep_schedule(self, sleep_time_str, wake_time_str):
        """设置睡眠时间表"""
        try:
            # 解析时间字符串，如 "23:00"
            sleep_hour = int(sleep_time_str.split(':')[0])
            wake_hour = int(wake_time_str.split(':')[0])
            
            self.player_sleep_start = sleep_hour
            self.player_sleep_end = wake_hour
        except (ValueError, IndexError):
            # 使用默认值
            self.player_sleep_start = 23
            self.player_sleep_end = 7
    
    def go_to_sleep(self):
        """进入睡眠模式"""
        self.is_player_sleeping = True
        self.sleep_start_time = datetime.now()
    
    def wake_up(self):
        """醒来"""
        self.is_player_sleeping = False
        self.sleep_start_time = None
    
    def get_sleep_duration(self):
        """获取已经睡眠的时长（秒）"""
        if self.sleep_start_time:
            delta = datetime.now() - self.sleep_start_time
            return delta.total_seconds()
        return 0
    
    def get_greeting(self):
        """根据时间获取问候语"""
        hour = datetime.now().hour
        
        if 5 <= hour < 9:
            return '早上好！'
        elif 9 <= hour < 12:
            return '上午好！'
        elif 12 <= hour < 14:
            return '中午好！'
        elif 14 <= hour < 18:
            return '下午好！'
        elif 18 <= hour < 21:
            return '傍晚好！'
        elif 21 <= hour < 24:
            return '晚上好！'
        else:
            return '夜深了，早点休息哦~'
    
    def should_pet_be_sleepy(self):
        """判断宠物是否应该犯困"""
        hour = datetime.now().hour
        return hour >= 20 or hour < 5
    
    def get_background_color(self):
        """获取当前时间的背景颜色"""
        hour = datetime.now().hour
        
        if 6 <= hour < 12:  # 早晨 - 天蓝色
            return (0.53, 0.81, 0.92, 1)
        elif 12 <= hour < 18:  # 下午 - 暖黄色
            return (1, 0.88, 0.73, 1)
        elif 18 <= hour < 21:  # 傍晚 - 橙色
            return (1, 0.55, 0, 1)
        else:  # 夜晚 - 深蓝色
            return (0.098, 0.098, 0.44, 1)
    
    def to_dict(self):
        """转换为字典（用于保存）"""
        return {
            'player_sleep_start': self.player_sleep_start,
            'player_sleep_end': self.player_sleep_end,
            'is_player_sleeping': self.is_player_sleeping,
            'sleep_start_time': self.sleep_start_time.isoformat() if self.sleep_start_time else None
        }
    
    def load(self, data):
        """从字典加载"""
        if data:
            self.player_sleep_start = data.get('player_sleep_start', 23)
            self.player_sleep_end = data.get('player_sleep_end', 7)
            self.is_player_sleeping = data.get('is_player_sleeping', False)
            
            sleep_start = data.get('sleep_start_time')
            if sleep_start:
                self.sleep_start_time = datetime.fromisoformat(sleep_start)
