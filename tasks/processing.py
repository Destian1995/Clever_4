import random

def generate_processing_task():
    """
    Задание на быстрое сравнение двух чисел.
    Пользователь должен выбрать большее число.
    """
    a = random.randint(10, 999)
    b = random.randint(10, 999)
    correct_answer = str(max(a, b))

    task = f"Какое число больше: {a} или {b}?"
    return task, correct_answer

def check_processing_answer(user_answer, correct_answer):
    return user_answer.strip() == correct_answer.strip()

# Тестирование
if __name__ == "__main__":
    task, answer = generate_processing_task()
    print("Задание:", task)
    print("Правильный ответ:", answer)