from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

# KivyMD импорты
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView

# Работа с БД
from database import get_progress


KV = '''
<StatsScreen>:
    name: "stats"
'''

Builder.load_string(KV)


class Divider(Widget):
    def __init__(self, height=dp(1), color=(1, 1, 1, 0.2), **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = height
        with self.canvas:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_texture = CoreImage("files/menu.png").texture
        with self.canvas.before:
            self.rect = Rectangle(texture=self.bg_texture, size=Window.size)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def on_pre_enter(self, *args):
        self.build_ui()

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def build_ui(self, dt=None):
        self.clear_widgets()

        # Основной контейнер
        layout = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Заголовок экрана
        title = MDLabel(
            text="Статистика",
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(title)

        progress = get_progress()

        # === Блок с IQ — выносим отдельно и поднимаем вверх ===
        iq_container = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=[0, dp(10), 0, dp(10)]
        )

        if progress:
            iq_value = progress.get("iq_score", 0)
            self.iq_label = MDLabel(
                text=f"IQ: {iq_value}",
                font_style="H2",
                theme_text_color="Custom",
                text_color=(1, 0.85, 0.2, 1),
                halign="center",
                valign="middle",
                font_size="48sp",
                bold=True
            )
            self.iq_label.bind(size=self.iq_label.setter('text_size'))
            iq_container.add_widget(self.iq_label)
            layout.add_widget(iq_container)

            categories = {
                'attention_score': 'Внимание',
                'logic_score': 'Логика',
                'processing_score': 'Обработка информации',
                'math_score': 'Счет в уме',
                'memory_score': 'Память',
            }

            # Карточка с таблицей статистики
            card = MDCard(
                padding=dp(20),
                size_hint=(1, None),
                height=Window.height * 0.5,
                elevation=10,
                md_bg_color=[0.1, 0.1, 0.1, 0.9],
                radius=[20],
                orientation='vertical'
            )

            table = MDBoxLayout(orientation='vertical', spacing=dp(8))
            for key, name in categories.items():
                row = MDBoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))

                label = MDLabel(
                    text=name,
                    halign="left",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    size_hint_x=0.6,
                    valign='middle'
                )
                label.bind(size=label.setter('text_size'))

                value = progress.get(key, 0)
                score = MDLabel(
                    text=str(value),
                    halign="right",
                    bold=True,
                    theme_text_color="Custom",
                    text_color=(0.2, 1, 0.8, 1),
                    size_hint_x=0.4,
                    valign='middle'
                )
                score.bind(size=score.setter('text_size'))

                row.add_widget(label)
                row.add_widget(score)
                table.add_widget(row)

            card.add_widget(table)
            layout.add_widget(card)

        else:
            no_data = MDLabel(
                text="Нет данных. Пройдите тест хотя бы один раз.",
                halign="center",
                theme_text_color="Error",
                size_hint_y=None,
                height=dp(40)
            )
            layout.add_widget(no_data)

        # === Кнопка "Пройти тест снова" — делаем её больше и добавляем плавное мигание ===
        self.restart_btn = MDRaisedButton(
            text="Пройти тест снова",
            on_press=self.restart_test,
            pos_hint={"center_x": 0.5},
            size_hint=(0.8, None),
            height=dp(70),
            md_bg_color=[1, 1, 1, 1],  # Белый фон кнопки
            text_color=(0, 0, 0, 1),  # Черный текст
            elevation=10,
            font_size="20sp"
        )
        layout.add_widget(self.restart_btn)

        # Запуск плавной анимации
        Clock.schedule_once(self.start_blinking, 0.5)

        # Кнопка назад
        back_btn = MDRaisedButton(
            text="Назад",
            on_press=self.go_back,
            pos_hint={"center_x": 0.5},
            size_hint=(0.6, None),
            height=dp(48),
            md_bg_color=[0.1, 0.5, 0.8, 1],
            text_color=(1, 1, 1, 1),
            elevation=6
        )
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def start_blinking(self, dt):
        """Запуск бесконечной анимации плавного мигания"""
        if not hasattr(self, 'restart_btn'):
            return

        # Анимация уменьшения прозрачности
        anim = Animation(md_bg_color=[1, 1, 1, 0.4], duration=0.8) + \
               Animation(md_bg_color=[1, 1, 1, 1], duration=0.8)
        anim.repeat = True
        anim.start(self.restart_btn)

    def restart_test(self, instance):
        self.manager.get_screen('test').restart_test()
        self.manager.current = 'test'

    def go_back(self, instance):
        self.manager.current = 'menu'