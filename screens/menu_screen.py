from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.graphics import Rectangle, Color, Line
from kivy.core.image import Image as CoreImage
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.text.markup import MarkupLabel
from kivy.graphics import Rectangle, Color


KV = '''
<StyledButton@MDRaisedButton>:
    font_size: "18sp"
    pos_hint: {"center_x": 0.5}
    md_bg_color: app.theme_cls.primary_light
'''

Builder.load_string(KV)


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_texture = CoreImage("files/menu.png").texture
        self.bind(size=self._update_rect, pos=self._update_rect)
        with self.canvas.before:
            self.rect = Rectangle(texture=self.bg_texture, size=self.size, pos=self.pos)

        Clock.schedule_once(self.create_ui, 0.1)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def create_ui(self, dt):
        # Основной макет
        layout = MDBoxLayout(
            orientation="vertical",
            spacing="30dp",
            padding="20dp",
            size_hint=(None, None),
            width=300,
            height=400,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        layout.md_bg_color = [0, 0, 0, 0]

        # Заголовок с белым текстом и чёрной обводкой (через кастомную отрисовку)
        self.title = MDLabel(
            text="Клевер_4",
            halign="center",
            font_style="H3",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # Белый цвет текста
            bold=True,
            font_size="48sp"
        )

        # Кнопки
        start_btn = MDRaisedButton(
            text="Начать тест",
            on_press=self.start_test,
            size_hint=(1, None),
            height="60dp",
            font_size="20sp",
            md_bg_color=[0.2, 0.8, 0.4, 1],
            elevation=10,
            pos_hint={"center_x": 0.5}
        )

        stats_btn = MDRaisedButton(
            text="Статистика",
            on_press=self.show_stats,
            size_hint=(1, None),
            height="60dp",
            font_size="20sp",
            md_bg_color=[0.1, 0.6, 0.8, 1],
            elevation=6,
            pos_hint={"center_x": 0.5}
        )

        layout.add_widget(self.title)
        layout.add_widget(start_btn)
        layout.add_widget(stats_btn)
        self.add_widget(layout)

    def start_test(self, instance):
        self.manager.current = 'test'

    def show_stats(self, instance):
        self.manager.current = 'result'