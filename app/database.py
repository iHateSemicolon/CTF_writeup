import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import Config

DB_PATH = Config.DATABASE_PATH

def init_db():
    """앱 시작할 때 딱 한 번 호출해서 테이블 만드는 함수"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        pw TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        idx INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        title TEXT NOT NULL,
        category TEXT,
        content TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    conn.commit()
    conn.close()


def register_user(user_id, user_pw):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_pw = generate_password_hash(user_pw)  # ← 여기서 해싱
    try:
        cursor.execute('INSERT INTO users (id, pw) VALUES (?, ?)', (user_id, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # 아이디 중복
    finally:
        conn.close()


def check_login(user_id, user_pw):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return False
    return check_password_hash(user[1], user_pw)  # user[1] = pw 컬럼(해시값)


def save_note(user_id, title, category, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO notes (user_id, title, category, content)
    VALUES (?, ?, ?, ?)
    ''', (user_id, title, category, content))
    conn.commit()
    conn.close()


def get_my_notes(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_note_by_id(note_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE idx = ?", (note_id,))
    row = cursor.fetchone()
    conn.close()
    return row
