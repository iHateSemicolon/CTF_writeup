from flask import Blueprint, render_template, request, redirect, url_for, session
from app import database

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/note')
def note_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.show_login_page'))
    return render_template('note.html')

@notes_bp.route('/save_note', methods=['POST'])
def save_note():
    title = request.form.get('title')
    category = request.form.get('category')
    content = request.form.get('content')

    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.show_login_page')) # 이 부분 새로 추가 기존 방식은 database.save_note(user_id, title, category, content)였음

    database.save_note(user_id, title, category, content)
    return redirect(url_for('notes.show_my_notes'))

@notes_bp.route('/my_notes')
def show_my_notes():
    if 'user_id' not in session:
        return redirect(url_for('auth.show_login_page'))

    current_user = session.get('user_id')
    user_notes = database.get_my_notes(current_user)

    """
    이 사이에 리스트 띄우기 부분이 아예 my_notes.html 로 옮겨졌어요. 기존엔 여기서 f-string으로 HTML 조합해서 바로 리턴 했었음..
    """

    return render_template('my_notes.html', notes=user_notes, user=current_user) # XSS 방지 부분
# 의미 : 이 함수는 쉽게 말해서 "내가 껍데기(HTML)를 준비해 둘 테니까, 파이썬 너는 알맹이(데이터)만 배달해 줘"라는 뜻이에요.

"""
save_note에서 session.get('user_id', 'guest')였던 걸 session.get('user_id') + 명시적 체크로 바꿨어요. 기존 코드는 로그인 안 해도 'guest'로 노트가 저장돼버리는 구멍이 있었거든요.
show_my_notes가 f-string HTML 조합 대신 render_template으로 바뀌었어요 — 이게 Step 4에서 만들 my_notes.html과 연결되는 부분입니다.
"""