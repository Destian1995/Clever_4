import random

# База знаний: категории и их элементы
categories = {
    "природа": ["дерево", "цветок", "трава", "лист", "корень", "камень", "река", "гора", "облако", "дождь"],
    "животные": ["собака", "кошка", "птица", "лошадь", "корова", "лев", "слон", "жираф", "крокодил", "дельфин"],
    "фрукты": ["яблоко", "банан", "апельсин", "груша", "киви", "виноград", "мандарин", "ананас", "персик", "слива"],
    "овощи": ["морковь", "картофель", "лук", "чеснок", "помидор", "огурец", "капуста", "брокколи", "редис", "свёкла"],
    "транспорт": ["автомобиль", "велосипед", "поезд", "самолет", "катер", "метро", "мотоцикл", "грузовик", "вертолёт", "пароход"],
    "одежда": ["рубашка", "брюки", "футболка", "кроссовки", "шляпа", "куртка", "джинсы", "шорты", "туфли", "шарф"],
    "мебель": ["стул", "стол", "кровать", "шкаф", "тумбочка", "диван", "полка", "комод", "зеркало", "кровать"],
    "электроника": ["телефон", "планшет", "телевизор", "наушники", "компьютер", "принтер", "часы", "камера", "проектор", "плеер"],
    "продукты": ["хлеб", "молоко", "сыр", "яйца", "масло", "мука", "сахар", "соль", "мясо", "рыба"],
    "профессии": ["учитель", "врач", "инженер", "водитель", "программист", "повар", "строитель", "менеджер", "полицейский", "летчик"],
    "спорт": ["футбол", "баскетбол", "плование", "бег", "велосипед", "гимнастика", "бокс", "волейбол", "теннис", "лыжи"],
    "цвета": ["красный", "синий", "зеленый", "желтый", "фиолетовый", "оранжевый", "розовый", "черный", "белый", "коричневый"],
    "геометрия": ["круг", "квадрат", "треугольник", "прямоугольник", "ромб", "трапеция", "овал", "куб", "цилиндр", "пирамида"]
}
def generate_attention_task(difficulty="medium"):
    """
    Генерирует задание "Найди лишнее":
    4 слова из одной категории + 1 из другой.
    """

    # Выбираем основную категорию
    main_category = random.choice(list(categories.keys()))
    # Вариации задания: 'odd_one', 'count', 'common'
    variant = random.choice(['odd_one', 'count', 'common'])

    if variant == 'odd_one':
        # классическое: 3-5 слов одной категории + 1 лишнее
        main_count = random.choice([3, 4, 5])
        main_words = random.sample(categories[main_category], main_count)
        other_categories = [cat for cat in categories if cat != main_category]
        other_category = random.choice(other_categories)
        extra_word = random.choice(categories[other_category])
        full_list = main_words + [extra_word]
        random.shuffle(full_list)
        task = "Какое слово лишнее? " + ", ".join(full_list)
        return task, "Введите ответ", extra_word

    elif variant == 'count':
        # Считать слова, принадлежащие выбранной категории в списке
        pool = []
        for _ in range(8):
            if random.random() < 0.6:
                pool.append(random.choice(categories[main_category]))
            else:
                other = random.choice([c for c in categories if c != main_category])
                pool.append(random.choice(categories[other]))
        task = "Сколько слов из категории '%s' в списке: %s" % (main_category, ", ".join(pool))
        correct = str(sum(1 for w in pool if w in categories[main_category]))
        return task, "Введите число", correct

    else:
        # common: найти общее слово для нескольких небольших списков
        picks = random.sample(list(categories.keys()), k=3)
        lists = [random.sample(categories[p], 3) for p in picks]
        # добавим одно общее слово из первой категории
        common = random.choice(categories[picks[0]])
        lists[1][0] = common
        lists[2][0] = common
        task = "Какое слово встречается чаще остальных:\n" + " | ".join([", ".join(l) for l in lists])
        return task, "Введите слово", common

    # Выбираем "лишнее" слово из другой категории
    other_categories = [cat for cat in categories if cat != main_category]
    other_category = random.choice(other_categories)
    extra_word = random.choice(categories[other_category])

    # Формируем полный список и перемешиваем
    full_list = main_words + [extra_word]
    random.shuffle(full_list)

    task = "Какое слово лишнее? " + ", ".join(full_list)
    return task, "Введите ответ", extra_word

def check_attention_answer(user_answer, correct_answer):
    return user_answer.strip().lower() == correct_answer.strip().lower()

# Тестирование
if __name__ == "__main__":
    task, question, answer = generate_attention_task()
    print("Задание:", task)
    print("Правильный ответ:", answer)