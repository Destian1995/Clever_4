from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

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

    def on_enter(self):
        # Получить результаты из БД и отобразить
        pass

    def go_back(self, instance):
        self.manager.current = 'menu'