from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
import sys

KV = '''
<StyledButton@MDRaisedButton>:
    font_size: "20sp"
    size_hint: 0.9, None
    height: "65dp"
    md_bg_color: app.theme_cls.primary_light
    elevation: 12
'''

Builder.load_string(KV)


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video = None
        self.title_container = None
        self._title_letters = []
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
        layout = FloatLayout()

        # Заголовок (контейнер)
        self.title_container = FloatLayout(
            size_hint=(1, None),
            height="60dp",
            pos_hint={"top": 1}
        )
        layout.add_widget(self.title_container)
        Clock.schedule_once(lambda dt: self.animate_title("Clever_4"), 0.5)

        # Блок кнопок
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

        # Фабрика кнопок с иконкой
        def build_icon_button(text, image_path, bg_color, callback):
            box = MDRaisedButton(
                size_hint=(1, None),
                height="65dp",
                md_bg_color=bg_color,
                elevation=12,
                on_press=lambda x: [button_animation(x), callback(x)]
            )

            inner = BoxLayout(
                orientation="horizontal",
                spacing="12dp",
                padding=[10, 0, 10, 0],  # убираем вертикальный отступ
                size_hint=(1, 1),
                pos_hint={"center_y": 0.5}
            )

            icon = Image(
                source=image_path,
                size_hint=(None, None),
                size=("32dp", "32dp"),
                allow_stretch=True,
                pos_hint={"center_y": 0.5}  # центр по вертикали
            )

            label = MDLabel(
                text=text,
                halign="left",
                valign="middle",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size="20sp",
                size_hint=(1, 1)
            )
            label.bind(size=label.setter('text_size'))  # выравнивание по центру

            inner.add_widget(icon)
            inner.add_widget(label)
            box.add_widget(inner)
            return box

        # Кнопки
        start_btn = build_icon_button(
            "Начать тест", "files/pict/test.png", [0.2, 0.8, 0.4, 1], self.start_test
        )
        stats_btn = build_icon_button(
            "Статистика", "files/pict/stat.png", [0.1, 0.6, 0.8, 1], self.show_stats
        )
        exit_btn = build_icon_button(
            "Выход", "files/pict/exit.png", [0.8, 0.2, 0.2, 1], self.exit_app
        )

        for btn in [start_btn, stats_btn, exit_btn]:
            btn_layout.add_widget(btn)

        layout.add_widget(btn_layout)
        self.add_widget(layout)

    def animate_title(self, text, interval=0.1):
        self.title_container.clear_widgets()
        self._title_letters = []

        total_len = len(text)
        spacing = Window.width / (total_len + 2)

        for i, char in enumerate(text):
            x_pos = Window.width / 2 - (total_len / 2.0 * spacing) + (i * spacing)

            # Тень — чёрная
            shadow = MDLabel(
                text=char,
                halign="center",
                font_style="H4",
                theme_text_color="Custom",
                text_color=(0, 0, 0, 0),
                bold=True,
                font_size="36sp",
                size_hint=(None, None),
                size=("40dp", "60dp"),
                pos=(x_pos + 1, 442),
            )

            # Основной текст — белый
            label = MDLabel(
                text=char,
                halign="center",
                font_style="H4",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0),
                bold=True,
                font_size="36sp",
                size_hint=(None, None),
                size=("40dp", "60dp"),
                pos=(x_pos, 450),
            )

            self.title_container.add_widget(shadow)
            self.title_container.add_widget(label)
            self._title_letters.append((shadow, label))

        def fade_in(index):
            if index < len(self._title_letters):
                shadow, label = self._title_letters[index]
                anim_shadow = Animation(text_color=(0, 0, 0, 1), duration=0.2)
                anim_label = Animation(text_color=(1, 1, 1, 1), duration=0.2)
                anim_shadow.start(shadow)
                anim_label.start(label)
                Clock.schedule_once(lambda dt: fade_in(index + 1), interval)
            else:
                Clock.schedule_once(self.remove_title, 3)

        fade_in(0)

    def remove_title(self, dt, interval=0.08):
        def fade_out(index):
            if index < len(self._title_letters):
                shadow, label = self._title_letters[index]
                anim_shadow = Animation(text_color=(0, 0, 0, 0), duration=0.2)
                anim_label = Animation(text_color=(1, 1, 1, 0), duration=0.2)
                anim_shadow.start(shadow)
                anim_label.start(label)
                Clock.schedule_once(lambda dt: fade_out(index + 1), interval)
            else:
                Clock.schedule_once(lambda dt: self.animate_title("Clever_4"), 1)

        fade_out(0)

    def start_test(self, instance):
        self.manager.current = 'difficulty'

    def show_stats(self, instance):
        self.manager.current = 'result'

    def exit_app(self, instance):
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            PythonActivity.mActivity.finish()
        else:
            Window.close() or sys.exit()
