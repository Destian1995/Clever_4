import random

def generate_task(difficulty=1):
    a = random.randint(1, 10 * difficulty)
    b = random.randint(1, 10 * difficulty)
    op = random.choice(['+', '-', '*'])
    task = f"{a} {op} {b}"
    correct_answer = eval(task)
    return task, correct_answer