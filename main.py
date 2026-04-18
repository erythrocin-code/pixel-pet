"""
像素风格虚拟宠物养成游戏 - 主程序
类似拓麻歌子的经典玩法
"""

import os
import json
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.utils import platform
from kivy.metrics import dp, sp

# 导入游戏模块
from pet import Pet
from time_manager import TimeManager
from save_system import SaveSystem
from pixel_pet import PixelPetWidget
from food_menu import FoodMenu
from notifications import NotificationManager


class MainMenuScreen(Screen):
    """主菜单界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = FloatLayout()
        
        # 背景色
        with layout.canvas.before:
            Color(0.176, 0.106, 0.412, 1)  # 深紫色背景
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        
        layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # 标题
        title = Label(
            text='[b]像素宠物[/b]',
            markup=True,
            font_size=sp(48),
            pos_hint={'center_x': 0.5, 'center_y': 0.75},
            color=(1, 0.95, 0.8, 1)
        )
        layout.add_widget(title)
        
        # 副标题
        subtitle = Label(
            text='一个温馨的虚拟宠物养成游戏',
            font_size=sp(16),
            pos_hint={'center_x': 0.5, 'center_y': 0.68},
            color=(0.7, 0.6, 0.9, 1)
        )
        layout.add_widget(subtitle)
        
        # 预览宠物
        self.preview_pet = PixelPetWidget(
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            pos_hint={'center_x': 0.5, 'center_y': 0.48}
        )
        layout.add_widget(self.preview_pet)
        
        # 继续游戏按钮
        continue_btn = self.create_menu_button(
            '继续游戏',
            {'center_x': 0.5, 'center_y': 0.32},
            self.continue_game
        )
        layout.add_widget(continue_btn)
        
        # 新游戏按钮
        new_btn = self.create_menu_button(
            '新游戏',
            {'center_x': 0.5, 'center_y': 0.22},
            self.new_game
        )
        layout.add_widget(new_btn)
        
        # 设置按钮
        settings_btn = self.create_menu_button(
            '设置',
            {'center_x': 0.5, 'center_y': 0.12},
            self.open_settings
        )
        layout.add_widget(settings_btn)
        
        self.add_widget(layout)
    
    def create_menu_button(self, text, pos_hint, callback):
        btn = Button(
            text=text,
            size_hint=(0.6, 0.07),
            pos_hint=pos_hint,
            background_color=(0.42, 0.73, 0.19, 1),
            background_normal='',
            font_size=sp(20),
            color=(1, 1, 1, 1)
        )
        btn.bind(on_press=callback)
        return btn
    
    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def continue_game(self, instance):
        app = App.get_running_app()
        if app.save_system.has_save():
            app.load_game()
            self.manager.current = 'game'
        else:
            self.show_no_save_popup()
    
    def new_game(self, instance):
        self.show_name_popup()
    
    def show_name_popup(self):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        content.add_widget(Label(
            text='给你的宠物取个名字吧！',
            font_size=sp(18)
        ))
        
        from kivy.uix.textinput import TextInput
        self.name_input = TextInput(
            text='小萌',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size=sp(20)
        )
        content.add_widget(self.name_input)
        
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        ok_btn = Button(text='确定', background_color=(0.42, 0.73, 0.19, 1))
        cancel_btn = Button(text='取消', background_color=(0.8, 0.2, 0.2, 1))
        
        btn_layout.add_widget(ok_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='新游戏',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        ok_btn.bind(on_press=lambda x: self.start_new_game(popup))
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def start_new_game(self, popup):
        name = self.name_input.text.strip() or '小萌'
        popup.dismiss()
        
        app = App.get_running_app()
        app.create_new_game(name)
        self.manager.current = 'game'
    
    def show_no_save_popup(self):
        popup = Popup(
            title='提示',
            content=Label(text='没有找到存档，请开始新游戏'),
            size_hint=(0.6, 0.3)
        )
        popup.open()
    
    def open_settings(self, instance):
        self.manager.current = 'settings'


class GameScreen(Screen):
    """游戏主界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        self.game_loop = None
    
    def build_ui(self):
        self.main_layout = FloatLayout()
        
        # 背景
        with self.main_layout.canvas.before:
            self.bg_color = Color(0.176, 0.106, 0.412, 1)
            self.bg_rect = Rectangle(pos=self.main_layout.pos, size=self.main_layout.size)
        
        self.main_layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # 顶部信息栏
        self.top_bar = self.create_top_bar()
        self.main_layout.add_widget(self.top_bar)
        
        # 宠物显示区域
        self.pet_widget = PixelPetWidget(
            size_hint=(None, None),
            size=(dp(200), dp(200)),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )
        self.main_layout.add_widget(self.pet_widget)
        
        # 状态显示区域
        self.status_panel = self.create_status_panel()
        self.main_layout.add_widget(self.status_panel)
        
        # 操作按钮区域
        self.action_buttons = self.create_action_buttons()
        self.main_layout.add_widget(self.action_buttons)
        
        # 通知管理器
        self.notification_manager = NotificationManager(
            size_hint=(1, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'y': 0.02}
        )
        self.main_layout.add_widget(self.notification_manager)
        
        self.add_widget(self.main_layout)
    
    def create_top_bar(self):
        bar = BoxLayout(
            size_hint=(1, 0.08),
            pos_hint={'top': 1},
            padding=[dp(10), 0]
        )
        
        with bar.canvas.before:
            Color(0.1, 0.06, 0.25, 0.9)
            Rectangle(pos=bar.pos, size=bar.size)
        
        self.pet_name_label = Label(
            text='小萌',
            font_size=sp(18),
            size_hint=(0.3, 1),
            color=(1, 1, 1, 1)
        )
        
        self.time_label = Label(
            text='00:00',
            font_size=sp(24),
            size_hint=(0.4, 1),
            color=(1, 0.95, 0.8, 1)
        )
        
        self.day_label = Label(
            text='第1天',
            font_size=sp(16),
            size_hint=(0.2, 1),
            color=(0.7, 0.9, 1, 1)
        )
        
        self.sleep_btn = Button(
            text='🌙',
            font_size=sp(24),
            size_hint=(0.1, 1),
            background_color=(0, 0, 0, 0),
            background_normal=''
        )
        self.sleep_btn.bind(on_press=self.toggle_sleep_mode)
        
        bar.add_widget(self.pet_name_label)
        bar.add_widget(self.time_label)
        bar.add_widget(self.day_label)
        bar.add_widget(self.sleep_btn)
        
        return bar
    
    def create_status_panel(self):
        panel = GridLayout(
            cols=2,
            size_hint=(0.9, 0.2),
            pos_hint={'center_x': 0.5, 'y': 0.25},
            spacing=dp(10),
            padding=dp(10)
        )
        
        self.status_bars = {}
        statuses = [
            ('hunger', '🍖 饱腹度', (1, 0.6, 0.2, 1)),
            ('happiness', '⭐ 幸福度', (1, 0.9, 0.2, 1)),
            ('health', '❤️ 健康度', (1, 0.3, 0.3, 1)),
            ('cleanliness', '✨ 清洁度', (0.3, 0.7, 1, 1)),
            ('energy', '⚡ 能量值', (0.3, 1, 0.3, 1))
        ]
        
        for key, label_text, color in statuses:
            container = BoxLayout(orientation='vertical', spacing=dp(2))
            
            label = Label(
                text=label_text,
                font_size=sp(14),
                size_hint_y=0.4,
                color=(0.9, 0.9, 0.9, 1)
            )
            container.add_widget(label)
            
            bar_bg = Widget(size_hint_y=0.6)
            with bar_bg.canvas:
                Color(0.2, 0.2, 0.2, 1)
                self.status_bars[f'{key}_bg'] = Rectangle(
                    pos=bar_bg.pos,
                    size=bar_bg.size
                )
                Color(*color)
                self.status_bars[key] = Rectangle(
                    pos=bar_bg.pos,
                    size=(bar_bg.size[0] * 0.8, bar_bg.size[1])
                )
            
            container.add_widget(bar_bg)
            panel.add_widget(container)
        
        return panel
    
    def create_action_buttons(self):
        buttons = [
            ('🍎', '喂食', self.show_food_menu),
            ('🎮', '玩耍', self.play_with_pet),
            ('🛁', '清洁', self.clean_pet),
            ('💤', '休息', self.pet_sleep),
            ('💊', '治疗', self.heal_pet)
        ]
        
        layout = GridLayout(
            cols=5,
            size_hint=(0.95, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.14},
            spacing=dp(5)
        )
        
        for icon, text, callback in buttons:
            btn = Button(
                text=f'{icon}\n{text}',
                font_size=sp(16),
                background_color=(0.42, 0.73, 0.19, 0.9),
                background_normal='',
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=callback)
            layout.add_widget(btn)
        
        return layout
    
    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def on_enter(self):
        """进入游戏界面时启动游戏循环"""
        self.game_loop = Clock.schedule_interval(self.update, 1/30)  # 30 FPS
        self.update_display()
    
    def on_leave(self):
        """离开游戏界面时停止游戏循环"""
        if self.game_loop:
            self.game_loop.cancel()
    
    def update(self, dt):
        """游戏主循环"""
        app = App.get_running_app()
        if app.pet:
            app.pet.update(dt, app.time_manager.is_player_sleeping)
            self.update_display()
            self.update_background()
    
    def update_display(self):
        """更新显示"""
        app = App.get_running_app()
        if not app.pet:
            return
        
        pet = app.pet
        
        # 更新顶部信息
        self.pet_name_label.text = pet.name
        self.time_label.text = datetime.now().strftime('%H:%M')
        self.day_label.text = f'第{pet.age_days}天'
        
        # 更新状态条
        self.update_status_bar('hunger', pet.hunger / 100)
        self.update_status_bar('happiness', pet.happiness / 100)
        self.update_status_bar('health', pet.health / 100)
        self.update_status_bar('cleanliness', pet.cleanliness / 100)
        self.update_status_bar('energy', pet.energy / 100)
        
        # 更新宠物显示
        self.pet_widget.set_state(pet)
    
    def update_status_bar(self, key, value):
        """更新单个状态条"""
        if key in self.status_bars:
            bar = self.status_bars[key]
            # 保持高度，改变宽度
            bar.size = (bar.size[0], bar.size[1])  # 这里需要修正
    
    def update_background(self):
        """根据时间更新背景颜色"""
        hour = datetime.now().hour
        
        if 6 <= hour < 12:  # 早晨
            self.bg_color.rgba = (0.53, 0.81, 0.92, 1)  # 天蓝色
        elif 12 <= hour < 18:  # 下午
            self.bg_color.rgba = (1, 0.88, 0.73, 1)  # 暖黄色
        elif 18 <= hour < 21:  # 傍晚
            self.bg_color.rgba = (1, 0.55, 0, 1)  # 橙色
        else:  # 夜晚
            self.bg_color.rgba = (0.098, 0.098, 0.44, 1)  # 深蓝色
    
    def show_food_menu(self, instance):
        """显示食物菜单"""
        app = App.get_running_app()
        food_menu = FoodMenu(app.pet, self.notification_manager)
        food_menu.open()
    
    def play_with_pet(self, instance):
        """和宠物玩耍"""
        app = App.get_running_app()
        if app.pet.energy < 20:
            self.notification_manager.show('宠物太累了，需要休息！', 'warning')
            return
        
        app.pet.play()
        self.pet_widget.play_animation()
        self.notification_manager.show('和宠物玩耍中...', 'info')
    
    def clean_pet(self, instance):
        """清洁宠物"""
        app = App.get_running_app()
        app.pet.clean()
        self.pet_widget.clean_animation()
        self.notification_manager.show('宠物变得干净了！', 'success')
    
    def pet_sleep(self, instance):
        """让宠物睡觉"""
        app = App.get_running_app()
        app.pet.sleep()
        if app.pet.is_sleeping:
            self.notification_manager.show('宠物睡着了...', 'info')
        else:
            self.notification_manager.show('宠物醒来了！', 'info')
    
    def heal_pet(self, instance):
        """治疗宠物"""
        app = App.get_running_app()
        if not app.pet.is_sick:
            self.notification_manager.show('宠物很健康！', 'info')
            return
        
        app.pet.heal()
        self.notification_manager.show('宠物被治愈了！', 'success')
    
    def toggle_sleep_mode(self, instance):
        """切换玩家睡眠模式"""
        app = App.get_running_app()
        
        if app.time_manager.is_player_sleeping:
            # 醒来
            app.time_manager.wake_up()
            self.sleep_btn.text = '🌙'
            self.notification_manager.show('早上好！', 'success')
        else:
            # 准备睡觉
            self.show_sleep_popup()
    
    def show_sleep_popup(self):
        """显示睡觉确认弹窗"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        content.add_widget(Label(
            text='准备睡觉了吗？\n宠物也会休息哦~',
            font_size=sp(18),
            halign='center'
        ))
        
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        ok_btn = Button(text='晚安', background_color=(0.42, 0.73, 0.19, 1))
        cancel_btn = Button(text='再玩一会儿', background_color=(0.8, 0.2, 0.2, 1))
        
        btn_layout.add_widget(ok_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='晚安',
            content=content,
            size_hint=(0.8, 0.35),
            auto_dismiss=True
        )
        
        ok_btn.bind(on_press=lambda x: self.enter_sleep_mode(popup))
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def enter_sleep_mode(self, popup):
        """进入睡眠模式"""
        popup.dismiss()
        app = App.get_running_app()
        app.time_manager.go_to_sleep()
        app.pet.sleep()
        self.sleep_btn.text = '☀️'
        self.notification_manager.show('晚安~ Zzz...', 'info')


class SettingsScreen(Screen):
    """设置界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        with layout.canvas.before:
            Color(0.176, 0.106, 0.412, 1)
            Rectangle(pos=layout.pos, size=layout.size)
        
        # 标题
        layout.add_widget(Label(
            text='[b]设置[/b]',
            markup=True,
            font_size=sp(32),
            size_hint_y=0.15,
            color=(1, 0.95, 0.8, 1)
        ))
        
        # 睡眠时间设置
        sleep_section = BoxLayout(orientation='vertical', size_hint_y=0.3)
        sleep_section.add_widget(Label(
            text='睡眠时间设置',
            font_size=sp(20),
            color=(0.7, 0.9, 1, 1)
        ))
        
        time_layout = BoxLayout(size_hint_y=0.5)
        time_layout.add_widget(Label(text='睡觉时间:', font_size=sp(16)))
        
        from kivy.uix.spinner import Spinner
        self.sleep_time_spinner = Spinner(
            text='23:00',
            values=[f'{h:02d}:00' for h in range(24)],
            size_hint=(0.4, 1)
        )
        time_layout.add_widget(self.sleep_time_spinner)
        
        time_layout.add_widget(Label(text='起床时间:', font_size=sp(16)))
        self.wake_time_spinner = Spinner(
            text='07:00',
            values=[f'{h:02d}:00' for h in range(24)],
            size_hint=(0.4, 1)
        )
        time_layout.add_widget(self.wake_time_spinner)
        
        sleep_section.add_widget(time_layout)
        layout.add_widget(sleep_section)
        
        # 音效开关
        sound_layout = BoxLayout(size_hint_y=0.15)
        sound_layout.add_widget(Label(
            text='音效',
            font_size=sp(20),
            size_hint_x=0.7
        ))
        from kivy.uix.switch import Switch
        self.sound_switch = Switch(active=True, size_hint_x=0.3)
        sound_layout.add_widget(self.sound_switch)
        layout.add_widget(sound_layout)
        
        # 震动开关
        vibrate_layout = BoxLayout(size_hint_y=0.15)
        vibrate_layout.add_widget(Label(
            text='震动反馈',
            font_size=sp(20),
            size_hint_x=0.7
        ))
        self.vibrate_switch = Switch(active=True, size_hint_x=0.3)
        vibrate_layout.add_widget(self.vibrate_switch)
        layout.add_widget(vibrate_layout)
        
        # 返回按钮
        back_btn = Button(
            text='返回',
            size_hint_y=0.15,
            background_color=(0.8, 0.2, 0.2, 1),
            background_normal='',
            font_size=sp(20)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        app = App.get_running_app()
        app.save_settings(
            self.sleep_time_spinner.text,
            self.wake_time_spinner.text,
            self.sound_switch.active,
            self.vibrate_switch.active
        )
        self.manager.current = 'main'


class TamagotchiApp(App):
    """主应用类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pet = None
        self.time_manager = TimeManager()
        self.save_system = SaveSystem()
        self.settings = {
            'sleep_time': '23:00',
            'wake_time': '07:00',
            'sound': True,
            'vibrate': True
        }
    
    def build(self):
        """构建应用界面"""
        self.title = '像素宠物'
        
        # 设置窗口大小（用于桌面测试）
        if platform != 'android':
            Window.size = (400, 700)
        
        # 加载设置
        self.load_settings()
        
        # 创建屏幕管理器
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainMenuScreen(name='main'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm
    
    def create_new_game(self, name):
        """创建新游戏"""
        self.pet = Pet(name)
        self.time_manager.reset()
        self.save_game()
    
    def load_game(self):
        """加载存档"""
        data = self.save_system.load()
        if data:
            self.pet = Pet.from_dict(data['pet'])
            self.time_manager.load(data.get('time_manager', {}))
            
            # 计算离线效果
            offline_time = self.save_system.get_offline_time()
            if offline_time > 0:
                self.pet.apply_offline_effects(offline_time)
    
    def save_game(self):
        """保存游戏"""
        if self.pet:
            data = {
                'pet': self.pet.to_dict(),
                'time_manager': self.time_manager.to_dict(),
                'save_time': datetime.now().isoformat()
            }
            self.save_system.save(data)
    
    def load_settings(self):
        """加载设置"""
        settings = self.save_system.load_settings()
        if settings:
            self.settings.update(settings)
    
    def save_settings(self, sleep_time, wake_time, sound, vibrate):
        """保存设置"""
        self.settings = {
            'sleep_time': sleep_time,
            'wake_time': wake_time,
            'sound': sound,
            'vibrate': vibrate
        }
        self.time_manager.set_sleep_schedule(sleep_time, wake_time)
        self.save_system.save_settings(self.settings)
    
    def on_pause(self):
        """应用暂停时保存"""
        self.save_game()
        return True
    
    def on_resume(self):
        """应用恢复时"""
        if self.pet:
            offline_time = self.save_system.get_offline_time()
            if offline_time > 60:  # 超过1分钟
                self.pet.apply_offline_effects(offline_time)
    
    def on_stop(self):
        """应用停止时保存"""
        self.save_game()


if __name__ == '__main__':
    TamagotchiApp().run()
