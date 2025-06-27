import random

def generate_processing_task(difficulty="medium"):
    """
    Генерирует два близких случайных числа.
    Пользователь должен выбрать большее.
    """
    if difficulty == "easy":
        base = random.randint(100, 999)  # Меньший диапазон
        deviation = max(1, int(base * 0.01))  # Минимальное отклонение
    elif difficulty == "medium":
        base = random.randint(1000, 99999)  # Средний диапазон
        deviation = max(1, int(base * 0.05))  # Увеличенное отклонение
    elif difficulty == "hard":
        base = random.randint(100000, 9999999)  # Большой диапазон
        deviation = max(1, int(base * 0.1))  # Значительное отклонение

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
    task, question, answer = generate_processing_task(difficulty="hard")
    print("Задание:", task)
    print("Правильный ответ:", answer)