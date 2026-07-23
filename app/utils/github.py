# app/utils/github_export.py
import os
import base64
import requests
from app.utils.md import note_to_markdown
def push_to_github(note):
    token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPO')
    filename = f"{note[3]}/note_{note[0]}.md"  # category 폴더 안에 저장
    content = note_to_markdown(note)  # 저번에 만든 함수 재사용

    url = f"https://api.github.com/repos/{repo}/contents/{filename}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    data = {
        "message": f"add writeup: {note[2]}",
        "content": base64.b64encode(content.encode()).decode(),
    }
    res = requests.put(url, json=data, headers=headers)
    return res.status_code in (200, 201)