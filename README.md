# About
# CRN (CTF Rapid Note)

> **Fast, Safe, and Markdown-based CTF Writeup Management System**
> CTF 문제를 풀며 작성하는 빠른 로컬 저장 및 마크다운 기반의 오답노트 웹 애플리케이션입니다.

---

## Key Features (주요 기능)

* **Rapid Local Storage**: 작성한 오답노트를 SQLite DB에 안전하게 저장 및 관리
* **Markdown Export**: 작성한 오답노트를 원클릭으로 `.md` 마크다운 파일로 변환 및 다운로드 (`export_note`)
* **Secure Authentication**: 
  * Werkzeug 기반 비밀번호 단방향 암호화 해싱 (`scrypt`)
  * CSRF 토큰 검증 및 보안 세션 쿠키 설정 (`HttpOnly`, `SameSite=Lax`)
* **Blueprint Architecture**: `auth` 및 `notes` 모듈 분리로 깔끔한 백엔드 구조 유지

---

## Tech Stack (기술 스택)

* **Backend**: Python 3, Flask, Flask-WTF (CSRF)
* **Database**: SQLite3
* **Frontend**: HTML5, Jinja2 Template, Bootstrap 5
* **Security**: Werkzeug Security (Password Hashing)

---

## TODO / Roadmap (추후 계획)
[x] 세션 기반 인증 및 비밀번호 해싱 (auth)

[x] 오답노트 작성 및 조회 기능 (notes)

[x] 작성한 오답노트 .md 내보내기 기능

[ ] 회원가입 성공 시 템플릿 렌더링 및 UI 리팩토링

[ ] GitHub OAuth 연동

[ ] 작성한 Writeup을 지정한 GitHub 레포지토리로 자동 Commit/Push 기능

---

## Project Structure (프로젝트 구조)

```text
CRN/
├── app/
│   ├── templates/
│   │   ├── login.html
│   │   ├── my_notes.html
│   │   ├── note.html
│   │   ├── signup.html
│   ├── routes/
│   │   ├── auth.py          # 회원가입 및 로그인/로그아웃 라우트
│   │   ├── _init_.py       
│   │   └── notes.py         # 오답노트 작성, 조회, MD 내보내기 라우트
│   ├── utils/
│   │   └── md.py            # 마크다운 변환 유틸리티
│   ├── _init_.py  
│   ├── config.py            # 환경변수 및 기본 설정
│   └── database.py          # SQLite DB 테이블 생성 및 C.R.U.D 로직
├── run.py                   # 앱 실행 엔트리포인트
├── ctf_notes.db             # 로컬 SQLite 데이터베이스
├── .env                     # 환경변수 (SECRET_KEY 등)
├── .gitignore
└── README.md
