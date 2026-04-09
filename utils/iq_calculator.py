def calculate_iq(answers_log):
    """
    Рассчитывает общий IQ на основе лога ответов.
    Сложные вопросы дают больше очков.
    """
    total_points = 0
    max_points = 0

    # Оценочные максимальные баллы по категории (используются для нормализации)
    max_by_cat = {
        'внимание': 8,
        'память': 10,
        'обработка информации': 9,
        'логика': 14,
        'счет в уме': 14
    }

    for entry in answers_log:
        cat = entry.get('category', 'unknown')
        ok = bool(entry.get('is_correct', False))
        pts = entry.get('points')

        # Если запись содержит уже рассчитанные очки — используем их,
        # иначе — возьмём ориентировочное значение из max_by_cat
        if pts is None:
            pts = max_by_cat.get(cat, 6)

        total_points += pts if ok else 0
        max_points += max_by_cat.get(cat, 6)

    percentage = total_points / max_points if max_points > 0 else 0
    iq = 85 + (percentage * 70)  # От 80 до 150
    return round(iq, 2)