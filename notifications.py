"""
通知管理器 - 显示游戏内通知消息
"""

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp


class NotificationManager(FloatLayout):
    """通知管理器"""
    
    NOTIFICATION_COLORS = {
        'info': (0.3, 0.6, 1, 0.9),      # 蓝色
        'success': (0.3, 0.9, 0.3, 0.9),  # 绿色
        'warning': (1, 0.7, 0.2, 0.9),    # 橙色
        'error': (1, 0.3, 0.3, 0.9)       # 红色
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_notification = None
        self.hide_event = None
    
    def show(self, message, notification_type='info', duration=3):
        """显示通知"""
        # 清除之前的通知
        if self.current_notification:
            self.remove_widget(self.current_notification)
            if self.hide_event:
                self.hide_event.cancel()
        
        # 创建通知容器
        notification = FloatLayout(
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # 获取颜色
        color = self.NOTIFICATION_COLORS.get(
            notification_type, 
            self.NOTIFICATION_COLORS['info']
        )
        
        # 绘制背景
        with notification.canvas.before:
            Color(*color)
            bg = RoundedRectangle(
                pos=notification.pos,
                size=notification.size,
                radius=[dp(10)]
            )
        
        notification.bind(
            pos=lambda w, p: setattr(bg, 'pos', p),
            size=lambda w, s: setattr(bg, 'size', s)
        )
        
        # 添加文字
        label = Label(
            text=message,
            font_size=sp(16),
            color=(1, 1, 1, 1),
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        notification.add_widget(label)
        
        # 添加到界面
        self.add_widget(notification)
        self.current_notification = notification
        
        # 初始位置（屏幕下方外）
        notification.y = -dp(60)
        
        # 滑入动画
        anim = Animation(y=dp(5), duration=0.3)
        anim.start(notification)
        
        # 设置自动隐藏
        self.hide_event = Clock.schedule_once(
            lambda dt: self.hide(),
            duration
        )
    
    def hide(self):
        """隐藏通知"""
        if self.current_notification:
            anim = Animation(y=-dp(60), duration=0.3)
            anim.bind(
                on_complete=lambda a, w: self.remove_widget(w)
            )
            anim.start(self.current_notification)
            self.current_notification = None
