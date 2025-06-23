from kivy.uix.screenmanager import ScreenManager

# Подключаем KivyMD
from kivymd.app import MDApp
# Твои модули
from database import *
from screens.menu_screen import MenuScreen
from screens.test_screen import TestScreen
from screens.result_screen import StatsScreen
from screens.splash_screen import SplashScreen


class CleverApp(MDApp):  # Наследуемся от MDApp
    def build(self):
        init_db()
        check_and_reset_weekly()

        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TestScreen(name='test'))
        sm.add_widget(StatsScreen(name='result'))

        # Применяем стиль Material Design
        self.theme_cls.primary_palette = "Teal"  # Цветовая тема
        self.theme_cls.theme_style = "Light"     # Светлая/Тёмная тема
        return sm


if __name__ == '__main__':
    CleverApp().run()