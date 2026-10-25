# kocer

[![PyPI](https://img.shields.io/pypi/v/kocer)](https://pypi.org/project/kocer/) [![Python](https://img.shields.io/pypi/pyversions/kocer)](https://pypi.org/project/kocer/) [![tests](https://github.com/Choi-kwan-u/kocer/actions/workflows/tests.yml/badge.svg)](https://github.com/Choi-kwan-u/kocer/actions/workflows/tests.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![demo](https://img.shields.io/badge/demo-브라우저에서_써보기-2a78d6)](https://choi-kwan-u.github.io/kocer/) [![Hugging Face Space](https://img.shields.io/badge/🤗_Space-kocer-ffd21e)](https://huggingface.co/spaces/Gonow1/kocer)

한국어 STT를 공정하게 채점하는 CER — 띄어쓰기·숫자·문장부호·영문 약어 표기 차이를 오류로 세지 않습니다.

**[설치 없이 브라우저에서 써보기 →](https://choi-kwan-u.github.io/kocer/)** 정답과 STT 출력을 붙여넣으면 기존 CER, kocer CER, 오류 분해가 바로 나옵니다.

*Fair CER for Korean speech recognition. Number notation (3개 ↔ 세 개) is scored against every valid Korean reading, the original CER is kept alongside, and `breakdown()` tells you where your errors come from. Pure Python, zero dependencies, `jiwer`-compatible API.*

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Choi-kwan-u/kocer/main/docs/breakdown-dark.svg">
  <img alt="공개 한국어 ASR 모델 7개 설정의 기존 CER 오류를 띄어쓰기·문장부호·숫자/영문·진짜 오류로 나눈 누적 막대. 모델에 따라 46~68%가 표기 차이다." src="https://raw.githubusercontent.com/Choi-kwan-u/kocer/main/docs/breakdown-light.svg">
</picture>

위 그림을 **내 모델 출력으로 한 줄에** 얻습니다. 기존 CER은 그대로 두고, 그 오류가 어디서 왔는지 나눠 보여줍니다.

> **기존 CER**은 정답과 받아쓰기를 글자 그대로 비교한 값입니다. 띄어쓰기와 문장부호도 글자로 셉니다. [jiwer](https://github.com/jitsi/jiwer)의 `cer()`와 Hugging Face `evaluate`의 `cer`가 이렇게 계산하고, 아래 출력의 `raw CER`이 이 값입니다.

```python
>>> import kocer
>>> print(kocer.breakdown(refs, hyps))      # whisper-large-v3, Zeroth test 457발화
raw CER 8.60%  →  kocer CER 2.93%   (2,191 raw errors, 457 pairs, kocer 0.3.0)
띄어쓰기     1,142   52%  █████████████████████
문장부호       226   10%  ████
숫자·영문      258   12%  █████
진짜 오류      565   26%  ██████████
```

## 왜 필요한가

정답이 "세 시에 만나"인데 모델이 "3시에 만나"라고 받아쓰면, 맞은 걸까요? 사람이 보면 맞았습니다. 그런데 기존 CER은 글자가 다르니 틀렸다고 셉니다. 띄어쓰기와 문장부호를 빼고 재는 [nlptutti](https://github.com/hyeonsangjeon/computing-Korean-STT-error-rates) 같은 한국어 도구도 숫자 표기 차이는 그대로 오류로 셉니다.

이게 진짜 문제가 되는 건 **모델을 비교할 때**입니다. 숫자를 아라비아로 쓰는 모델과 한글로 쓰는 모델이 있으면, 정답 전사가 어느 쪽으로 적혀 있느냐에 따라 이기는 쪽이 바뀝니다. 실력이 아니라 숫자 쓰는 습관을 비교하게 되는 겁니다.

실제로 확인한 사례입니다. 같은 두 모델의 같은 받아쓰기 결과를, 정답의 숫자 표기만 바꿔서 채점했습니다.

| 정답 전사의 숫자 표기 | 띄어쓰기·문장부호를 뺀 CER의 결론 | kocer의 결론 |
|---|---|---|
| 아라비아 숫자 (`3시`) | 새 모델이 더 좋다 | 새 모델이 더 좋다 |
| 한글 (`세 시`) | 새 모델이 **더 나쁘다** | 새 모델이 더 좋다 |

띄어쓰기와 문장부호를 빼고 재도, 정답을 어떻게 적었느냐에 따라 정반대 결론이 나옵니다. kocer는 같은 말을 다르게 적은 것을 맞은 것으로 보기 때문에, 어느 쪽 정답으로 재도 같은 결론이 나옵니다.

그래서 비슷한 모델끼리, 특히 새 버전이 숫자 쓰는 습관을 바꿨을 때 필요합니다. 모델끼리 실력 차이가 크면 어떤 도구로 재도 순위는 거의 같습니다. 차이가 진짜인지는 `kocer.compare()`로 확인할 수 있습니다.

<details>
<summary>자세한 숫자</summary>

- 데이터: AI-Hub KsponSpeech 평가셋 중 숫자가 든 628발화. 이 데이터는 숫자를 `(3시)/(세 시)`처럼 두 가지로 적어 두어서, 같은 음성에 대해 두 정답을 만들 수 있습니다.
- 모델: 원래 모델 [Qwen/Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B)와, 이를 한국어 데이터로 추가 학습한 새 모델 [TeamUNIVA/qwen3_asr_1.7b_ko](https://huggingface.co/TeamUNIVA/qwen3_asr_1.7b_ko).
- 띄어쓰기·문장부호를 뺀 CER(nlptutti 방식): 정답이 `3시`면 새 모델이 8.50%p 좋고, `세 시`면 4.13%p 나쁩니다.
- kocer: 정답이 `3시`면 새 모델이 2.34%p 좋고, `세 시`여도 2.36%p 좋습니다.
- 네 값 모두 문장 단위 paired bootstrap 95% 신뢰구간이 0을 벗어납니다. 자세한 내용은 [benchmarks/](benchmarks/)에 있습니다.

</details>

## 설치

```bash
pip install kocer          # 순수 파이썬, 의존성 없음
pip install "kocer[fast]"  # rapidfuzz로 수십 배 빠름. 긴 문장을 많이 잴 때 권장
```

## 사용

```python
import kocer

kocer.cer("사과 세 개 주세요", "사과 3개 주세요")    # 0.0
kocer.cer(refs, hyps)                                 # 리스트는 코퍼스 단위 (jiwer와 같은 집계)

r = kocer.measure("세 시 삼십 분", "3시 30분")
r.cer, r.raw_cer                                      # 0.0, 0.625  (정규화 후, 정규화 전)

print(kocer.breakdown(refs, hyps))                    # 오류를 종류별로 분해 (위 출력)
print(kocer.compare(refs, {"새 모델": new, "이전 모델": old}))   # 모델 비교: 순위와 차이의 95% 신뢰구간
kocer.cer("유니스트 입학", "UNIST 입학", aliases={"UNIST": "유니스트"})   # 단어처럼 읽는 약어
kocer.cer("(7시)/(일곱 시)에 만나", "7시에 만나")    # 0.0  AI-Hub 이중 표기는 양쪽 다 정답
kocer.cer("b/ 그거+ 그거 *좋아", "그거 그거 좋아", aihub=True)   # 0.0  AI-Hub 원본 전사를 정제 없이
```

```bash
kocer ref.txt hyp.txt          # 줄 단위 쌍. raw CER, kocer CER, 오류 분해
kocer ref.txt hyp.txt --diff   # 틀린 글자만 색으로 표시
kocer ref.txt new.txt old.txt  # 결과 파일이 둘 이상이면 모델 비교
```

<details>
<summary>API 전체</summary>

```python
kocer.wer(ref, hyp)

r = kocer.measure("세 시 삼십 분", "3시 30분")
r.ops         # {'S': 0, 'D': 0, 'I': 0}
r.alignment   # [('H', '세', '세'), ...]
r.chosen_ref  # 숫자 후보 중 실제로 채택된 정답
r.chosen_hyp  # '세시삼십분'

b = kocer.breakdown(refs, hyps)
b.spacing, b.punctuation, b.numbers_letters, b.remaining   # 합이 b.raw_errors
b.shares                          # 비율
b.cer                             # {'raw':…, 'nospace':…, 'nopunct':…, 'kocer':…}

c = kocer.compare(refs, {"A": hyps_a, "B": hyps_b, "C": hyps_c}, n_boot=2000, seed=0)
c.cer                             # 시스템별 CER
c.pairs[("A", "B")]               # (CER A − CER B, 95% 하한, 상한). 문장 단위 paired bootstrap
c.significant("A", "B")           # 차이가 0이 아닌가
c.ranks["A"]                      # (순위 하한, 상한, 1위 확률)
print(c)                          # 표로 출력. numpy가 있으면 빠르게, 없으면 순수 파이썬으로 계산

kocer.cer("엘지 트윈스", "LG 트윈스")      # 0.0  대문자 연속은 철자 읽기
kocer.cer("케이비오 리그", "KBO 리그")      # 0.0
```

</details>

## 기존 도구와 비교

[jiwer](https://github.com/jitsi/jiwer), [nlptutti](https://github.com/hyeonsangjeon/computing-Korean-STT-error-rates), kocer는 모두 같은 편집거리로 CER을 계산합니다. 다른 건 **무엇을 오류로 세느냐**입니다. jiwer는 띄어쓰기·문장부호도 오류로 세고, nlptutti는 그 둘은 무시하지만 숫자·영문 표기 차이는 셉니다. kocer는 숫자와 영문 약어 읽기까지 같은 말로 봅니다.

| 정답 | STT 결과 | jiwer | nlptutti | kocer |
|---|---|---|---|---|
| 네, 알겠습니다. | 네 알겠습니다 | 0.222 | 0.000 | 0.000 |
| 사과 세 개 주세요 | 사과 3개 주세요 | 0.200 | 0.143 | **0.000** |
| 세 시 삼십 분 | 3시 30분 | 0.625 | 0.600 | **0.000** |
| 이천이십사 년 십이 월 | 2024년 12월 | 0.750 | 0.778 | **0.000** |
| 에이아이 모델 | AI 모델 | 0.571 | 0.667 | **0.000** |
| 사과 세 개 주세요 | 사과 **네** 개 주세요 | 0.100 | 0.143 | 0.143 |
| 세 시 삼십 분 | 3시 **13**분 | 0.625 | 0.600 | 0.400 |

마지막 두 줄은 진짜 인식 오류이고, kocer도 오류로 셉니다. jiwer 4.0.0, nlptutti 0.0.0.24, kocer 0.3.0, 모두 기본 설정.

개체명·키워드 평가나 품질 게이트(기준 점수로 CI 막기)가 필요하면 nlptutti가 낫습니다. 두 도구를 같이 써도 됩니다.

<details>
<summary>기능 비교표</summary>

| | jiwer | nlptutti | kocer |
|---|---|---|---|
| 띄어쓰기·문장부호 무시 | 직접 설정 | 기본 | 기본 |
| 숫자 읽기 차이 무시 (3개 = 세 개) | 없음 | 없음 | 기본 |
| 영문 약어 읽기 차이 무시 (AI = 에이아이) | 없음 | 없음 | 기본, 사용자 사전 지원 |
| 정규화 전·후 CER을 한 번에 반환 | 없음 | 없음 | `raw_cer`, `cer` |
| 오류를 띄어쓰기·문장부호·숫자·진짜 오류로 분해 | 없음 | 없음 | `breakdown()` |
| 여러 모델 비교, 쌍별 신뢰구간 | 없음 | 있음 | `compare()` |
| 품질 게이트 (기준 점수로 CI 막기) | 없음 | 있음 | 없음 |
| 개체명·키워드 오류율 | 없음 | 있음 | 없음 |
| 지원 지표 | WER, CER, MER, WIL, WIP | CER, WER, CRR | CER, WER |
| 필수 의존성 | rapidfuzz, click | jiwer | 없음 |

`오십 퍼센트` / `50%`도 jiwer와 nlptutti는 1.000, kocer는 0.000입니다.

</details>

## 채점 규칙

띄어쓰기와 문장부호를 지우고, 숫자와 영문 약어는 가능한 읽기 중 CER이 가장 낮은 것을 고릅니다. 모든 단계는 끌 수 있고, 정규화 전 CER(`raw_cer`)을 항상 같이 돌려줍니다. 정규화가 실제 오류를 숨길 수 있으니 두 값을 같이 보고하세요.

<details>
<summary>단계별 설정, 숫자 후보 규칙, 계산식</summary>

| 단계 | 기본 | 끄기 | 예 |
|---|---|---|---|
| 유니코드 NFC | 켬 | - | 자모 분리 입력 |
| 문장부호 제거 | 켬 | `punct=False` | `네, 알겠습니다.` = `네 알겠습니다` |
| 필러 제거 (음, 어, 그) | **끔** | `fillers=True` | 실제 단어 "그"도 지워질 수 있어 기본은 끔 |
| 영문 약어·단위 | 켬 | `letters=False` | `AI` = `에이아이`, `NASA` = `나사`, `50%` = `50퍼센트` |
| 숫자 후보 전개 | 켬 | `numbers=False` | `3개` = `세 개`, `3층` = `삼 층` |
| AI-Hub 이중 표기 | 켬 | `dual=False` | `(7시)/(일곱 시)` = `7시` = `일곱 시` |
| AI-Hub 잡음 태그·표시 제거 | **끔** | `aihub=True`로 켬 | `b/`, `n/`, `어/`, `+`, `*` 제거. 일반 텍스트의 `C++`를 지키려고 기본은 끔 |
| 공백 제거 | CER만 | - | WER은 공백 유지 |

`normalize=False`면 jiwer와 같은 순수 CER을 돌려줍니다.

**숫자: 정답 하나가 아니라 후보 집합.** 숫자는 조수사에 따라 읽기가 달라서(3개 = 세 개, 3층 = 삼 층) 규칙 하나로 정답을 만들 수 없습니다. 숫자마다 `{원문 숫자, 한자어 읽기, 고유어 읽기, 자릿수 읽기}` 후보를 만들고 CER이 최소가 되는 조합을 고릅니다.

- 조수사 사전([counters.py](src/kocer/counters.py))에 있으면 그 읽기만, 없으면 두 읽기를 모두 허용합니다.
- 반대 방향(정답이 한글 수사, 결과가 숫자)도 처리합니다.
- 전화번호·연도는 자릿수 읽기(010 = 공일공, 2024 = 이공이사)도 후보입니다.
- 고유어 읽기는 1~99까지이고, 관형형(세, 스무)과 단독형(셋, 스물)을 모두 넣습니다. 소수점은 `점`만 받고 구어 `쩜`은 받지 않습니다.
- 후보 조합이 64개를 넘으면 숫자 구간마다 따로 최적 후보를 고르는 근사를 씁니다.

**계산식.** CER = (치환 + 삭제 + 삽입) / 정답 글자 수. 정규화는 정답과 결과에 같은 순서로 적용하고, 공백을 뺀 글자 단위로 셉니다. 분모가 정규화 후 정답 글자 수라서 `raw_cer`와 `cer`의 분모가 다릅니다. 둘을 비율로 비교하지 말고, 오류 개수가 필요하면 `breakdown()`을 쓰세요. 결과는 항상 같습니다(결정적).

</details>

## 공개 모델 벤치마크

공개 한국어 ASR 7개 설정을 Zeroth, FLEURS, Common Voice 27, KsponSpeech(합계 7,418발화)에서 돌리고, 같은 출력을 네 단계로 채점했습니다.

- Zeroth·FLEURS·Common Voice(1,418발화) 기준으로, 기존 CER이 센 오류의 **46~68%는 표기 차이**였습니다. 대부분은 띄어쓰기와 문장부호입니다.
- 숫자가 든 문장에서는 기존 채점이 비교 방향을 틀립니다(위 표). 전체 평균으로 보면 숫자 없는 문장이 많아 차이가 작아집니다.
- 정규화가 진짜 오류를 숨기지 않는지 100건을 직접 읽었습니다. 실제 오류를 숨긴 경우는 0건이었습니다.

모델별 점수, 단계별 CER, 신뢰구간, 디코딩 설정, 재현 스크립트는 [benchmarks/](benchmarks/)에 있습니다. KsponSpeech 결과는 한국지능정보사회진흥원(NIA)의 AI-Hub에서 제공한 '한국어 음성' 데이터를 활용했고, 약관상 숫자 표만 공개합니다.

<details>
<summary>모델별 kocer CER</summary>

| 모델 | Zeroth | FLEURS | Common Voice 27 | KsponSpeech clean / other |
|---|---|---|---|---|
| TeamUNIVA/qwen3_asr_1.7b_ko | 2.37 | **4.25** | 6.00 | **6.10 / 6.48** |
| TeamUNIVA/qwen3_asr_1.7b_ko_beta | 2.46 | 4.31 | 6.08 | 6.81 / 7.26 |
| BuzzASR/korean | 3.16 | 4.72 | **3.88** | 10.14 / 9.41 |
| openai/whisper-large-v3 | 2.93 | 4.37 | 5.80 | 11.07 / 11.87 |
| Qwen/Qwen3-ASR-1.7B | 2.91 | 4.31 | 6.61 | 8.70 / 8.59 |
| SenseVoiceSmall (itn 켬) | **2.40** | 6.95 | 9.68 | 13.28 / 13.82 |
| SenseVoiceSmall (itn 끔) | 2.41 | 6.91 | 9.72 | 13.09 / 13.72 |

단위 %, 총 오류 / 총 정답 글자. KsponSpeech는 철자 정답 기준. 모든 데이터셋에서 이기는 모델은 없고, 각 모델은 학습 데이터와 가까운 데이터셋에서 강합니다(BuzzASR은 Common Voice, TeamUNIVA는 KsponSpeech로 보임). 디코딩은 모두 greedy이고, BuzzASR을 모델카드 권장 설정(반복 억제)으로 다시 돌리면 네 데이터셋 모두 오히려 나빠집니다([자세히](benchmarks/README.md)).

</details>

## 한계

- 숫자와 영문 약어가 아닌 표기 차이(구어 축약, 발음대로 적은 표기)는 오류로 셉니다.
- 영문 약어 처리는 공개 데이터에 영문이 거의 없어 효과를 검증하지 못했습니다. 효과가 확인된 건 숫자입니다.
- 내장 약어 사전은 16개뿐입니다. 단어처럼 읽는 약어는 `aliases`로 넘기세요.
- 단위 기호는 `%`, `km`, `kg`, `cm`, `mm`, `ml`만 바꿉니다. 조수사 사전도 완전하지 않습니다. [tests/cases.tsv](tests/cases.tsv)에 케이스를 추가하는 PR을 환영합니다.
- WER은 띄어쓰기 차이를 오류로 셉니다. 한국어에서는 CER을 권합니다.

## 인용과 보고

점수를 적을 때는 버전을 함께 적어 주세요. 정규화 규칙이 버전마다 바뀌어 같은 출력도 점수가 다를 수 있습니다. `raw_cer`도 같이 적으면 다른 도구로 잰 숫자와 비교할 수 있습니다.

```
CER 4.13% (raw) / 2.93% (kocer 0.3.0)
```

레포 오른쪽의 "Cite this repository"에서 인용 형식을 복사할 수 있습니다([CITATION.cff](CITATION.cff)).

<details>
<summary>BibTeX, 관련 연구</summary>

```bibtex
@software{kocer,
  author  = {Choi, Kwan-u},
  title   = {kocer: fair CER/WER for Korean speech recognition},
  year    = {2026},
  version = {0.3.0},
  url     = {https://github.com/Choi-kwan-u/kocer}
}
```

- [jiwer](https://github.com/jitsi/jiwer): 범용 WER/CER. kocer의 `cer()`·`wer()` 시그니처가 이것을 따릅니다.
- [nlptutti](https://github.com/hyeonsangjeon/computing-Korean-STT-error-rates): 한국어 STT 평가. 띄어쓰기·문장부호 무시, 시스템 비교 리포트, 개체명 평가.
- [Open ASR Leaderboard](https://github.com/huggingface/open_asr_leaderboard)의 OIWER: 참조에 허용되는 철자가 여럿일 때 그중 하나와 맞으면 정답으로 치는 방식. kocer의 숫자 후보 집합은 같은 발상을 한국어 숫자·조수사에 적용한 것입니다.
- "What is lost in Normalization?" (EMNLP 2024): Whisper식 정규화가 비영어권 문자에서 점수를 왜곡한다는 분석.
- [whisper_normalizer](https://github.com/kurianbenoy/whisper_normalizer): Whisper 논문의 영어·기본 정규화기 구현.

</details>

## 라이선스

[MIT](LICENSE)

---

도움이 됐다면 ⭐ 스타를 눌러 주세요. 다른 한국어 STT 연구자들이 이 도구를 찾는 데 도움이 됩니다.
