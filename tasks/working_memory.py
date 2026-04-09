import random

def generate_memory_task(difficulty="medium"):
    """Вариативное задание на рабочую память: иногда просят символ по позиции,
    иногда просят воспроизвести всю последовательность или её часть.
    Возвращает `sequence, question, correct_answer`.
    """
    # длина последовательности — от 4 до 10
    length = random.randint(4, 10)
    symbols = [random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(length)]
    sequence = " ".join(symbols)

    variant = random.choice(['position', 'full', 'subsequence'])
    if variant == 'position':
        position = random.randint(1, length)
        question = f"Какой символ был на {position} месте?"
        correct_answer = symbols[position - 1]
        return sequence, question, correct_answer

    elif variant == 'full':
        question = "Воспроизведите всю последовательность через пробел." 
        correct_answer = sequence
        return sequence, question, correct_answer

    else:
        # subsequence: попросить последние/первые N элементов
        n = random.randint(2, max(2, length // 2))
        side = random.choice(['first', 'last'])
        if side == 'first':
            seq = " ".join(symbols[:n])
            question = f"Какие первые {n} символов были в последовательности?"
            correct_answer = seq
        else:
            seq = " ".join(symbols[-n:])
            question = f"Какие последние {n} символов были в последовательности?"
            correct_answer = seq
        return sequence, question, correct_answer


def check_memory_answer(user_answer, correct_answer):
    return user_answer.strip().upper() == correct_answer.strip().upper()


# Тестирование
if __name__ == "__main__":
    seq, q, ans = generate_memory_task()
    print("Последовательность:", seq)
    print("Вопрос:", q)
    print("Правильный ответ:", ans)