def note_to_markdown(note):
    md = f"""# {note[2]}

- **카테고리**: {note[3]}
- **작성일자**: {note[5]}

## 풀이 / 배운 점

{note[4]}
"""
    return md