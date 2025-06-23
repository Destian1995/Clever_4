def calculate_iq(answers_log):
    """
    Рассчитывает общий IQ на основе лога ответов.
    Сложные вопросы дают больше очков.
    """
    total_points = 0
    max_points = 0

    for entry in answers_log:
        cat = entry['category']
        ok = entry['is_correct']
        diff = entry['difficulty']

        # Баллы за задание в зависимости от категории и сложности
        if cat == 'внимание':
            points = 10
        elif cat == 'память':
            points = 10 if diff == 'hard' else 7 if diff == 'medium' else 5
        elif cat == 'обработка информации':
            points = 9 if diff == 'hard' else 6 if diff == 'medium' else 4
        elif cat == 'логика':
            points = 14 if diff == 'hard' else 10 if diff == 'medium' else 6
        elif cat == 'счет в уме':
            points = 14 if diff == 'hard' else 11 if diff == 'medium' else 7
        else:
            points = 6  # По умолчанию

        entry['points'] = points  # <-- Записываем баллы в лог

        max_points += points

        if ok:
            total_points += points

    percentage = total_points / max_points if max_points > 0 else 0
    iq = 80 + percentage * 70  # От 80 до 150
    return round(iq, 2)