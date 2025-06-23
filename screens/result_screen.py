from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# KivyMD импорты
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

# Работа с БД
from database import get_progress

KV = '''
<ResultScreen>:
    name: "result"
'''

Builder.load_string(KV)


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        # Общий фон экрана — темно-синий
        layout = MDBoxLayout(
            orientation='vertical',
            padding="20dp",
            spacing="30dp",
            md_bg_color=[0.1, 0.2, 0.4, 1]  # Темно-синий фон
        )

        # Карточка с результатом — темно-фиолетовая
        card = MDCard(
            orientation='vertical',
            padding="20dp",
            size_hint=(0.9, None),
            height="200dp",
            elevation=10,
            radius=[20],
            md_bg_color=[0.2, 0, 0.4, 1],  # Темно-фиолетовый фон
            line_color=[0.1, 0, 0.2, 1],   # Еще более темная рамка
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        # Показ IQ
        self.iq_label = MDLabel(
            text="Ваш IQ: --",
            halign="center",
            font_style="H2",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # Белый текст
            valign="middle"
        )

        # Кнопка "Пройти тест снова"
        restart_btn = MDRaisedButton(
            text="Пройти тест снова",
            on_press=self.restart_test,
            pos_hint={"center_x": 0.5},
            md_bg_color=[1, 1, 1, 1],     # Белый фон кнопки
            text_color=(0, 0, 0, 1),      # Черный текст
            elevation=8
        )

        # Кнопка "В меню"
        back_btn = MDRaisedButton(
            text="В меню",
            on_press=self.go_back,
            pos_hint={"center_x": 0.5},
            md_bg_color=[0.1, 0.5, 0.8, 1],  # Светло-синяя
            elevation=6
        )

        # Добавляем элементы в карточку и макет
        card.add_widget(self.iq_label)

        layout.add_widget(card)
        layout.add_widget(restart_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self):
        progress = get_progress()
        if progress:
            iq = progress.get('iq_score', 0)
            self.iq_label.text = f"Ваш IQ: {iq}"
        else:
            self.iq_label.text = "Ваш IQ: N/A"

    def restart_test(self, instance):
        self.manager.get_screen('test').restart_test()
        self.manager.current = 'test'

    def go_back(self, instance):
        self.manager.current = 'menu'