import random

def generate_task(difficulty=1):
    global correct_answer, question, task
    task_type = random.choice(['arith', 'sqrt'])  # Тип задачи

    if task_type == 'arith':
        a = random.randint(1, 100 * difficulty)
        b = random.randint(1, 100 * difficulty)
        op = random.choice(['+', '-', '*', '/'])

        if op == '/':
            # Деление: делитель должен быть множителем делимого
            b = random.randint(1, 20 * difficulty)
            a = b * random.randint(1, 20 * difficulty)  # Чтобы результат был целым числом
            correct_result = a / b
        else:
            correct_result = eval(f"{a}{op}{b}")

        task = f"{a} {op} {b}"
        question = "Какой результат вычисления?"
        correct_answer = str(int(correct_result) if isinstance(correct_result, float) and correct_result.is_integer() else correct_result)

    elif task_type == 'sqrt':
        number = random.randint(1, 25 * difficulty)
        square = number * number
        task = f"√{square}"
        question = "Чему равен квадратный корень из этого числа?"
        correct_answer = str(number)

    return task, question, correct_answer


def check_math_answer(user_answer, correct_answer):
    return user_answer.strip() == correct_answer.strip()