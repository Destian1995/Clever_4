import random
import math


def _format_answer(value):
    # Форматируем: если целое — без десятичных, иначе — с 2 знаками
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def generate_task(difficulty="medium"):
    """Генерирует арифметическое или sqrt задание с повышенной сложностью.

    Для hard уровня добавляем:
    - Цепочки из 3-4 операций
    - Возведение в квадрат/куб
    - Проценты от чисел
    - Комбинированные выражения со скобками
    """
    task_type = random.choice(['arith', 'sqrt', 'power', 'percent'])

    if task_type == 'arith':
        # easy: простые операции с однозначными и двузначными числами
        if difficulty == 'easy':
            a = random.randint(5, 50)
            b = random.randint(2, 30)
            op = random.choice(['+', '-', '*', '/'])

            if op == '/':
                # выбираем желаемый результат: целое или с .5
                if random.random() < 0.3:
                    # половинчатый результат
                    r = random.randint(1, 15) + 0.5
                    # b должен быть чётным чтобы a = r*b было целым
                    b = random.choice([i for i in range(2, 31) if i % 2 == 0])
                    a = int(r * b)
                else:
                    r = random.randint(1, 15)
                    b = random.randint(1, 15)
                    a = r * b

                correct_result = a / b
            else:
                correct_result = eval(f"{a}{op}{b}")

            task = f"{a} {op} {b}"

        # medium: выражение из 2-3 операций с увеличенными диапазонами
        elif difficulty == 'medium':
            attempts = 0
            while attempts < 500:
                attempts += 1
                num_ops = random.choice([2, 3])
                
                if num_ops == 2:
                    ops = random.choices(['+', '-', '*', '/'], k=2)
                    # Вариации: если внутри скобок '*' или '/', делаем однозначные числа внутри;
                    # если внутри '+' или '-', делаем внутри 3- и 2-значные числа.
                    if ops[0] in ['*', '/']:
                        a = random.randint(3, 15)
                        b = random.randint(3, 15)
                    else:
                        a = random.randint(100, 999)
                        b = random.randint(10, 99)

                    # Правила для третьего числа в зависимости от внешней операции
                    if ops[1] in ['*', '/']:
                        c = random.randint(10, 50)
                    else:
                        c = random.randint(1, 150)

                    expr = f"({a}{ops[0]}{b}){ops[1]}{c}"
                else:
                    # 3 операции: (a op1 b) op2 c op3 d
                    ops = random.choices(['+', '-', '*', '/'], k=3)
                    a = random.randint(5, 30)
                    b = random.randint(5, 30)
                    c = random.randint(3, 20)
                    d = random.randint(2, 15)
                    
                    # Избегаем деления на ноль и слишком сложных дробей
                    if ops[0] in ['*', '/'] and ops[1] in ['*', '/']:
                        continue
                    
                    expr = f"(({a}{ops[0]}{b}){ops[1]}{c}){ops[2]}{d}"
                
                try:
                    val = eval(expr)
                except Exception:
                    continue

                # допустимы только значения с шагом 0.5 и в разумных пределах
                if abs(val * 2 - round(val * 2)) < 1e-9 and -10000 < val < 10000:
                    correct_result = val
                    task = expr
                    break
            else:
                # fallback — простое выражение с допустимым результатом
                a = random.randint(20, 99)
                b = random.randint(10, 50)
                task = f"{a}*{b}"
                correct_result = a * b

        # hard: сложные выражения с 3-4 операциями, степени, комбинированные
        else:
            for _ in range(600):
                variant = random.choice(['prod_div', 'sum_div', 'mul2', 'chain3', 'chain4', 'mixed'])
                
                if variant == 'prod_div':
                    a = random.randint(15, 99)
                    b = random.randint(10, 50)
                    c = random.randint(5, 25)
                    prod = a * b
                    if prod % c == 0 or (prod * 2) % c == 0:
                        expr = f"({a}*{b})/{c}"
                        correct_result = prod / c
                        task = expr
                        break
                elif variant == 'sum_div':
                    a = random.randint(200, 999)
                    b = random.randint(50, 200)
                    c = random.randint(3, 15)
                    s = a + b
                    if s % c == 0 or (s * 2) % c == 0:
                        expr = f"({a}+{b})/{c}"
                        correct_result = s / c
                        task = expr
                        break
                elif variant == 'chain3':
                    # Цепочка: ((a * b) + c) / d
                    a = random.randint(8, 25)
                    b = random.randint(8, 25)
                    c = random.randint(20, 100)
                    d = random.randint(3, 12)
                    val = ((a * b) + c) / d
                    if abs(val * 2 - round(val * 2)) < 1e-9:
                        expr = f"(({a}*{b})+{c})/{d}"
                        correct_result = val
                        task = expr
                        break
                elif variant == 'chain4':
                    # Цепочка из 4 операций: (((a * b) + c) / d) + e
                    a = random.randint(5, 20)
                    b = random.randint(5, 20)
                    c = random.randint(10, 80)
                    d = random.randint(2, 10)
                    e = random.randint(5, 30)
                    val = (((a * b) + c) / d) + e
                    if abs(val * 2 - round(val * 2)) < 1e-9 and val < 5000:
                        expr = f"((({a}*{b})+{c})/{d})+{e}"
                        correct_result = val
                        task = expr
                        break
                elif variant == 'mixed':
                    # Смешанное: (a + b) * c - d
                    a = random.randint(50, 200)
                    b = random.randint(30, 100)
                    c = random.randint(3, 8)
                    d = random.randint(20, 150)
                    val = (a + b) * c - d
                    expr = f"({a}+{b})*{c}-{d}"
                    correct_result = val
                    task = expr
                    break
                else:
                    a = random.randint(20, 99)
                    b = random.randint(15, 60)
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
            number = random.randint(12, 45)
        elif difficulty == "hard":
            number = random.randint(35, 150)

        square = number * number
        task = f"√{square}"
        question = "Чему равен квадратный корень из этого числа?"
        correct_answer = str(number)
    
    elif task_type == 'power':
        # Возведение в степень
        if difficulty == "easy":
            base = random.randint(2, 8)
            exp = 2
        elif difficulty == "medium":
            base = random.randint(5, 15)
            exp = random.choice([2, 3])
        else:  # hard
            base = random.randint(10, 25)
            exp = random.choice([2, 3])
        
        result = base ** exp
        task = f"{base}^{exp}"
        question = "Чему равно это число в степени?"
        correct_answer = str(result)
    
    elif task_type == 'percent':
        # Вычисление процентов - только целые или .5 результаты
        if difficulty == "easy":
            percent = random.choice([10, 20, 25, 30, 40, 50])
            # Число должно делиться на 100/gcd(percent, 100)
            divisor = 100 // math.gcd(int(percent), 100)
            multiplier = random.randint(2, 20)
            number = divisor * multiplier
        elif difficulty == "medium":
            percent = random.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 75, 80])
            divisor = 100 // math.gcd(int(percent), 100)
            multiplier = random.randint(2, 30)
            number = divisor * multiplier
        else:  # hard
            percent = random.choice([5, 10, 12, 15, 20, 24, 25, 30, 35, 40, 45, 48, 50, 60, 70, 75, 80, 90])
            divisor = 100 // math.gcd(int(percent), 100)
            multiplier = random.randint(3, 40)
            number = divisor * multiplier
        
        result = int((percent / 100) * number)
        
        task = f"{percent}% от {number}"
        question = "Сколько это будет?"
        correct_answer = str(result)

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
    print("=== ТЕСТ ГЕНЕРАЦИИ ЗАДАЧ ===\n")
    for d in ['easy', 'medium', 'hard']:
        print(f"--- {d.upper()} ---")
        for i in range(10):
            task, question, answer = generate_task(difficulty=d)
            print(f"{i+1}. {task:35s} => {answer}")
        print()