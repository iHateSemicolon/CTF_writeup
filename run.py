from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


#설명: 이제 진짜 실행 파일은 이거 하나예요.
#create_app()으로 앱을 만들고 실행만 담당합니다. app.py는 더 이상 필요 없어요 (삭제하거나 백업용으로만 남겨두세요).