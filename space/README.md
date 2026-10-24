---
title: kocer
emoji: 🎙️
colorFrom: blue
colorTo: yellow
sdk: static
app_file: index.html
pinned: false
license: mit
short_description: 한국어 STT CER. 띄어쓰기·숫자·부호 차이를 오류로 안 셈
---

정답과 STT 출력을 넣으면 기존 CER, kocer CER, 오류 분해를 보여주는 데모입니다. 서버 없이 브라우저 안에서(Pyodide) kocer를 돌립니다. 라이브러리와 벤치마크는 https://github.com/Choi-kwan-u/kocer 에 있습니다.

- `index.html`: 이 Space가 띄우는 페이지 (정적, CPU 한도 안 씀)
- `demo_core.py`: 채점·렌더 코드 (브라우저와 Gradio 버전이 같이 씀)
- `app.py`, `requirements.txt`: 서버 CPU가 있을 때 쓸 Gradio 버전 (README의 `sdk: gradio`로 바꾸면 이걸 띄움)
