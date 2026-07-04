from flask import Blueprint, render_template, request, redirect, url_for, session
from app import database

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/') # 첫화면 렌더링
def home(): # 홈 함수
    return render_template('signup.html') # 가장 첫 화면은 로그인 화면

@auth_bp.route('/sign_up_test', methods=['POST']) #로그인 화면에서 회원가입 버튼 눌렀을 때 처리하는 라우트 (테스트)
def sign_up(): # 회원가입 처리 함수
    nickname = request.form.get('ur_nick') # 그 html 파일내에 폼 태그에서 가져오기
    password = request.form.get('ur_pw') # 얘도 같은 방식

    if database.register_user(nickname, password): # 데이터 베이스 안에 등록된 유저(닉네임, 비밀번호)가 없으면 true(회원 가입 성공문) 있으면 (false) 라면 이미 있는 아이디라고 반환
        return f"<h4>{nickname}님 가입 성공! <a href='/login_page'>로그인하러 가기</a></h4>"  # !self-XSS 나중에 템플릿화 하기! true 일때
    else:
        return f"<h4>이미 있는 아이디입니다.</h4>" # false 일때

@auth_bp.route('/login_page') # 로그인 페이지 렌더링
def show_login_page(): # 로그인 페이지 함수 (네이밍 고치기 - 좀 통일 좀 해라)
    return render_template('login.html') # 그 login.html 파일 렌더링 해서 보여주기

@auth_bp.route('/login_test', methods=['POST']) # 로그인 테스팅 하기 라우트!!
def login_check(): # 로그인 체크 함수
    ur_id = request.form.get('ur_nick') # 회원가입때랑 같은 형식으로 form 태그에서 가져오기 
    ur_pw = request.form.get('ur_pw')

    if database.check_login(ur_id, ur_pw): # 데이터 베이스 내에 아이디랑 비밀번호가 일치하면 true 반환, 아니면 false 반환 (패스워드 까지 검사 하고 온거임) 근데 네이밍 좀 바꿔라 check_login 부분좀;통일좀;
        session['user_id'] = ur_id # user_id <-(사용자가 입력한거) 가 세션에 저장 되고 그 세션이 ur_id랑 일치하면 로그인 성공하게 함 
        return redirect(url_for('notes.note_page')) # note_page() 함수로 이동 (오답노트 페이지) note_page() 함수는 notes.py 에 있음
    else: # false 일때 (로그인 실패)
        return "<h3>아이디랑 비밀번호를 다시 확인해 주세요</h3>" # 출력문

@auth_bp.route('/logout') # 새로운 로그아웃 페이지 추가 
def logout(): # 로그아웃 함수
    session.pop('user_id', None) # 세션에서 로그인 증명서(user_id)를 파기한다(pop) None은 기본값으로, 만약 user_id가 세션에 없으면 아무 일도 안 일어나게 함
    return redirect(url_for('auth.show_login_page')) # 'auth' 파일의 'show_login_page' 함수 주소로 강제 이동(리디렉트)시킨다 - 멱살잡이

