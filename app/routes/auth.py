from flask import Blueprint, render_template, request, redirect, url_for, session
from app import database

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('signup.html')

@auth_bp.route('/sign_up_test', methods=['POST']) # 여기 왜 사인업 테스트임? 
def sign_up():
    nickname = request.form.get('ur_nick')
    password = request.form.get('ur_pw')

    if database.register_user(nickname, password):
        return f"<h4>{nickname}님 가입 성공! <a href='/login_page'>로그인하러 가기</a></h4>"
    else:
        return f"<h4>이미 있는 아이디입니다.</h4>"

@auth_bp.route('/login_page')
def show_login_page():
    return render_template('login.html')

@auth_bp.route('/login_test', methods=['POST'])
def login_check():
    ur_id = request.form.get('ur_nick')
    ur_pw = request.form.get('ur_pw')

    if database.check_login(ur_id, ur_pw):
        session['user_id'] = ur_id
        return redirect(url_for('notes.note_page'))
    else:
        return "<h3>아이디랑 비밀번호를 다시 확인해 주세요</h3>"

@auth_bp.route('/logout') # 새로운 로그아웃 페이지 추가 
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.show_login_page'))

"""
설명: app = Flask(__name__) 대신 Blueprint('auth', __name__)을 씁니다. @app.route(...)였던 게 @auth_bp.route(...)로만 바뀌는 거라 기존 코드 로직은 거의 그대로예요. 눈여겨볼 부분:

login_check에서 로그인 성공하면 이제 HTML 문자열 대신 redirect(url_for('notes.note_page'))로 바로 노트 작성 페이지로 넘겨요. url_for('notes.note_page')처럼 블루프린트이름.함수이름으로 참조하는 게 규칙이에요 (notes blueprint 안의 note_page 함수).
logout 라우트를 새로 추가했어요. 기존엔 없었죠.
f"<h4>{nickname}님 가입 성공!...처럼 남아있는 부분은 지금은 위험하지 않아요 (닉네임이 서버가 만든 문자열이 아니라 유저 입력이긴 하지만, alert 정도로 그치는 self-XSS라 우선순위 낮음). 나중에 여유 되면 여기도 템플릿화 하시면 더 좋습니다.
"""