import random

def generate_processing_task(difficulty="medium"):
    """
    Генерирует два близких случайных числа.
    Пользователь должен выбрать большее.
    """
    # Вариативные задачи: выбрать большее, число с большим количеством цифр, число с одинаковой последней цифрой
    variant = random.choice(['which_bigger', 'more_digits', 'same_last_digit'])

    if variant == 'which_bigger':
        base = random.randint(10, 9999)
        deviation = max(1, int(max(1, base * 0.02)))
        a = base
        b = base + random.choice([-1, 1]) * random.randint(1, deviation)
        if random.random() < 0.5:
            a, b = b, a
        correct_answer = str(max(a, b))
        task = f"Какое число больше: {a} или {b}?"
        return task, "Введите ответ", correct_answer

    elif variant == 'more_digits':
        a = random.randint(1, 9999)
        b = random.randint(1, 9999)
        correct_answer = str(a if len(str(a)) > len(str(b)) else b if len(str(b)) > len(str(a)) else 'равно')
        task = f"Какое число содержит больше цифр: {a} или {b}?"
        return task, "Введите ответ (число или 'равно')", correct_answer

    else:
        # Найти число с той же последней цифрой, или выбрать, совпадают ли
        a = random.randint(1, 9999)
        b = random.randint(1, 9999)
        task = f"У {a} и {b} одинаковая последняя цифра? (да/нет)"
        correct_answer = 'да' if str(a)[-1] == str(b)[-1] else 'нет'
        return task, "Введите ответ (да/нет)", correct_answer


def check_processing_answer(user_answer, correct_answer):
    return user_answer.strip() == correct_answer.strip()

# Тестирование
if __name__ == "__main__":
    task, question, answer = generate_processing_task(difficulty="hard")
    print("Задание:", task)
    print("Правильный ответ:", answer)