from kivy.uix.floatlayout import FloatLayout
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.utils import platform
from kivy.core.window import Window

from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout


class DifficultyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video = None
        self.title = None
        Clock.schedule_once(self.setup_background)
        Clock.schedule_once(self.create_ui, 0.2)

    def setup_background(self, dt):
        self.video = Video(
            source="files/video_menu.mp4",  # можно использовать тот же файл
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
        layout = FloatLayout()

        self.title = MDLabel(
            text="",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True,
            font_size="28sp",
            size_hint=(1, None),
            height="60dp",
            pos_hint={"top": 0.95}
        )
        layout.add_widget(self.title)
        Clock.schedule_once(lambda dt: self.animate_title("Выберите уровень сложности"), 0.4)

        btn_layout = MDBoxLayout(
            orientation="vertical",
            spacing="25dp",
            padding="20dp",
            size_hint=(0.8, None),
            pos_hint={"center_x": 0.5, "center_y": 0.45},
        )
        btn_layout.bind(minimum_height=btn_layout.setter('height'))

        def button_animation(instance):
            anim = Animation(opacity=0.8, duration=0.1) + Animation(opacity=1, duration=0.1)
            anim.start(instance)

        easy_btn = MDRaisedButton(
            text="Разминка",
            on_press=lambda x: [button_animation(x), self.set_difficulty("easy")],
            size_hint=(1, None),
            height="60dp",
            font_size="20sp",
            md_bg_color=[0.2, 0.8, 0.2, 1],
            elevation=12
        )
        medium_btn = MDRaisedButton(
            text="Средний",
            on_press=lambda x: [button_animation(x), self.set_difficulty("medium")],
            size_hint=(1, None),
            height="60dp",
            font_size="20sp",
            md_bg_color=[0.8, 0.6, 0.2, 1],
            elevation=12
        )
        hard_btn = MDRaisedButton(
            text="Высокий",
            on_press=lambda x: [button_animation(x), self.set_difficulty("hard")],
            size_hint=(1, None),
            height="60dp",
            font_size="20sp",
            md_bg_color=[0.8, 0.2, 0.2, 1],
            elevation=12
        )

        for btn in [easy_btn, medium_btn, hard_btn]:
            btn_layout.add_widget(btn)

        self.add_widget(layout)
        layout.add_widget(btn_layout)

    def animate_title(self, text, interval=0.08):
        self.title.text = ""
        self._title_text = text
        self._title_index = 0

        def update_title(dt):
            if self._title_index < len(self._title_text):
                self.title.text += self._title_text[self._title_index]
                self._title_index += 1
            else:
                Clock.unschedule(self._title_anim_event)

        self._title_anim_event = Clock.schedule_interval(update_title, interval)

    def set_difficulty(self, difficulty):
        self.manager.get_screen('test').set_difficulty(difficulty)
        self.manager.current = 'test'
