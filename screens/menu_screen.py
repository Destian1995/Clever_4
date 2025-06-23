from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.videoplayer import Video
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
import sys

KV = '''
<StyledButton@MDRaisedButton>:
    font_size: "23sp"
    pos_hint: {"center_x": 0.5}
    md_bg_color: app.theme_cls.primary_light
'''

Builder.load_string(KV)


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video = None
        Clock.schedule_once(self.setup_background)
        Clock.schedule_once(self.create_ui, 0.2)

    def setup_background(self, dt):
        self.video = Video(
            source="files/video_menu.mp4",
            state="play",
            options={'eos': 'loop'},
            allow_stretch=True,
            keep_ratio=False
        )
        self.video.opacity = 0.8
        self.video.size_hint = (1, 1)
        self.video.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.add_widget(self.video, index=0)

    def create_ui(self, dt):
        # Основной контейнер
        layout = FloatLayout()

        # Заголовок (всегда сверху по центру)
        self.title = MDLabel(
            text="Clever_4",
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True,
            font_size="32sp",
            size_hint=(1, None),
            height="60dp",
            pos_hint={"top": 1}  # Прижимаем к верху
        )
        layout.add_widget(self.title)

        # Контейнер для кнопок (по центру экрана)
        btn_layout = MDBoxLayout(
            orientation="vertical",
            spacing="40dp",
            padding="20dp",
            size_hint=(0.8, None),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        btn_layout.bind(minimum_height=btn_layout.setter('height'))

        start_btn = MDRaisedButton(
            text="Начать тест",
            on_press=self.start_test,
            size_hint_y=None,
            height="60dp",
            font_size="18sp",
            md_bg_color=[0.2, 0.8, 0.4, 1],
            elevation=10
        )

        stats_btn = MDRaisedButton(
            text="Статистика",
            on_press=self.show_stats,
            size_hint_y=None,
            height="60dp",
            font_size="18sp",
            md_bg_color=[0.1, 0.6, 0.8, 1],
            elevation=6
        )

        exit_btn = MDRaisedButton(
            text="Выход",
            on_press=self.exit_app,
            size_hint_y=None,
            height="60dp",
            font_size="18sp",
            md_bg_color=[0.8, 0.2, 0.2, 1],
            elevation=6
        )

        btn_layout.add_widget(start_btn)
        btn_layout.add_widget(stats_btn)
        btn_layout.add_widget(exit_btn)

        layout.add_widget(btn_layout)
        self.add_widget(layout)

    def start_test(self, instance):
        self.manager.current = 'test'

    def show_stats(self, instance):
        self.manager.current = 'result'

    def exit_app(self, instance):
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            PythonActivity.mActivity.finish()
        else:
            Window.close() or sys.exit()
