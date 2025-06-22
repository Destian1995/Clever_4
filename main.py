from libraries_clever_4 import *
from database import init_db, check_and_reset_weekly
from screens.menu_screen import MenuScreen
from screens.test_screen import TestScreen
from screens.result_screen import ResultScreen

class CleverApp(App):
    def build(self):
        init_db()
        check_and_reset_weekly()

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TestScreen(name='test'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

if __name__ == '__main__':
    CleverApp().run()