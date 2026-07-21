from flask import Blueprint, render_template, request, redirect, url_for, session
from app import database

from flask import Response
from app.utils.md import note_to_markdown

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/note') # 노트 페이지
def note_page(): # 노트페이지 함수
    if 'user_id' not in session: #만약 유저아이디가 세션에 없다면
        return redirect(url_for('auth.show_login_page')) # 인증 미들웨어 부분, 만약 유저 아이디 없을시 로그인 페이지로 안내
    return render_template('note.html')  #note.html 파일 렌더링

@notes_bp.route('/save_note', methods=['POST']) # 노트 저장을 눌렀을때 실행 되는 라우트
def save_note(): # 노트 저장 함수
    title = request.form.get('title') # html 파일 내에 form 태그에서 타이틀,
    category = request.form.get('category')# 카테고리,
    content = request.form.get('content') # 내용 가져오기

    user_id = session.get('user_id') # 세션에서 유저 아이디 가져오기 
    if not user_id: # 만약 세션에 유저 아이디가 없으면
        return redirect(url_for('auth.show_login_page'))  # 인증 미들웨어 2, 로그인 페이지로 안내

    database.save_note(user_id, title, category, content) # 데이터베이스에 저장
    return redirect(url_for('notes.show_my_notes'))# 저장 후 내 노트 페이지로 이동

@notes_bp.route('/my_notes') # 내 노트 페이지
def show_my_notes(): # 내 노트 페이지 함수
    if 'user_id' not in session: # 만약 세션에 유저 아이디가 없다면
        return redirect(url_for('auth.show_login_page')) # 인증 미들웨어 3, 로그인 페이지로 안내

    current_user = session.get('user_id') # 현재 유저
    user_notes = database.get_my_notes(current_user) # 그 현재 유저의 노트



    return render_template('my_notes.html', notes=user_notes, user=current_user) # XSS 방지 부분 # # 내 노트 리스트에 위에서 선언 해뒀던 현재 유저와 현재 유저의 노트 같이 렌더링

@notes_bp.route('/note/<int:note_id>/export')
def export_note(note_id):
    note = database.get_note_by_id(note_id)
    md_content = note_to_markdown(note)
    return Response(
        md_content,
        mimetype='text/markdown',
        headers={'Content-Disposition': f'attachment; filename=note_{note_id}.md'}
    )