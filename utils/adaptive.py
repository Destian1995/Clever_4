from collections import deque

class AdaptiveController:
    """Простой контроллер адаптивности на основе скользящего окна.

    Хранит последние N результатов по категориям и возвращает уровень сложности
    ('easy', 'medium', 'hard') в зависимости от процента правильных ответов.
    """
    def __init__(self, window_size=8):
        self.window_size = window_size
        self.history = {}  # category -> deque of bools

    def update(self, category, is_correct: bool):
        if category not in self.history:
            self.history[category] = deque(maxlen=self.window_size)
        self.history[category].append(bool(is_correct))

    def success_rate(self, category):
        data = self.history.get(category, [])
        if not data:
            return 0.0
        return sum(1 for v in data if v) / len(data)

    def get_difficulty_for(self, category):
        """Возвращает рекомендованный уровень сложности для категории.

        Логика:
        - success >= 0.8 => поднять сложность
        - success < 0.5 => понизить
        - иначе — оставить средним
        """
        rate = self.success_rate(category)
        if rate >= 0.8:
            return 'hard'
        if rate < 0.5 and len(self.history.get(category, [])) >= 3:
            return 'easy'
        return 'medium'
