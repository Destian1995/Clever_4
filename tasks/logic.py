import random

def generate_logic_task():
    """
    Простая логическая головоломка на основе аналогий:
    Например: "Если 1 = 3, 2 = 6, 3 = 9, то 4 = ?"
    """
    base = random.randint(1, 10)
    rule = random.choice([
        lambda x: x * base,
        lambda x: x + base,
        lambda x: x ** base,
        lambda x: x * 2 + base
    ])

    examples = [f"{i} = {rule(i)}" for i in range(1, 4)]
    question_num = random.randint(4, 6)
    task = "Продолжите последовательность: " + ", ".join(examples) + f", то {question_num} = ?"
    correct_answer = str(rule(question_num))
    return task, correct_answer

def check_logic_answer(user_answer, correct_answer):
    return user_answer.strip() == correct_answer.strip()

# Тестирование
if __name__ == "__main__":
    task, answer = generate_logic_task()
    print("Задание:", task)
    print("Правильный ответ:", answer)