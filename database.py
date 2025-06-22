import sqlite3
from datetime import datetime, timedelta

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

def save_scores(scores):
    conn = sqlite3.connect('data/user_progress.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE progress SET
            attention_score = ?,
            logic_score = ?,
            processing_score = ?,
            math_score = ?,
            memory_score = ?,
            last_test_date = date("now")
        WHERE id=1
    ''', (
        scores['attention'],
        scores['logic'],
        scores['processing'],
        scores['math'],
        scores['memory']
    ))
    conn.commit()
    conn.close()