import sqlite3
from datetime import datetime, timedelta


def save_scores(answers_log, iq):
    conn = sqlite3.connect('data/user_progress.db')
    cursor = conn.cursor()

    # Инициализируем счётчики
    scores = {
        'внимание': 0,
        'логика': 0,
        'обработка информации': 0,
        'счет в уме': 0,
        'память': 0
    }

    # Суммируем баллы по категориям
    for entry in answers_log:
        cat = entry['category']
        ok = entry['is_correct']

        if not ok:
            continue

        if cat in scores:
            points = entry.get('points', 0)  # Берём баллы из лога
            scores[cat] += points

    # Обновляем БД
    cursor.execute('''
        UPDATE progress SET
            attention_score = ?,
            logic_score = ?,
            processing_score = ?,
            math_score = ?,
            memory_score = ?,
            iq_score = ?,
            last_test_date = date("now")
        WHERE id=1
    ''', (
        scores['внимание'],
        scores['логика'],
        scores['обработка информации'],
        scores['счет в уме'],
        scores['память'],
        iq
    ))

    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect('data/user_progress.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY,
            last_test_date TEXT,
            attention_score REAL DEFAULT 0,
            logic_score REAL DEFAULT 0,
            processing_score REAL DEFAULT 0,
            math_score REAL DEFAULT 0,
            memory_score REAL DEFAULT 0
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO progress (id, last_test_date) VALUES (1, date("now"))')
    conn.commit()
    conn.close()

def get_last_test_date():
    conn = sqlite3.connect('data/user_progress.db')
    cursor = conn.cursor()
    cursor.execute('SELECT last_test_date FROM progress WHERE id=1')
    date_str = cursor.fetchone()[0]
    conn.close()
    return datetime.strptime(date_str, '%Y-%m-%d')

def update_last_test_date():
    conn = sqlite3.connect('data/user_progress.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE progress SET last_test_date = date("now") WHERE id=1')
    conn.commit()
    conn.close()

def reset_all_scores():
    conn = sqlite3.connect('data/user_progress.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE progress SET 
            attention_score = 0,
            logic_score = 0,
            processing_score = 0,
            math_score = 0,
            memory_score = 0,
            last_test_date = date("now")
        WHERE id=1
    ''')
    conn.commit()
    conn.close()

def check_and_reset_weekly():
    last_date = get_last_test_date()
    if datetime.now() - last_date > timedelta(days=7):
        reset_all_scores()

def get_progress():
    conn = sqlite3.connect('data/user_progress.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM progress WHERE id=1')
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            'id': row[0],
            'last_test_date': row[1],
            'attention_score': row[2],
            'logic_score': row[3],
            'processing_score': row[4],
            'math_score': row[5],
            'memory_score': row[6],
            'iq_score': row[7]
        }
    return None