import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일을 읽어서 환경변수로 등록

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'ctf_notes.db')

"""
설명: load_dotenv()가 .env 파일 내용을 파이썬이 읽을 수 있는 환경변수로 올려줘요.
 os.environ.get('SECRET_KEY')로 꺼내 쓰는 거고요. DATABASE_PATH는 두 번째 인자로 기본값('ctf_notes.db')을 줘서, .env에 안 써놔도 에러 안 나게 해뒀습니다.
python-dotenv 패키지 설치 필요: pip install python-dotenv
"""