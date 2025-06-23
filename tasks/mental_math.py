import random

def generate_task(difficulty=1):
    a = random.randint(1, 100 * difficulty)
    b = random.randint(1, 100 * difficulty)
    op = random.choice(['+', '-', '*'])
    task = f"{a} {op} {b}"
    question = "Какой результат вычисления?"
    correct_answer = str(eval(f"{a}{op}{b}"))
    return task, question, correct_answer

def check_math_answer(user_answer, correct_answer):
    return user_answer.strip() == correct_answer.strip()