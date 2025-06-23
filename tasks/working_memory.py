import random

def generate_memory_task():
    """
    Возвращает:
    - sequence: строка с последовательностью символов
    - question: текст вопроса
    - correct_answer: правильный ответ
    """
    symbols = [str(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")) for _ in range(5)]
    position = random.randint(1, len(symbols))

    sequence = " ".join(symbols)
    question = f"Какой символ был на {position} месте?"

    # Получаем правильный ответ из списка (не строки, потому что split() не нужен)
    correct_answer = symbols[position - 1]  # ← вот здесь была ошибка

    return sequence, question, correct_answer


def check_memory_answer(user_answer, correct_answer):
    return user_answer.strip().upper() == correct_answer.strip().upper()


# Тестирование
if __name__ == "__main__":
    seq, q, ans = generate_memory_task()
    print("Последовательность:", seq)
    print("Вопрос:", q)
    print("Правильный ответ:", ans)