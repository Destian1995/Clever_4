import random


def _format_answer(value):
    # Форматируем: если целое — без десятичных, иначе — с 2 знаками
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def generate_task(difficulty="medium"):
    """Генерирует арифметическое или sqrt задание.

    Для операций умножения/деления избегаем трёхзначных множителей: вместо
    100*100 генерируем комбинированное выражение с двумя-значными числами,
    например `(10*23)/12`.
    """
    task_type = random.choice(['arith', 'sqrt'])

    if task_type == 'arith':
        # easy: простые операции
        if difficulty == 'easy':
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            op = random.choice(['+', '-', '*', '/'])

            if op == '/':
                # выбираем желаемый результат: целое или с .5
                if random.random() < 0.3:
                    # половинчатый результат
                    r = random.randint(1, 10) + 0.5
                    # b должен быть чётным чтобы a = r*b было целым
                    b = random.choice([i for i in range(2, 21) if i % 2 == 0])
                    a = int(r * b)
                else:
                    r = random.randint(1, 10)
                    b = random.randint(1, 10)
                    a = r * b

                correct_result = a / b
            else:
                correct_result = eval(f"{a}{op}{b}")

            task = f"{a} {op} {b}"

        # medium: выражение из двух операций — особые правила по размерам чисел
        elif difficulty == 'medium':
            attempts = 0
            while attempts < 400:
                attempts += 1
                ops = random.choices(['+', '-', '*', '/'], k=2)
                # Вариации: если внутри скобок '*' или '/', делаем однозначные числа внутри;
                # если внутри '+' или '-', делаем внутри 3- и 2-значные числа.
                if ops[0] in ['*', '/']:
                    a = random.randint(2, 9)
                    b = random.randint(2, 9)
                else:
                    a = random.randint(100, 999)
                    b = random.randint(10, 99)

                # Правила для третьего числа в зависимости от внешней операции
                if ops[1] in ['*', '/']:
                    c = random.randint(10, 99)
                else:
                    c = random.randint(1, 99)

                expr = f"({a}{ops[0]}{b}){ops[1]}{c}"
                try:
                    val = eval(expr)
                except Exception:
                    continue

                # допустимы только значения с шагом 0.5
                if abs(val * 2 - round(val * 2)) < 1e-9:
                    correct_result = val
                    task = expr
                    break
            else:
                # fallback — простое выражение с допустимым результатом (двузначные умножения)
                a = random.randint(10, 99)
                b = random.randint(10, 99)
                task = f"{a}*{b}"
                correct_result = a * b

        # hard: выражения с произведением / делением, допускаем .5
        else:
            for _ in range(500):
                # hard: пробуем разные вариации. В одной из них — (a*b)/c с двузначными a,b,c;
                # в другой — (a+b)/c где a,b — трех- и двузначные,
                # и в третьей — простое умножение двузначных.
                variant = random.choice(['prod_div', 'sum_div', 'mul2'])
                if variant == 'prod_div':
                    a = random.randint(10, 99)
                    b = random.randint(10, 99)
                    c = random.randint(10, 99)
                    prod = a * b
                    if prod % c == 0 or (prod * 2) % c == 0:
                        expr = f"({a}*{b})/{c}"
                        correct_result = prod / c
                        task = expr
                        break
                elif variant == 'sum_div':
                    a = random.randint(100, 999)
                    b = random.randint(10, 99)
                    c = random.randint(2, 12)
                    s = a + b
                    if s % c == 0 or (s * 2) % c == 0:
                        expr = f"({a}+{b})/{c}"
                        correct_result = s / c
                        task = expr
                        break
                else:
                    a = random.randint(10, 99)
                    b = random.randint(10, 99)
                    expr = f"{a}*{b}"
                    correct_result = a * b
                    task = expr
                    break

        question = "Какой результат вычисления?"
        correct_answer = _format_answer(correct_result)

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
    """Проверяет ответ, пытаясь сравнить численно с допуском.

    Поддерживает целые и десятичные ответы; допускаем небольшую погрешность.
    """
    ua = user_answer.strip()
    ca = correct_answer.strip()
    try:
        # Попробуем сравнить как числа
        u = float(ua.replace(',', '.'))
        c = float(ca.replace(',', '.'))
        return abs(u - c) < 1e-2
    except Exception:
        # Фоллбек на строковое сравнение
        return ua == ca


# Тестирование
if __name__ == "__main__":
    for d in ['easy', 'medium', 'hard']:
        task, question, answer = generate_task(difficulty=d)
        print(d, '->', task, question, '=>', answer)