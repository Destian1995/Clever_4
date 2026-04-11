from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

# KivyMD импорты
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, PushMatrix, PopMatrix, Scale, Translate
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty, ListProperty
import math
# Задачи
from tasks.attention import generate_attention_task, check_attention_answer
from tasks.logic import generate_logic_task, check_logic_answer
from tasks.processing import generate_processing_task, check_processing_answer
from tasks.mental_math import generate_task as generate_math_task, check_math_answer
from tasks.working_memory import generate_memory_task, check_memory_answer

# Адаптивный контроллер
from utils.adaptive import AdaptiveController

# База данных и IQ
from database import save_scores
from utils.iq_calculator import calculate_iq

KV = '''
<StyledButton@MDRaisedButton>:
    font_size: "18sp"
    pos_hint: {"center_x": 0.5}
'''

Builder.load_string(KV)

class CircularCountdown(Widget):
    value = NumericProperty(0)
    def __init__(self, total_time=4, on_complete=None, **kwargs):
        super().__init__(**kwargs)
        self.total_time = total_time
        self.value = 0
        self.elapsed_time = 0
        self.alpha = 1  # прозрачность кольца
        self._on_complete = on_complete

        # Центральная метка
        self.text_label = MDLabel(
            text=str(total_time),
            halign="center",
            valign="middle",
            font_style="H4",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=("100dp", "100dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.add_widget(self.text_label)

        # Пульсация текста
        Clock.schedule_interval(self.animate_pulse, 1 / 60)

    def on_value(self, *args):
        remaining = max(0, round(self.total_time - self.value, 1))
        self.text_label.text = str(remaining)

    def animate_pulse(self, dt):
        scale = 1.0 + 0.08 * math.sin(self.elapsed_time * 4)
        self.text_label.font_size = f"{scale * 48}sp"
        self.elapsed_time += dt

    def draw(self):
        self.canvas.before.clear()
        with self.canvas.before:
            PushMatrix()
            width = min(self.width, self.height) / 2
            line_width = 12
            cx, cy = self.center
            progress = 1 - (self.value / self.total_time)
            angle = 360 * progress

            # Технологичный цвет: неоново-синий с затуханием
            Color(0.2, 0.7, 1, self.alpha)  # RGBA

            Line(circle=(cx, cy, width - line_width, 90, 90 + angle), width=line_width, cap='round')

            PopMatrix()

    def update(self, dt):
        self.value += dt
        if self.value >= self.total_time:
            self.value = self.total_time
            self.draw()
            # Вызовим callback завершения в main loop, если он задан
            try:
                if callable(self._on_complete):
                    Clock.schedule_once(lambda dt: self._on_complete(), 0)
            except Exception:
                pass
            self.fade_out()
            return False
        self.draw()

    def fade_out(self):
        """Плавное исчезновение кольца после завершения"""
        anim = Animation(alpha=0, duration=0.5)
        anim.bind(on_progress=lambda *_: self.draw())
        anim.start(self)

    def stop(self):
        Clock.unschedule(self.update)
        self.parent.remove_widget(self)

class OutlinedLabel(Widget):
    text = StringProperty("")
    font_size = NumericProperty(24)
    color = ListProperty([1, 1, 1, 1])  # Цвет текста
    outline_color = ListProperty([0, 0, 0, 1])  # Цвет обводки
    outline_width = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas,
                  size=self.update_canvas,
                  text=self.update_canvas,
                  font_size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.text:
            return

        core_label = CoreLabel(text=self.text, font_size=self.font_size)
        core_label.refresh()
        texture = core_label.texture
        tex_w, tex_h = texture.size

        x = self.center_x - tex_w / 2
        y = self.center_y - tex_h / 2

        with self.canvas:
            # Обводка — 8 направлений
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                Color(*self.outline_color)
                Rectangle(texture=texture, pos=(x + dx * self.outline_width, y + dy * self.outline_width), size=texture.size)

            # Основной текст
            Color(*self.color)
            Rectangle(texture=texture, pos=(x, y), size=texture.size)

class TestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.difficulty = "medium"
        self.tasks = []
        self.current_index = 0
        self.user_answers = []
        self.correct_answers = []
        self.answers_log = []
        self.adaptive = AdaptiveController()
        self.total_tasks = 0
        self._timer_event = None

    def set_difficulty(self, difficulty):
        """Устанавливает уровень сложности для теста"""
        self.difficulty = difficulty
        self.on_enter()  # Генерация новых задач с учетом выбранной сложности

    def on_enter(self):
        """Вызывается при входе на экран"""
        self.clear_widgets()
        # Если требуется показать 3-2-1 перед стартом, запускаем отсчёт
        if getattr(self, '_do_countdown', False):
            self._do_countdown = False
            self.start_countdown()
            return

        self.reset_test()  # Сбрасываем все данные теста
        self.generate_tasks()  # Генерируем новые задачи
        self.show_current_task()  # Показываем первое задание

    def start_countdown(self, start=3):
        """Показывает 3-2-1 в центре экрана, затем запускает тест."""
        # Простой полноэкранный лейбл для отсчёта
        overlay = MDLabel(
            text=str(start),
            halign='center',
            valign='middle',
            font_style='H2',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            size_hint=(1, 1)
        )
        self.clear_widgets()
        self.add_widget(overlay)

        def tick(dt):
            nonlocal start
            start -= 1
            if start <= 0:
                # очищаем и стартуем тест
                self.clear_widgets()
                Clock.unschedule(event)
                self.reset_test()
                self.generate_tasks()
                self.show_current_task()
                return
            overlay.text = str(start)

        event = Clock.schedule_interval(tick, 1)

    def generate_tasks(self):
        """Генерирует задачи с учетом выбранной сложности"""
        # Генерируем задачи в едином уровне сложности, но с вариациями внутри генераторов
        self.tasks = [
            ('внимание',) + generate_attention_task(),
            ('логика',) + generate_logic_task(),
            ('обработка информации',) + generate_processing_task(),
            ('счет в уме',) + generate_math_task(),
            ('память',) + generate_memory_task()
        ]
        self.total_tasks = len(self.tasks)

    def show_current_task(self):
        layout = MDBoxLayout(orientation='vertical', padding="20dp", spacing="15dp")

        if self.current_index < len(self.tasks):
            category, sequence, question, answer = self.tasks[self.current_index]
            self.correct_answers.append(answer)

            # Поле ввода и кнопка (в верхней части)
            input_layout = MDBoxLayout(orientation='vertical', spacing="10dp", size_hint_y=None, height="120dp")
            input_layout.pos_hint = {"top": 1}

            self.answer_input = MDTextField(
                hint_text="Введите ответ",
                multiline=False,
                opacity=0,
                disabled=True,
                size_hint_y=None,
                height="60dp"
            )

            self.check_btn = MDRaisedButton(
                text="Проверить",
                on_press=self.submit_answer,
                pos_hint={"center_x": 0.5},
                opacity=0,
                disabled=True
            )

            input_layout.add_widget(self.answer_input)
            input_layout.add_widget(self.check_btn)

            layout.add_widget(input_layout)

            # Описание задания
            self.task_label = MDLabel(
                text=sequence,
                halign="center",
                font_style="H6"
            )

            self.countdown_label = MDLabel(
                text="",
                halign="center",
                font_style="H6",
                opacity=0
            )

            self.circular_timer = None
            if category not in ['логика', 'счет в уме']:
                # Подстраиваем время показа последовательности по длине текста
                try:
                    words = len(str(sequence).split())
                    chars = len(str(sequence))
                    # Базовое время: 0.6s на слово, минимум 3, максимум 10
                    total_time = max(3, min(10, 0.6 * words + 1))
                    # Если текст длинный по символам — добавим немного
                    if chars > 80:
                        total_time += 2
                except Exception:
                    total_time = 4

                self.circular_timer = CircularCountdown(total_time=total_time)
                self.circular_timer.size_hint = (None, None)
                self.circular_timer.size = ("200dp", "200dp")
                self.circular_timer.pos_hint = {"center_x": 0.5}

            self.question_label = MDLabel(
                text="",
                halign="center",
                font_style="H6"
            )

            # Progress: label + bar
            progress_layout = MDBoxLayout(orientation='vertical', size_hint_y=None, height='64dp', spacing='6dp')
            self.progress_label = MDLabel(text=f"Задание {self.current_index+1} / {self.total_tasks}", halign='center', font_style='Subtitle1')
            self.progress_bar = MDProgressBar(value=0)
            progress_layout.add_widget(self.progress_label)
            progress_layout.add_widget(self.progress_bar)
            layout.add_widget(progress_layout)

            layout.add_widget(self.task_label)

            if self.circular_timer:
                layout.add_widget(self.circular_timer)
                # Отменим предыдущий event, если он остался
                try:
                    if self._timer_event is not None:
                        Clock.unschedule(self._timer_event)
                except Exception:
                    pass
                self._timer_event = Clock.schedule_interval(self.circular_timer.update, 1 / 60)

            layout.add_widget(self.question_label)
            self.add_widget(layout)

            if category not in ['логика', 'счет в уме']:
                # Используем callback на окончание таймера вместо отдельного schedule_once
                self.circular_timer._on_complete = lambda: self.hide_sequence(category)
            else:
                self.question_label.text = question
                self.answer_input.opacity = 1
                self.answer_input.disabled = False
                self.check_btn.opacity = 1
                self.check_btn.disabled = False

            # Обновляем прогресс внутри ветки активного задания
            try:
                if hasattr(self, 'progress_bar'):
                    pct = (self.current_index / max(1, self.total_tasks)) * 100
                    self.progress_bar.value = pct
                    self.progress_label.text = f"Задание {self.current_index+1} / {self.total_tasks}"
            except Exception:
                pass
        else:
            # Нет активных заданий — показываем финальный экран
            finish_layout = MDBoxLayout(orientation='vertical', padding='20dp', spacing='15dp')
            finish_label = MDLabel(
                text="Тест завершён!",
                halign="center",
                font_style="H5"
            )
            finish_btn = MDRaisedButton(
                text="Посмотреть результаты",
                on_press=self.finish_test,
                pos_hint={"center_x": 0.5}
            )
            finish_layout.add_widget(finish_label)
            finish_layout.add_widget(finish_btn)
            self.add_widget(finish_layout)

    def submit_answer(self, instance):
        user_answer = self.answer_input.text.strip()

        # Получаем текущую задачу
        category, task, question, answer = self.tasks[self.current_index]

        is_correct = False

        # Проверка ответа (расширяем для более интересных форматов)
        if category == 'внимание':
            is_correct = check_attention_answer(user_answer, answer)
        elif category == 'логика':
            is_correct = check_logic_answer(user_answer, answer)
        elif category == 'обработка информации':
            is_correct = check_processing_answer(user_answer, answer)
        elif category == 'счет в уме':
            is_correct = check_math_answer(user_answer, answer)
        elif category == 'память':
            is_correct = check_memory_answer(user_answer, answer)

        result_text = (
            "[b][color=#00FF00]Верно![/color][/b]"
            if is_correct
            else f"[color=#FF0000]Неверно.[/color]\n[color=#1E3A8A]Правильный ответ: {answer}[/color]"
        )


        dialog = MDDialog(
            title="Результат",
            type="custom",
            content_cls=Label(
                text=result_text,
                markup=True,
                font_size="20sp" if is_correct else "16sp",
                halign="center",
            ),
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_press=lambda x: (dialog.dismiss(), self.next_task())
                )
            ]
        )
        dialog.open()

        # Сохраняем результат с категорией и очками, рассчитываем очки по сложности выражения
        def calc_points(task_str, category):
            # Увеличенные баллы за счет в уме:
            # - Цепочки из 3-4 операций или скобки — 15 баллов
            # - Возведение в степень или проценты — 12 баллов
            # - Умножение/деление с двузначными числами — 10 баллов
            # - Простые операции — 5 баллов
            if category == 'счет в уме':
                if task_str.count('(') >= 2 or task_str.count(')') >= 2:
                    return 15  # сложные цепочки
                if '^' in task_str or '%' in task_str:
                    return 12  # степени и проценты
                if any(op in task_str for op in ['*', '/']):
                    return 10  # умножение/деление
                return 8  # сложение/вычитание
            else:
                # Для других категорий
                if any(ch in task_str for ch in ['(', ')']):
                    return 8
                if any(op in task_str for op in ['*', '/']):
                    return 5
                return 3

        points = calc_points(task, category) if is_correct else 0

        self.answers_log.append({
            'category': category,
            'is_correct': is_correct,
            'points': points,
            'task': task
        })
        # обновляем адаптивный контроллер
        try:
            self.adaptive.update(category, is_correct)
        except Exception:
            pass

        self.user_answers.append(user_answer)
        self.current_index += 1
        # если был запущен таймер обновления — отменим его, потому что пользователь ответил досрочно
        try:
            if self._timer_event is not None:
                Clock.unschedule(self._timer_event)
                self._timer_event = None
        except Exception:
            pass

    def hide_sequence(self, category):
        if category not in ['логика', 'счет в уме']:
            self.task_label.text = ""

        # Текущий таск: (category, sequence, question, answer)
        _, task, question, answer = self.tasks[self.current_index]
        self.question_label.text = question

        # Скрываем таймер, если он был
        if hasattr(self, 'circular_timer') and self.circular_timer:
            try:
                # Отменим event обновления
                if self._timer_event is not None:
                    Clock.unschedule(self._timer_event)
                    self._timer_event = None
            except Exception:
                pass
            try:
                self.circular_timer.stop()
            except Exception:
                pass
            self.circular_timer = None

        # Активируем ввод
        self.answer_input.opacity = 1
        self.answer_input.disabled = False
        self.check_btn.opacity = 1
        self.check_btn.disabled = False

    def reset_test(self):
        """Полностью сбрасывает все данные теста"""
        self.current_index = 0  # Сброс индекса текущего задания
        self.tasks = []  # Очистка старых задач
        self.user_answers.clear()  # Очистка ответов пользователя
        self.correct_answers.clear()  # Очистка правильных ответов
        self.answers_log.clear()  # Очистка лога ответов

    def next_task(self):
        """Переход к следующему заданию"""
        self.clear_widgets()
        # Перейдём к следующему заданию; не перегенерируем весь список, чтобы
        # можно было корректно показать прогресс до конца теста.
        if self.current_index < len(self.tasks):
            self.show_current_task()
        else:
            # Показываем финальный экран
            layout = MDBoxLayout(orientation='vertical', padding='20dp', spacing='15dp')
            finish_label = MDLabel(text="Тест завершён!", halign='center', font_style='H5')
            finish_btn = MDRaisedButton(text='Посмотреть результаты', on_press=self.finish_test, pos_hint={'center_x':0.5})
            layout.add_widget(finish_label)
            layout.add_widget(finish_btn)
            self.add_widget(layout)

    def finish_test(self, instance=None):
        """Завершение теста и переход к результатам"""
        iq = calculate_iq(self.answers_log)
        save_scores(self.answers_log, iq)
        self.manager.current = 'result'

    def restart_test(self):
        """Полностью сбрасывает все данные и начинает тест заново"""
        self.reset_test()  # Сбрасываем все данные теста
        self.current_index = 0
        self.tasks = []  # ← Старые задачи очищаются
        self.user_answers.clear()
        self.generate_tasks()  # ← Генерируем новые задачи
        self.show_current_task()
        self.answers_log.clear()  # ← Очистка ЛОГА ответов

