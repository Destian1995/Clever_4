from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

# KivyMD импорты
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog

# Задачи
from tasks.attention import generate_attention_task, check_attention_answer
from tasks.logic import generate_logic_task, check_logic_answer
from tasks.processing import generate_processing_task, check_processing_answer
from tasks.mental_math import generate_task as generate_math_task, check_math_answer
from tasks.working_memory import generate_memory_task, check_memory_answer

# База данных и IQ
from database import save_scores
from utils.iq_calculator import calculate_iq

KV = '''
<StyledButton@MDRaisedButton>:
    font_size: "18sp"
    pos_hint: {"center_x": 0.5}
'''

Builder.load_string(KV)

class TestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = []
        self.current_index = 0
        self.user_answers = []
        self.correct_answers = []
        self.scores = {
            'attention': 0,
            'logic': 0,
            'processing': 0,
            'math': 0,
            'memory': 0
        }

    def on_enter(self):
        """Вызывается при входе на экран"""
        self.clear_widgets()
        self.generate_tasks()
        self.show_current_task()

    def generate_tasks(self):
        """Генерация 5 заданий по разным категориям"""
        self.tasks = [
            ('внимание', *generate_attention_task()),
            ('логика', *generate_logic_task()),
            ('обработка информации', *generate_processing_task()),
            ('счет в уме', *generate_math_task(difficulty=2)),
            ('память', *generate_memory_task())
        ]

    def show_current_task(self):
        """Отображает текущее задание"""
        layout = MDBoxLayout(orientation='vertical', padding="20dp", spacing="15dp")

        if self.current_index < len(self.tasks):
            category, task, answer = self.tasks[self.current_index]
            self.correct_answers.append(answer)

            # Заголовок
            title = MDLabel(
                text=f"Задание {self.current_index + 1}/5 — {category.capitalize()}",
                halign="center",
                font_style="H6"
            )
            layout.add_widget(title)

            # Текст задания
            question = MDLabel(text=str(task), halign="center", font_style="Body1")
            layout.add_widget(question)

            # Поле ввода
            self.answer_input = MDTextField(hint_text="Введите ответ", multiline=False)
            layout.add_widget(self.answer_input)

            # Кнопка проверки
            check_btn = MDRaisedButton(
                text="Проверить",
                on_press=self.submit_answer,
                pos_hint={"center_x": 0.5}
            )
            layout.add_widget(check_btn)

        else:
            finish_label = MDLabel(text="Тест завершён!", halign="center", font_style="H5")
            finish_btn = MDRaisedButton(
                text="Посмотреть результаты",
                on_press=self.finish_test,
                pos_hint={"center_x": 0.5}
            )
            layout.add_widget(finish_label)
            layout.add_widget(finish_btn)

        self.add_widget(layout)

    def submit_answer(self, instance):
        """Обработка ответа пользователя"""
        user_answer = self.answer_input.text.strip()
        correct_answer = self.correct_answers[self.current_index]

        if user_answer:
            # Проверяем ответ
            category, _, _ = self.tasks[self.current_index]
            is_correct = False

            if category == 'attention':
                is_correct = check_attention_answer(user_answer, correct_answer)
            elif category == 'logic':
                is_correct = check_logic_answer(user_answer, correct_answer)
            elif category == 'processing':
                is_correct = check_processing_answer(user_answer, correct_answer)
            elif category == 'math':
                is_correct = check_math_answer(user_answer, correct_answer)
            elif category == 'memory':
                is_correct = check_memory_answer(user_answer, correct_answer)

            # Простой диалог с результатом
            dialog = MDDialog(
                title="Результат",
                text="✅ Верно!" if is_correct else f"❌ Неверно. Правильный ответ: {correct_answer}",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_press=lambda x: (dialog.dismiss(), self.next_task())
                    )
                ]
            )
            dialog.open()

            # Сохраняем баллы (если верно — даём 20 баллов за задание)
            self.scores[category] = 20 if is_correct else 0
            self.user_answers.append(user_answer)
            self.current_index += 1

    def next_task(self):
        """Переход к следующему заданию"""
        self.clear_widgets()
        self.show_current_task()

    def finish_test(self, instance=None):
        """Завершение теста и переход к результатам"""
        save_scores(self.scores)
        self.manager.current = 'result'