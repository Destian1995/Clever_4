import random

def generate_memory_task():
    """
    Генерирует задание на запоминание последовательности символов.
    Пользователь должен ответить, какой символ был на определённой позиции.
    """
    # Генерируем случайную последовательность (буквы или цифры)
    symbols = [str(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")) for _ in range(5)]

    # Выбираем случайную позицию (от 1 до 5)
    position = random.randint(1, len(symbols))

    # Формируем текст задания
    sequence_text = " ".join(symbols)
    task = f"Запомните последовательность: {sequence_text}\nКакой символ был на {position} месте?"

    # Правильный ответ (индексы начинаются с 0, позиция с 1)
    correct_answer = symbols[position - 1]

    return task, correct_answer

def check_memory_answer(user_answer, correct_answer):
    """
    Проверяет, совпадает ли ответ пользователя с правильным.
    """
    return user_answer.strip().upper() == correct_answer.strip().upper()

# Тестирование
if __name__ == "__main__":
    task, answer = generate_memory_task()
    print("Задание:\n", task)
    print("Правильный ответ:", answer)