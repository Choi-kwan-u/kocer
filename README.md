# kocer

한국어 STT를 공정하게 채점하는 CER — 띄어쓰기·숫자·문장부호·영문 약어 표기 차이를 오류로 세지 않습니다.

*Fair CER/WER for Korean speech recognition. Spacing, punctuation, number notation (3개 ↔ 세 개) and Latin acronyms (AI ↔ 에이아이) are not counted as errors. Pure Python, zero dependencies, `jiwer`-compatible API.*

```
ref: 사과 세 개 주세요
hyp: 사과 3개 주세요
jiwer CER 0.200   nlptutti CER 0.143   kocer CER 0.000
```

## 설치

```bash
pip install git+https://github.com/Choi-kwan-u/kocer.git
```

## 사용

```python
import kocer

kocer.cer("사과 세 개 주세요", "사과 3개 주세요")   # 0.0
kocer.cer(refs, hyps)                                # 리스트도 됨 (jiwer와 같은 코퍼스 집계)
kocer.wer(ref, hyp)

r = kocer.measure("세 시 삼십 분", "3시 30분")
r.cer         # 0.0  정규화 후
r.raw_cer     # 0.625  정규화 전 (jiwer와 같은 값). 둘의 차이가 "가짜 오류"의 크기
r.ops         # {'S': 0, 'D': 0, 'I': 0}
r.alignment   # [('H', '세', '세'), ...]
r.chosen_ref  # 숫자 후보 중 실제로 채택된 정답
r.chosen_hyp  # '세시삼십분'
```

```bash
kocer ref.txt hyp.txt          # 줄 단위 쌍, raw CER과 kocer CER을 같이 출력
kocer ref.txt hyp.txt --diff   # 틀린 글자만 색으로 표시
```

## 무엇을 무시하고, 무엇을 세는가

정규화는 순서대로 적용되고 각 단계를 끌 수 있습니다.

| 단계 | 기본 | 끄기 | 예 |
|---|---|---|---|
| 유니코드 NFC | 켬 | - | 자모 분리 입력 |
| 문장부호 제거 | 켬 | `punct=False` | `네, 알겠습니다.` = `네 알겠습니다` |
| 필러 제거 (음, 어, 그) | **끔** | `fillers=True` | 실제 단어 "그"도 지워질 수 있어 기본은 끔 |
| 영문 약어·단위 | 켬 | `letters=False` | `AI` = `에이아이`, `50%` = `50퍼센트` |
| 숫자 후보 전개 | 켬 | `numbers=False` | `3개` = `세 개`, `3층` = `삼 층` |
| 공백 제거 | CER만 | - | WER은 공백 유지 |

`normalize=False`면 jiwer와 같은 순수 CER을 돌려줍니다.

### 숫자: 정답 하나가 아니라 후보 집합

숫자는 조수사에 따라 읽기가 달라서(3개=세 개, 3층=삼 층, 3시 30분=세 시 삼십 분) 규칙 하나로 정답을 만들 수 없습니다. kocer는 숫자마다 `{원문 숫자, 한자어 읽기, 고유어 읽기, 자릿수 읽기}` 후보를 만들고 CER이 최소가 되는 조합을 고릅니다.

- 조수사 사전([counters.py](src/kocer/counters.py))에 있으면 그 읽기만, **없으면 두 읽기 모두 허용**합니다. 틀리게 감점하는 것보다 관대한 쪽이 안전하다는 정책입니다.
- 반대 방향(ref가 한글 수사, hyp가 숫자)도 처리합니다.
- 전화번호·연도는 자릿수 읽기(010 = 공일공, 2024 = 이공이사)도 후보에 들어갑니다.
- 고유어 읽기는 1~99까지. `100개`는 `백 개`만 허용합니다.

### "너무 관대하다"는 비판에 대해

정규화는 실제 오류를 숨길 수 있습니다. 그래서 `raw_cer`를 항상 같이 돌려주고, 모든 단계를 끌 수 있게 했습니다. 두 값을 같이 보고하세요.

## 기존 도구 비교 (2026-10-23 실측)

nlptutti 0.0.0.24, jiwer 4.0.0. [tests/cases.tsv](tests/cases.tsv)의 케이스 일부.

| ref | hyp | jiwer | nlptutti | kocer |
|---|---|---|---|---|
| 사과 세 개 주세요 | 사과 3개 주세요 | 0.200 | 0.143 | 0.000 |
| 삼 층으로 가세요 | 3층으로 가세요 | 0.222 | 0.143 | 0.000 |
| 세 시 삼십 분 | 3시 30분 | 0.625 | 0.600 | 0.000 |
| 에이아이 모델 | AI 모델 | 0.571 | 0.667 | 0.000 |
| 네, 알겠습니다. | 네 알겠습니다 | 0.222 | 0.000 | 0.000 |
| 오늘날씨가좋다 | 오늘 날씨가 좋다 | 0.286 | 0.000 | 0.000 |

nlptutti는 띄어쓰기·문장부호를 이미 처리하고, CLI·코퍼스 비교 리포트·개체명 평가 등 kocer에 없는 기능이 많습니다. kocer의 차이는 숫자·영문 약어 정규화와 `raw_cer` 대비 표시입니다.

## 한계

- WER은 띄어쓰기 차이를 오류로 셉니다. 한국어 WER의 본질적 한계이고, CER을 권합니다.
- 조수사 사전은 완전하지 않습니다. 사전에 없는 조수사는 두 읽기를 다 허용합니다. 케이스를 [tests/cases.tsv](tests/cases.tsv)에 추가하는 PR을 환영합니다.
- 입력은 텍스트 쌍만 받습니다. 음성 파일·모델 실행은 다루지 않습니다.

## 라이선스

MIT
