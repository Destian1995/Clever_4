import random

def generate_processing_task():
    """
    Генерирует два близких случайных числа.
    Пользователь должен выбрать большее.
    """
    # Базовое число
    base = random.randint(1000, 99999)

    # Небольшое отклонение (±1% от базового числа)
    deviation = max(1, int(base * 0.01))  # минимум 1, чтобы гарантировать разницу

    # Генерируем два близких числа
    a = base
    b = base + random.choice([-1, 1]) * random.randint(1, deviation)

    # Перемешиваем для случайности порядка
    if random.random() < 0.5:
        a, b = b, a

    correct_answer = str(max(a, b))

    task = f"Какое число больше: {a} или {b}?"
    return task, "Введите ответ", correct_answer


def check_processing_answer(user_answer, correct_answer):
    return user_answer.strip() == correct_answer.strip()

# Тестирование
if __name__ == "__main__":
    task, answer = generate_processing_task()
    print("Задание:", task)
    print("Правильный ответ:", answer)