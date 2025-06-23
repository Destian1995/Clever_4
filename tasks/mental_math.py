import random

def generate_task(difficulty=1):
    a = random.randint(1, 10 * difficulty)
    b = random.randint(1, 10 * difficulty)
    op = random.choice(['+', '-', '*'])
    return f"{a} {op} {b}", str(eval(f"{a}{op}{b}"))

def check_math_answer(user_answer, correct_answer):
    return user_answer.strip() == correct_answer.strip()