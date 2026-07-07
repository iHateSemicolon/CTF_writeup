import os
from dotenv import load_dotenv

load_dotenv()  # .env 환경변수 메모리에 등록 하기

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') # 시크릿 키를 가져오너라 
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'ctf_notes.db')  # 메모리에 지정된거 잇나 찾아보거라 없으면 걍 현재 디렉토리에 ctf_notes.db 파일 만들어라
    