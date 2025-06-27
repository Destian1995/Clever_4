import random

def generate_task(difficulty="medium"):
    global correct_answer, question, task
    task_type = random.choice(['arith', 'sqrt'])  # Тип задачи

    if task_type == 'arith':
        if difficulty == "easy":
            a = random.randint(1, 50)
            b = random.randint(1, 50)
            op = random.choice(['+', '-', '*', '/'])
        elif difficulty == "medium":
            a = random.randint(10, 500)
            b = random.randint(10, 500)
            op = random.choice(['+', '-', '*', '/'])
        elif difficulty == "hard":
            a = random.randint(234, 1400)
            b = random.randint(156, 1300)
            op = random.choice(['*', '/'])

        if op == '/':
            # Деление: делитель должен быть множителем делимого
            b = random.randint(1, 20)
            a = b * random.randint(1, 20)  # Чтобы результат был целым числом
            correct_result = a / b
        else:
            correct_result = eval(f"{a}{op}{b}")

        task = f"{a} {op} {b}"
        question = "Какой результат вычисления?"
        correct_answer = str(int(correct_result) if isinstance(correct_result, float) and correct_result.is_integer() else correct_result)

    elif task_type == 'sqrt':
        if difficulty == "easy":
            number = random.randint(1, 15)
        elif difficulty == "medium":
            number = random.randint(15, 55)
        elif difficulty == "hard":
            number = random.randint(55, 185)

        square = number * number
        task = f"√{square}"
        question = "Чему равен квадратный корень из этого числа?"
        correct_answer = str(number)

    return task, question, correct_answer


def check_math_answer(user_answer, correct_answer):
    return user_answer.strip() == correct_answer.strip()

# Тестирование
if __name__ == "__main__":
    task, question, answer = generate_task(difficulty="hard")
    print("Задание:", task)
    print("Правильный ответ:", answer)