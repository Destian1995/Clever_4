from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from database import *

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.title = Label(text="Ваш результат", font_size=24)
        self.results = Label()
        self.back_btn = Button(text="В меню")
        self.back_btn.bind(on_press=self.go_back)
        layout.add_widget(self.title)
        layout.add_widget(self.results)
        layout.add_widget(self.back_btn)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'menu'

    def on_enter(self):
        conn = sqlite3.connect('data/user_progress.db')
        cursor = conn.cursor()
        cursor.execute('SELECT iq_score FROM progress WHERE id=1')
        iq = cursor.fetchone()[0]
        conn.close()

        self.results.text = f"🧠 Ваш IQ: {iq}"