from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from tasks.attention import generate_attention_task
from tasks.logic import generate_logic_task
from tasks.processing import generate_processing_task
from tasks.mental_math import generate_task as generate_math_task
from tasks.working_memory import generate_memory_task
from database import *

class TestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = []
        self.answers = []
        self.current_index = 0
        self.scores = {
            'attention': 0,
            'logic': 0,
            'processing': 0,
            'math': 0,
            'memory': 0
        }

    def on_enter(self):
        self.generate_tasks()
        self.show_current_task()

    def generate_tasks(self):
        # Здесь можно усложнять в зависимости от уровня
        self.tasks = [
            generate_attention_task(),
            generate_logic_task(),
            generate_processing_task(),
            generate_math_task(difficulty=2),
            generate_memory_task()
        ]

    def show_current_task(self):
        # Отображаем текущее задание
        pass

    def submit_answer(self, answer):
        # Сохраняем ответ, проверяем, переходим к следующему
        pass

    def finish_test(self):
        # Подсчёт баллов, переход к результату
        database.save_scores(self.scores)
        self.manager.current = 'result'