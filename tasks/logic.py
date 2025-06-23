import random

def generate_logic_task():
    base = random.randint(1, 10)
    rule = random.choice([
        lambda x: x * base,
        lambda x: x + base,
        lambda x: x ** base,
        lambda x: x * 2 + base
    ])

    examples = [f"{i} = {rule(i)}" for i in range(1, 4)]
    question_num = random.randint(4, 6)
    task = ", ".join(examples)
    correct_answer = str(rule(question_num))
    question_text = f"Какое число должно быть на месте {question_num}?"

    return task, question_text, correct_answer

def check_logic_answer(user_answer, correct_answer):
    return user_answer.strip() == correct_answer.strip()

# Тестирование
if __name__ == "__main__":
    task, quetsion, answer = generate_logic_task()
    print("Задание:", task)
    print("Правильный ответ:", answer)