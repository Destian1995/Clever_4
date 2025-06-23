def calculate_iq(scores):
    """
    scores — словарь с результатами по категориям (от 0 до 20)
    Пример: {
        'attention': 18,
        'logic': 14,
        'processing': 16,
        'math': 20,
        'memory': 12
    }
    Возвращает общий IQ от 70 до 150
    """
    total_points = sum(scores.values())
    max_points = 20 * 5  # 5 категорий по 20 баллов = 100
    percentage = total_points / max_points
    iq = 70 + percentage * 80  # 70 + (0..1)*80
    return round(iq, 2)

# Тестирование
if __name__ == "__main__":
    test_scores = {
        'attention': 20,
        'logic': 20,
        'processing': 20,
        'math': 20,
        'memory': 20
    }
    print("Общий IQ:", calculate_iq(test_scores))  # должно быть 150