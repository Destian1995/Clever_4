from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        title = Label(text="🧠 Clever 4", font_size=32)
        start_btn = Button(text="Начать тест")
        start_btn.bind(on_press=self.start_test)
        layout.add_widget(title)
        layout.add_widget(start_btn)
        self.add_widget(layout)

    def start_test(self, instance):
        self.manager.current = 'test'