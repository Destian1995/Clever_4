
def calculate_iq(answers_log):
    """
    Рассчитывает общий IQ на основе лога ответов.
    Сложные вопросы дают больше очков.
    """
    total_points = 0

    for entry in answers_log:
        cat = entry['category']
        ok = entry['is_correct']
        diff = entry['difficulty']

        if not ok:
            continue

        if cat == 'внимание':
            total_points += 12
        elif cat == 'память':
            total_points += 15
        elif cat == 'обработка информации':
            total_points += 10
        elif cat == 'логика':
            if diff == 'hard':
                total_points += 27
            elif diff == 'medium':
                total_points += 18
            else:
                total_points += 10
        elif cat == 'счет в уме':
            if diff == 'hard':
                total_points += 25
            elif diff == 'medium':
                total_points += 12
            else:
                total_points += 6

    max_points = 135  # 5 вопросов × максимум по категории
    percentage = total_points / max_points
    iq = 80 + percentage * 80  # Диапазон от 80 до 150
    return round(iq, 2)
