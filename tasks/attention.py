import random

def generate_attention_task():
    """
    Показывает последовательность символов, где один случайный символ отсутствует.
    Пользователь должен определить, какого символа не хватает.
    """
    letters = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
    sequence = random.sample(letters, 5)
    missing_index = random.randint(0, 4)
    missing_char = sequence[missing_index]
    sequence[missing_index] = "_"

    task = "Какой символ отсутствует? " + " ".join(sequence)
    return task, missing_char

def check_attention_answer(user_answer, correct_answer):
    return user_answer.strip().upper() == correct_answer.strip().upper()

# Тестирование
if __name__ == "__main__":
    task, answer = generate_attention_task()
    print("Задание:", task)
    print("Правильный ответ:", answer)