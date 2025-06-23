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
            'внимание': 0,
            'логика': 0,
            'обработка информации': 0,
            'счет в уме': 0,
            'память': 0
        }

    def on_enter(self):
        """Вызывается при входе на экран"""
        self.clear_widgets()
        self.generate_tasks()
        self.show_current_task()

    def generate_tasks(self):
        self.tasks = [
            ('внимание', ) + generate_attention_task(),
            ('логика', ) + generate_logic_task(),
            ('обработка информации', ) + generate_processing_task(),
            ('счет в уме', ) + generate_math_task(difficulty=2),
            ('память', ) + generate_memory_task()
        ]

    def show_current_task(self):
        layout = MDBoxLayout(orientation='vertical', padding="20dp", spacing="15dp")

        if self.current_index < len(self.tasks):
            category, sequence, question, answer = self.tasks[self.current_index]
            self.correct_answers.append(answer)

            # Создаем виджеты и сохраняем их как атрибуты
            self.task_label = MDLabel(
                text=sequence,
                halign="center",
                font_style="H6"
            )

            self.question_label = MDLabel(
                text="",
                halign="center",
                font_style="H6"
            )

            self.answer_input = MDTextField(
                hint_text="Введите ответ",
                multiline=False,
                opacity=0,
                disabled=True
            )

            self.check_btn = MDRaisedButton(  # ← Теперь это self.check_btn
                text="Проверить",
                on_press=self.submit_answer,
                pos_hint={"center_x": 0.5},
                opacity=0,
                disabled=True
            )

            layout.add_widget(self.task_label)
            layout.add_widget(self.question_label)
            layout.add_widget(self.answer_input)
            layout.add_widget(self.check_btn)
            self.add_widget(layout)

            # Устанавливаем таймер на исчезновение последовательности
            if category not in ['логика', 'счет в уме']:
                Clock.schedule_once(lambda dt: self.hide_sequence(category), 4)
            else:
                # Для логики и счета сразу показываем кнопки И вопрос
                _, task, question, answer = self.tasks[self.current_index]
                self.question_label.text = question  # ← Показываем вопрос сразу!

                self.answer_input.opacity = 1
                self.answer_input.disabled = False
                self.check_btn.opacity = 1
                self.check_btn.disabled = False

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
        user_answer = self.answer_input.text.strip()
        correct_answer = self.correct_answers[self.current_index]

        if user_answer:
            # Правильно распаковываем все 4 значения
            category, task, question, answer = self.tasks[self.current_index]

            is_correct = False
            if category == 'внимание':
                is_correct = check_attention_answer(user_answer, correct_answer)
            elif category == 'логика':
                is_correct = check_logic_answer(user_answer, correct_answer)
            elif category == 'обработка информации':
                is_correct = check_processing_answer(user_answer, correct_answer)
            elif category == 'счет в уме':
                is_correct = check_math_answer(user_answer, correct_answer)
            elif category == 'память':
                is_correct = check_memory_answer(user_answer, correct_answer)

            dialog = MDDialog(
                title="Результат",
                text="Верно!" if is_correct else f"Неверно. Правильный ответ: {correct_answer}",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_press=lambda x: (dialog.dismiss(), self.next_task())
                    )
                ]
            )
            dialog.open()

            self.scores[category] = 20 if is_correct else 0
            self.user_answers.append(user_answer)
            self.current_index += 1

    def hide_sequence(self, category):
        # Если это НЕ "логика" и НЕ "счет в уме", скрываем последовательность
        if category not in ['логика', 'счет в уме']:
            self.task_label.text = ""

        # Получаем данные текущего задания
        _, task, question, answer = self.tasks[self.current_index]

        # Показываем вопрос (всегда)
        self.question_label.text = question

        # Активируем ввод
        self.answer_input.opacity = 1
        self.answer_input.disabled = False
        self.check_btn.opacity = 1
        self.check_btn.disabled = False

    def next_task(self):
        """Переход к следующему заданию"""
        self.clear_widgets()
        self.show_current_task()

    def finish_test(self, instance=None):
        """Завершение теста и переход к результатам"""
        # Рассчитываем IQ на основе набранных баллов
        iq = calculate_iq(self.scores)
        # Сохраняем результаты + IQ
        save_scores(self.scores, iq)

        # Переход к экрану результатов
        self.manager.current = 'result'

    def restart_test(self):
        """Сбрасывает индекс и счётчики для повторного прохождения"""
        self.current_index = 0
        self.correct_answers.clear()
        self.user_answers.clear()
        self.scores = {
            'внимание': 0,
            'логика': 0,
            'обработка информации': 0,
            'счет в уме': 0,
            'память': 0
        }
        self.generate_tasks()
        self.show_current_task()