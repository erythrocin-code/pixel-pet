"""
食物菜单 - 喂食界面
"""

from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp, sp


class FoodMenu:
    """食物菜单类"""
    
    FOODS = [
        {
            'id': 'apple',
            'name': '🍎 苹果',
            'desc': '饱腹+20 健康+5',
            'hunger': 20,
            'health': 5
        },
        {
            'id': 'candy',
            'name': '🍬 糖果',
            'desc': '饱腹+10 幸福+10',
            'hunger': 10,
            'health': -5,
            'happiness': 10
        },
        {
            'id': 'vegetable',
            'name': '🥦 蔬菜',
            'desc': '饱腹+15 健康+10',
            'hunger': 15,
            'health': 10
        },
        {
            'id': 'cake',
            'name': '🍰 蛋糕',
            'desc': '饱腹+30 幸福+20',
            'hunger': 30,
            'health': -10,
            'happiness': 20
        },
        {
            'id': 'potion',
            'name': '💊 药水',
            'desc': '健康+30',
            'health': 30
        },
        {
            'id': 'energy_bar',
            'name': '🍫 能量棒',
            'desc': '饱腹+25 能量+20',
            'hunger': 25,
            'energy': 20
        }
    ]
    
    def __init__(self, pet, notification_manager):
        self.pet = pet
        self.notification_manager = notification_manager
        self.popup = None
    
    def open(self):
        """打开食物菜单"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # 标题
        content.add_widget(Label(
            text='选择食物',
            font_size=sp(22),
            size_hint_y=0.1,
            color=(1, 0.95, 0.8, 1)
        ))
        
        # 食物网格
        grid = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=0.8
        )
        
        for food in self.FOODS:
            btn = self.create_food_button(food)
            grid.add_widget(btn)
        
        content.add_widget(grid)
        
        # 关闭按钮
        close_btn = Button(
            text='关闭',
            size_hint_y=0.1,
            background_color=(0.8, 0.2, 0.2, 1),
            background_normal=''
        )
        close_btn.bind(on_press=self.close)
        content.add_widget(close_btn)
        
        self.popup = Popup(
            title='',
            content=content,
            size_hint=(0.9, 0.7),
            background='',
            separator_height=0
        )
        self.popup.open()
    
    def create_food_button(self, food):
        """创建食物按钮"""
        btn_layout = BoxLayout(orientation='vertical', spacing=dp(2))
        
        # 食物名称
        name_label = Label(
            text=food['name'],
            font_size=sp(18),
            size_hint_y=0.6
        )
        btn_layout.add_widget(name_label)
        
        # 效果描述
        desc_label = Label(
            text=food['desc'],
            font_size=sp(12),
            size_hint_y=0.4,
            color=(0.8, 0.8, 0.8, 1)
        )
        btn_layout.add_widget(desc_label)
        
        # 创建按钮
        btn = Button(
            background_color=(0.42, 0.73, 0.19, 0.8),
            background_normal='',
            size_hint_y=None,
            height=dp(80)
        )
        btn.add_widget(btn_layout)
        btn.bind(on_press=lambda x: self.feed_pet(food))
        
        return btn
    
    def feed_pet(self, food):
        """喂食宠物"""
        if self.pet:
            success = self.pet.feed(food['id'])
            if success:
                self.notification_manager.show(
                    f"宠物吃了{food['name']}！",
                    'success'
                )
            else:
                self.notification_manager.show('喂食失败', 'warning')
        
        self.close()
    
    def close(self, *args):
        """关闭菜单"""
        if self.popup:
            self.popup.dismiss()
