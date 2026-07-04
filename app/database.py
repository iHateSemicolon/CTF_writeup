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


"""
init_db(): 기존엔 import database만 해도 테이블 생성이 실행됐어요. 이제는 create_app()에서 명시적으로 database.init_db()를 호출할 때만 실행됩니다. 이렇게 하면 나중에 "이 모듈 언제 뭘 실행하는지" 추적이 쉬워져요.
register_user: generate_password_hash(user_pw)가 비밀번호를 단방향 해시로 바꿔줍니다. 원본 비밀번호는 어디에도 저장 안 되고, DB엔 해시값만 들어가요.
check_login: 기존엔 WHERE id=? AND pw=?로 평문 비교했는데, 이제 pw는 해시값이라 평문 비교가 불가능해요. 그래서 먼저 id로만 유저를 찾고, check_password_hash(저장된_해시, 입력한_평문)로 검증합니다. 이 함수가 내부적으로 같은 방식으로 해싱해서 비교해줘요.
"""

