"""
像素宠物渲染器 - 绘制像素风格的宠物
"""

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.metrics import dp


class PixelPetWidget(Widget):
    """像素宠物显示组件"""
    
    # 像素颜色方案
    COLORS = {
        'body': (0.42, 0.73, 0.19, 1),      # 绿色身体
        'body_dark': (0.29, 0.55, 0.14, 1),  # 深绿
        'body_light': (0.6, 0.9, 0.31, 1),   # 浅绿
        'eye_white': (1, 1, 1, 1),
        'eye_black': (0.1, 0.1, 0.1, 1),
        'eye_highlight': (1, 1, 1, 0.8),
        'mouth': (0.2, 0.2, 0.2, 1),
        'cheek': (1, 0.6, 0.6, 0.6),         # 腮红
        'sick': (0.5, 0.5, 0.5, 1),           # 生病灰色
        'sleeping': (0.3, 0.3, 0.3, 1)
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pet_state = None
        self.animation_frame = 0
        self.breath_offset = 0
        self.blink_timer = 0
        self.is_blinking = False
        
        # 动画定时器
        self.anim_clock = Clock.schedule_interval(self.animate, 1/10)  # 10 FPS动画
        
        # 绑定大小变化
        self.bind(size=self.redraw, pos=self.redraw)
    
    def set_state(self, pet):
        """设置宠物状态"""
        self.pet_state = pet
        self.redraw()
    
    def animate(self, dt):
        """动画更新"""
        self.animation_frame = (self.animation_frame + 1) % 4
        self.breath_offset = [0, 1, 2, 1][self.animation_frame]
        
        # 随机眨眼
        self.blink_timer += dt
        if self.blink_timer > 3 and not self.is_blinking:
            if self.blink_timer > 3.2:
                self.is_blinking = False
                self.blink_timer = 0
            else:
                self.is_blinking = True
        
        self.redraw()
    
    def redraw(self, *args):
        """重绘宠物"""
        self.canvas.clear()
        
        if not self.pet_state:
            self.draw_default_pet()
            return
        
        with self.canvas:
            # 根据状态选择颜色
            if self.pet_state.is_sick:
                body_color = self.COLORS['sick']
            elif self.pet_state.is_sleeping:
                body_color = self.COLORS['sleeping']
            else:
                body_color = self.COLORS['body']
            
            # 计算中心位置
            cx = self.center_x
            cy = self.center_y
            size = min(self.width, self.height) * 0.8
            
            # 绘制身体（带呼吸动画）
            Color(*body_color)
            Ellipse(
                pos=(cx - size/2, cy - size/2 + self.breath_offset),
                size=(size, size * 0.85)
            )
            
            # 身体高光
            Color(*self.COLORS['body_light'])
            Ellipse(
                pos=(cx - size/4, cy + size/6 + self.breath_offset),
                size=(size/3, size/4)
            )
            
            # 绘制眼睛
            eye_y = cy + size/8 + self.breath_offset
            eye_size = size / 6
            
            if self.pet_state.is_sleeping:
                # 闭眼 - 横线
                Color(*self.COLORS['mouth'])
                Line(
                    points=[cx - size/4, eye_y, cx - size/8, eye_y],
                    width=dp(2)
                )
                Line(
                    points=[cx + size/8, eye_y, cx + size/4, eye_y],
                    width=dp(2)
                )
            elif self.is_blinking:
                # 眨眼
                Color(*self.COLORS['mouth'])
                Line(
                    points=[cx - size/4, eye_y, cx - size/8, eye_y],
                    width=dp(2)
                )
                Line(
                    points=[cx + size/8, eye_y, cx + size/4, eye_y],
                    width=dp(2)
                )
            else:
                # 睁眼
                # 左眼
                Color(*self.COLORS['eye_white'])
                Ellipse(
                    pos=(cx - size/4 - eye_size/2, eye_y - eye_size/2),
                    size=(eye_size, eye_size)
                )
                Color(*self.COLORS['eye_black'])
                Ellipse(
                    pos=(cx - size/4 - eye_size/4, eye_y - eye_size/4),
                    size=(eye_size/2, eye_size/2)
                )
                # 眼睛高光
                Color(*self.COLORS['eye_highlight'])
                Ellipse(
                    pos=(cx - size/4 - eye_size/6, eye_y),
                    size=(eye_size/4, eye_size/4)
                )
                
                # 右眼
                Color(*self.COLORS['eye_white'])
                Ellipse(
                    pos=(cx + size/8 - eye_size/2, eye_y - eye_size/2),
                    size=(eye_size, eye_size)
                )
                Color(*self.COLORS['eye_black'])
                Ellipse(
                    pos=(cx + size/8 - eye_size/4, eye_y - eye_size/4),
                    size=(eye_size/2, eye_size/2)
                )
                # 眼睛高光
                Color(*self.COLORS['eye_highlight'])
                Ellipse(
                    pos=(cx + size/8 - eye_size/6, eye_y),
                    size=(eye_size/4, eye_size/4)
                )
            
            # 绘制嘴巴
            mouth_y = cy - size/6 + self.breath_offset
            Color(*self.COLORS['mouth'])
            
            if self.pet_state.mood == 'happy':
                # 微笑
                Line(
                    points=[
                        cx - size/6, mouth_y,
                        cx - size/12, mouth_y - size/12,
                        cx, mouth_y - size/10,
                        cx + size/12, mouth_y - size/12,
                        cx + size/6, mouth_y
                    ],
                    width=dp(2)
                )
            elif self.pet_state.mood == 'sad':
                # 难过
                Line(
                    points=[
                        cx - size/6, mouth_y - size/12,
                        cx, mouth_y,
                        cx + size/6, mouth_y - size/12
                    ],
                    width=dp(2)
                )
            elif self.pet_state.mood == 'sick':
                # 生病 - 波浪线
                Line(
                    points=[
                        cx - size/6, mouth_y,
                        cx - size/12, mouth_y - size/20,
                        cx, mouth_y,
                        cx + size/12, mouth_y - size/20,
                        cx + size/6, mouth_y
                    ],
                    width=dp(2)
                )
            else:
                # 中性
                Line(
                    points=[cx - size/6, mouth_y, cx + size/6, mouth_y],
                    width=dp(2)
                )
            
            # 腮红（当开心时）
            if self.pet_state.mood == 'happy':
                Color(*self.COLORS['cheek'])
                Ellipse(
                    pos=(cx - size/3, cy - size/10),
                    size=(size/5, size/8)
                )
                Ellipse(
                    pos=(cx + size/6, cy - size/10),
                    size=(size/5, size/8)
                )
            
            # 绘制小脚
            foot_y = cy - size/2 - size/10 + self.breath_offset
            foot_offset = [0, 2, 0, -2][self.animation_frame]
            
            Color(*self.COLORS['body_dark'])
            # 左脚
            Rectangle(
                pos=(cx - size/3 + foot_offset, foot_y),
                size=(size/5, size/8)
            )
            # 右脚（延迟半拍）
            foot_offset2 = [0, -2, 0, 2][self.animation_frame]
            Rectangle(
                pos=(cx + size/10 + foot_offset2, foot_y),
                size=(size/5, size/8)
            )
            
            # 绘制zzz（睡觉时）
            if self.pet_state.is_sleeping:
                Color(1, 1, 1, 0.8)
                z_offset = (self.animation_frame % 3) * 5
                # 从kivy.graphics导入Label不可行，用线条代替
                Line(
                    points=[
                        cx + size/3, cy + size/3 + z_offset,
                        cx + size/3 + size/10, cy + size/3 + z_offset,
                        cx + size/3, cy + size/3 + size/10 + z_offset,
                        cx + size/3 + size/10, cy + size/3 + size/10 + z_offset
                    ],
                    width=dp(2)
                )
    
    def draw_default_pet(self):
        """绘制默认宠物（预览用）"""
        with self.canvas:
            cx = self.center_x
            cy = self.center_y
            size = min(self.width, self.height) * 0.8
            
            # 简单的绿色身体
            Color(*self.COLORS['body'])
            Ellipse(pos=(cx - size/2, cy - size/2), size=(size, size * 0.85))
            
            # 简单的眼睛
            Color(*self.COLORS['eye_white'])
            Ellipse(pos=(cx - size/4 - 5, cy + 5), size=(10, 10))
            Ellipse(pos=(cx + size/8 - 5, cy + 5), size=(10, 10))
            
            Color(*self.COLORS['eye_black'])
            Ellipse(pos=(cx - size/4 - 3, cy + 7), size=(6, 6))
            Ellipse(pos=(cx + size/8 - 3, cy + 7), size=(6, 6))
    
    def play_animation(self):
        """播放玩耍动画"""
        # 可以添加更复杂的动画逻辑
        pass
    
    def clean_animation(self):
        """播放清洁动画"""
        # 可以添加泡泡效果等
        pass
    
    def on_destroy(self):
        """销毁时清理"""
        if self.anim_clock:
            self.anim_clock.cancel()
