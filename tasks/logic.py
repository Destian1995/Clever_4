import random

def generate_logic_task(difficulty="medium"):
    if difficulty == "easy":
        base = random.randint(1, 30)
        rule = random.choice([
            lambda x: x + base,
            lambda x: x * base
        ])
        question_range = (4, 7)

    elif difficulty == "medium":
        base = random.randint(2, 4)
        rule = random.choice([
            lambda x: x ** base if x <= 5 else x * base,
            lambda x: x * 2 + base
        ])
        question_range = (4, 7)

    elif difficulty == "hard":
        base = random.randint(3000, 6000)
        rule = random.choice([
            lambda x: (x + base) * 3,
            lambda x: x * base,
            lambda x: x * 2 + base
        ])
        question_range = (4, 6)

    examples = [f"{i} = {rule(i)}" for i in range(1, 4)]
    question_num = random.randint(*question_range)
    task = ", ".join(examples)
    correct_answer = str(rule(question_num))
    question_text = f"Какое число должно быть на месте {question_num}?"

    return task, question_text, correct_answer

def check_logic_answer(user_answer, correct_answer):
    return user_answer.strip() == correct_answer.strip()

# Тестирование
if __name__ == "__main__":
    task, question, answer = generate_logic_task(difficulty="hard")
    print("Задание:", task)
    print(question)
    print("Правильный ответ:", answer)
