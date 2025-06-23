import random

# База знаний: категории и их элементы
categories = {
    "природа": ["дерево", "цветок", "трава", "лист", "корень"],
    "животные": ["собака", "кошка", "птица", "лошадь", "корова"],
    "фрукты": ["яблоко", "банан", "апельсин", "груша", "киви"],
    "транспорт": ["автомобиль", "велосипед", "поезд", "самолет", "катер"],
    "одежда": ["рубашка", "брюки", "футболка", "кроссовки", "шляпа"],
    "мебель": ["стул", "стол", "кровать", "шкаф", "тумбочка"],
    "электроника": ["телефон", "планшет", "телевизор", "наушники", "компьютер"]
}

def generate_attention_task():
    """
    Генерирует задание "Найди лишнее":
    4 слова из одной категории + 1 из другой.
    """

    # Выбираем основную категорию
    main_category = random.choice(list(categories.keys()))
    main_words = random.sample(categories[main_category], 4)

    # Выбираем "лишнее" слово из другой категории
    other_categories = [cat for cat in categories if cat != main_category]
    other_category = random.choice(other_categories)
    extra_word = random.choice(categories[other_category])

    # Формируем полный список и перемешиваем
    full_list = main_words + [extra_word]
    random.shuffle(full_list)

    task = "Какое слово лишнее? " + ", ".join(full_list)
    return task, "Какое слово лишнее? ", extra_word

def check_attention_answer(user_answer, correct_answer):
    return user_answer.strip().lower() == correct_answer.strip().lower()

# Тестирование
if __name__ == "__main__":
    task, question, answer = generate_attention_task()
    print("Задание:", task)
    print("Правильный ответ:", answer)