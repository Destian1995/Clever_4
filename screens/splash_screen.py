from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle

KV = '''
<SplashScreen>:
    name: "splash"
    on_enter: root.on_enter()
'''

Builder.load_string(KV)

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_texture = CoreImage("assets/splash.png").texture  # Загружаем текстуру
        with self.canvas.before:
            self.rect = Rectangle(texture=self.bg_texture, size=self.size)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        """Обновляем размеры фона при изменении окна"""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_enter(self, *args):
        """Вызывается при входе на экран"""
        self.build_ui()
        Clock.schedule_once(self.go_to_menu, 2)  # Ждём 2 секунды

    def build_ui(self):
        """Интерфейс поверх фона"""
        self.clear_widgets()

        layout = MDBoxLayout(
            orientation='vertical',
            padding="20dp",
            spacing="15dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None, None),
            width=200
        )
        self.add_widget(layout)

    def go_to_menu(self, dt):
        """Переход в главное меню после загрузки"""
        self.manager.current = 'menu'