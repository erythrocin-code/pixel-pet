"""
宠物类 - 核心游戏对象
"""

from datetime import datetime, timedelta
import random


class Pet:
    """虚拟宠物类"""
    
    STAGES = ['baby', 'child', 'teen', 'adult']
    STAGE_DAYS = [0, 3, 7, 14]  # 每个阶段的开始天数
    
    def __init__(self, name):
        self.name = name
        self.birth_time = datetime.now()
        self.age_days = 0
        
        # 状态值 (0-100)
        self.hunger = 80
        self.happiness = 80
        self.health = 100
        self.cleanliness = 80
        self.energy = 100
        
        # 状态
        self.is_sleeping = False
        self.is_sick = False
        self.stage = 'baby'
        
        # 计时器
        self.hunger_timer = 0
        self.happiness_timer = 0
        self.cleanliness_timer = 0
        self.health_timer = 0
        
        # 动画状态
        self.mood = 'happy'  # happy, neutral, sad, sick
        self.last_random_event = datetime.now()
        
        # 统计
        self.total_foods_eaten = 0
        self.times_played = 0
        self.times_cleaned = 0
    
    def update(self, dt, is_player_sleeping=False):
        """更新宠物状态"""
        # 更新年龄
        self.update_age()
        
        # 更新成长阶段
        self.update_stage()
        
        # 自然衰减（真实时间）
        decay_multiplier = 0.5 if is_player_sleeping else 1.0
        if self.is_sleeping:
            decay_multiplier *= 0.3
        
        # 饱腹度衰减（每10秒-1）
        self.hunger_timer += dt
        if self.hunger_timer >= 10:
            self.hunger_timer = 0
            self.hunger = max(0, self.hunger - 1 * decay_multiplier)
        
        # 幸福度衰减（每15秒-1）
        self.happiness_timer += dt
        if self.happiness_timer >= 15:
            self.happiness_timer = 0
            self.happiness = max(0, self.happiness - 1 * decay_multiplier)
        
        # 清洁度衰减（每20秒-1）
        self.cleanliness_timer += dt
        if self.cleanliness_timer >= 20:
            self.cleanliness_timer = 0
            self.cleanliness = max(0, self.cleanliness - 1 * decay_multiplier)
        
        # 能量变化
        if self.is_sleeping:
            self.energy = min(100, self.energy + 2 * dt)
        else:
            self.energy = max(0, self.energy - 0.5 * dt * decay_multiplier)
        
        # 健康度衰减（当其他状态差时）
        if self.hunger < 20 or self.cleanliness < 20:
            self.health_timer += dt
            if self.health_timer >= 30:
                self.health_timer = 0
                self.health = max(0, self.health - 1 * decay_multiplier)
        
        # 检查生病
        if self.health < 20 and not self.is_sick:
            if random.random() < 0.01:  # 1%概率生病
                self.is_sick = True
        
        # 更新心情
        self.update_mood()
        
        # 随机事件
        self.check_random_events()
    
    def update_age(self):
        """更新年龄（天数）"""
        now = datetime.now()
        delta = now - self.birth_time
        self.age_days = delta.days
    
    def update_stage(self):
        """更新成长阶段"""
        for i, days in enumerate(reversed(self.STAGE_DAYS)):
            if self.age_days >= days:
                self.stage = self.STAGES[3 - i]
                break
    
    def update_mood(self):
        """更新心情状态"""
        avg_status = (self.hunger + self.happiness + 
                     self.health + self.cleanliness + self.energy) / 5
        
        if self.is_sick:
            self.mood = 'sick'
        elif avg_status >= 70:
            self.mood = 'happy'
        elif avg_status >= 40:
            self.mood = 'neutral'
        else:
            self.mood = 'sad'
    
    def check_random_events(self):
        """检查随机事件"""
        now = datetime.now()
        delta = (now - self.last_random_event).total_seconds()
        
        if delta < 300:  # 每5分钟最多一次
            return
        
        self.last_random_event = now
        
        # 5%概率发现宝藏
        if random.random() < 0.05:
            return {'type': 'treasure', 'message': '宠物发现了宝藏！'}
        
        # 3%概率坏天气
        if random.random() < 0.03:
            self.happiness = max(0, self.happiness - 10)
            return {'type': 'storm', 'message': '暴风雨来了，宠物有点害怕'}
        
        return None
    
    def feed(self, food_type):
        """喂食"""
        foods = {
            'apple': {'hunger': 20, 'health': 5},
            'candy': {'hunger': 10, 'health': -5, 'happiness': 10},
            'vegetable': {'hunger': 15, 'health': 10},
            'cake': {'hunger': 30, 'health': -10, 'happiness': 20},
            'potion': {'health': 30},
            'energy_bar': {'hunger': 25, 'energy': 20}
        }
        
        if food_type in foods:
            food = foods[food_type]
            self.hunger = min(100, self.hunger + food.get('hunger', 0))
            self.health = min(100, max(0, self.health + food.get('health', 0)))
            self.happiness = min(100, self.happiness + food.get('happiness', 0))
            self.energy = min(100, self.energy + food.get('energy', 0))
            self.total_foods_eaten += 1
            return True
        return False
    
    def play(self):
        """玩耍"""
        if self.energy < 20:
            return False
        
        self.happiness = min(100, self.happiness + 15)
        self.energy = max(0, self.energy - 20)
        self.hunger = max(0, self.hunger - 5)
        self.times_played += 1
        return True
    
    def clean(self):
        """清洁"""
        self.cleanliness = min(100, self.cleanliness + 30)
        self.happiness = min(100, self.happiness + 5)
        self.times_cleaned += 1
    
    def sleep(self):
        """切换睡眠状态"""
        self.is_sleeping = not self.is_sleeping
        if self.is_sleeping:
            self.mood = 'sleeping'
    
    def heal(self):
        """治疗"""
        if self.is_sick:
            self.is_sick = False
            self.health = min(100, self.health + 30)
            return True
        return False
    
    def apply_offline_effects(self, offline_seconds):
        """应用离线效果"""
        # 计算离线时的衰减
        hours_offline = offline_seconds / 3600
        
        # 衰减系数（离线时衰减更慢）
        decay_rate = 0.5
        
        # 饱腹度衰减
        hunger_decay = min(50, hours_offline * 5 * decay_rate)
        self.hunger = max(0, self.hunger - hunger_decay)
        
        # 幸福度衰减
        happiness_decay = min(40, hours_offline * 4 * decay_rate)
        self.happiness = max(0, self.happiness - happiness_decay)
        
        # 清洁度衰减
        cleanliness_decay = min(30, hours_offline * 3 * decay_rate)
        self.cleanliness = max(0, self.cleanliness - cleanliness_decay)
        
        # 如果离线超过8小时，假设宠物大部分时间在睡觉
        if hours_offline > 8:
            self.energy = min(100, 80)  # 恢复到80
        else:
            # 睡觉时恢复能量
            self.energy = min(100, self.energy + hours_offline * 10)
        
        # 更新心情
        self.update_mood()
    
    def get_average_status(self):
        """获取平均状态值"""
        return (self.hunger + self.happiness + self.health + 
                self.cleanliness + self.energy) / 5
    
    def to_dict(self):
        """转换为字典（用于保存）"""
        return {
            'name': self.name,
            'birth_time': self.birth_time.isoformat(),
            'age_days': self.age_days,
            'hunger': self.hunger,
            'happiness': self.happiness,
            'health': self.health,
            'cleanliness': self.cleanliness,
            'energy': self.energy,
            'is_sleeping': self.is_sleeping,
            'is_sick': self.is_sick,
            'stage': self.stage,
            'mood': self.mood,
            'total_foods_eaten': self.total_foods_eaten,
            'times_played': self.times_played,
            'times_cleaned': self.times_cleaned
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建宠物"""
        pet = cls(data['name'])
        pet.birth_time = datetime.fromisoformat(data['birth_time'])
        pet.age_days = data['age_days']
        pet.hunger = data['hunger']
        pet.happiness = data['happiness']
        pet.health = data['health']
        pet.cleanliness = data['cleanliness']
        pet.energy = data['energy']
        pet.is_sleeping = data['is_sleeping']
        pet.is_sick = data['is_sick']
        pet.stage = data['stage']
        pet.mood = data['mood']
        pet.total_foods_eaten = data.get('total_foods_eaten', 0)
        pet.times_played = data.get('times_played', 0)
        pet.times_cleaned = data.get('times_cleaned', 0)
        return pet
