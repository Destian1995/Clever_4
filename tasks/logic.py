import random

def generate_logic_task(difficulty="medium"):
    # Варианты логических заданий: правило для последовательности, найти лишнее, заполнить пропуск
    variant = random.choice(['sequence_rule', 'odd_one', 'fill_gap'])

    if variant == 'sequence_rule':
        # простая арифметическая последовательность
        start = random.randint(1, 10)
        step = random.randint(1, 6)
        seq = [start + i * step for i in range(6)]
        question_num = random.randint(4, 6)
        task = ", ".join(f"{i}" for i in seq[:3]) + ", ..."
        correct_answer = str(seq[question_num - 1])
        question_text = f"Какое число стоит на позиции {question_num}?"
        return task, question_text, correct_answer

    elif variant == 'odd_one':
        # найти лишнее число по правилу
        base = random.randint(2, 5)
        seq = [base * i for i in range(1, 6)]
        odd = random.randint(1, 20)
        seq[random.randint(0, 4)] = odd
        task = ", ".join(str(x) for x in seq)
        correct_answer = str(odd)
        question_text = "Какое число лишнее?"
        return task, question_text, correct_answer

    else:
        # fill_gap: показать несколько примеров и просить следующую цифру
        a = random.randint(1, 10)
        b = random.randint(1, 5)
        seq = [a + i * b for i in range(5)]
        task = ", ".join(str(x) for x in seq[:-1]) + ", ?"
        correct_answer = str(seq[-1])
        question_text = "Какое число должно стоять вместо знака ?"
        return task, question_text, correct_answer

def check_logic_answer(user_answer, correct_answer):
    return user_answer.strip() == correct_answer.strip()

# Тестирование
if __name__ == "__main__":
    task, question, answer = generate_logic_task(difficulty="hard")
    print("Задание:", task)
    print(question)
    print("Правильный ответ:", answer)
