from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.metrics import dp
import sys

KV = '''
<StyledButton@MDRaisedButton>:
    font_size: "20sp"
    size_hint: 0.9, None
    height: "65dp"
    md_bg_color: app.theme_cls.primary_light
    elevation: 12

<GlowCard@MDCard>:
    orientation: "vertical"
    size_hint: 0.85, None
    height: "75dp"
    padding: "10dp"
    spacing: "10dp"
    radius: [15]
    elevation: 8
    ripple_behavior: True
'''

Builder.load_string(KV)


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video = None
        self.title_container = None
        self._title_letters = []
        self.buttons_list = []
        Clock.schedule_once(self.setup_background)
        Clock.schedule_once(self.create_ui, 0.2)

    def setup_background(self, dt):
        # Градиентный фон с анимацией
        self.video = Video(
            source="files/video_menu.mp4",
            state="play",
            options={'eos': 'loop'},
            allow_stretch=True,
            keep_ratio=False
        )
        self.video.opacity = 0.6
        self.video.size_hint = (1, 1)
        self.video.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.add_widget(self.video, index=0)
        
        # Добавляем полупрозрачный оверлей для лучшей читаемости
        overlay = MDBoxLayout(
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=[0, 0, 0, 0.4]
        )
        self.add_widget(overlay, index=1)

    def create_ui(self, dt):
        layout = FloatLayout()

        # Заголовок с неоновым эффектом
        self.title_container = FloatLayout(
            size_hint=(1, None),
            height="80dp",
            pos_hint={"top": 0.95}
        )
        layout.add_widget(self.title_container)
        Clock.schedule_once(lambda dt: self.animate_title("Clever_4"), 0.5)

        # Блок кнопок с улучшенным дизайном
        btn_layout = MDBoxLayout(
            orientation="vertical",
            spacing="20dp",
            padding=["30dp", "20dp"],
            size_hint=(0.9, None),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        btn_layout.bind(minimum_height=btn_layout.setter('height'))

        # Фабрика кнопок с карточками и эффектами
        def build_icon_button(text, image_path, color_start, color_end, callback):
            card = MDCard(
                size_hint=(1, None),
                height="70dp",
                radius=[15],
                elevation=10,
                ripple_behavior=True,
                md_bg_color=color_start,
            )
            
            inner = BoxLayout(
                orientation="horizontal",
                spacing="15dp",
                padding=["15dp", "10dp"],
                size_hint=(1, 1),
            )

            # Иконка с тенью
            icon_container = FloatLayout(size_hint=(None, None), size=("40dp", "40dp"))
            icon = Image(
                source=image_path,
                size_hint=(None, None),
                size=("36dp", "36dp"),
                allow_stretch=True,
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            )
            icon_container.add_widget(icon)

            # Текст с градиентным эффектом
            label = MDLabel(
                text=text,
                halign="left",
                valign="middle",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size="22sp",
                bold=True,
                size_hint=(1, 1),
                markup=True
            )
            label.bind(size=label.setter('text_size'))

            inner.add_widget(icon_container)
            inner.add_widget(label)
            card.add_widget(inner)
            
            # Анимация при нажатии
            def on_press(instance):
                anim = Animation(md_bg_color=color_end, duration=0.15) + \
                       Animation(md_bg_color=color_start, duration=0.15)
                anim.start(instance)
                callback(instance)
            
            card.bind(on_press=on_press)
            return card

        # Кнопки с градиентными цветами (start_color, end_color)
        start_btn = build_icon_button(
            "Начать тест", "files/pict/test.png", 
            [0.15, 0.75, 0.35, 1], [0.25, 0.9, 0.45, 1], 
            self.start_test
        )
        stats_btn = build_icon_button(
            "Статистика", "files/pict/stat.png", 
            [0.08, 0.55, 0.75, 1], [0.15, 0.7, 0.9, 1], 
            self.show_stats
        )
        exit_btn = build_icon_button(
            "Выход", "files/pict/exit.png", 
            [0.75, 0.15, 0.15, 1], [0.9, 0.25, 0.25, 1], 
            self.exit_app
        )

        for btn in [start_btn, stats_btn, exit_btn]:
            self.buttons_list.append(btn)
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

            # Неоновое свечение (голубое)
            glow = MDLabel(
                text=char,
                halign="center",
                font_style="H4",
                theme_text_color="Custom",
                text_color=(0, 0.8, 1, 0),
                bold=True,
                font_size="42sp",
                size_hint=(None, None),
                size=("50dp", "70dp"),
                pos=(x_pos, 445),
            )

            # Тень — чёрная с размытием
            shadow = MDLabel(
                text=char,
                halign="center",
                font_style="H4",
                theme_text_color="Custom",
                text_color=(0, 0, 0, 0),
                bold=True,
                font_size="38sp",
                size_hint=(None, None),
                size=("45dp", "65dp"),
                pos=(x_pos + 2, 438),
            )

            # Основной текст — белый
            label = MDLabel(
                text=char,
                halign="center",
                font_style="H4",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0),
                bold=True,
                font_size="38sp",
                size_hint=(None, None),
                size=("45dp", "65dp"),
                pos=(x_pos, 445),
            )

            self.title_container.add_widget(glow)
            self.title_container.add_widget(shadow)
            self.title_container.add_widget(label)
            self._title_letters.append((glow, shadow, label))

        def fade_in(index):
            if index < len(self._title_letters):
                glow, shadow, label = self._title_letters[index]
                anim_glow = Animation(text_color=(0, 0.9, 1, 0.8), duration=0.3)
                anim_shadow = Animation(text_color=(0, 0, 0, 0.7), duration=0.2)
                anim_label = Animation(text_color=(1, 1, 1, 1), duration=0.2)
                anim_glow.start(glow)
                anim_shadow.start(shadow)
                anim_label.start(label)
                Clock.schedule_once(lambda dt: fade_in(index + 1), interval)
            else:
                Clock.schedule_once(self.remove_title, 3)

        fade_in(0)

    def remove_title(self, dt, interval=0.08):
        def fade_out(index):
            if index < len(self._title_letters):
                glow, shadow, label = self._title_letters[index]
                anim_glow = Animation(text_color=(0, 0.9, 1, 0), duration=0.25)
                anim_shadow = Animation(text_color=(0, 0, 0, 0), duration=0.2)
                anim_label = Animation(text_color=(1, 1, 1, 0), duration=0.2)
                anim_glow.start(glow)
                anim_shadow.start(shadow)
                anim_label.start(label)
                Clock.schedule_once(lambda dt: fade_out(index + 1), interval)
            else:
                Clock.schedule_once(lambda dt: self.animate_title("Clever_4"), 1)

        fade_out(0)

    def start_test(self, instance):
        # Помечаем, что при входе на экран теста нужно показать обратный отсчёт
        test_screen = self.manager.get_screen('test')
        setattr(test_screen, '_do_countdown', True)
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
