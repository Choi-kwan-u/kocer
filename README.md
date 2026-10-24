# kocer

[![PyPI](https://img.shields.io/pypi/v/kocer)](https://pypi.org/project/kocer/) [![Python](https://img.shields.io/pypi/pyversions/kocer)](https://pypi.org/project/kocer/) [![tests](https://github.com/Choi-kwan-u/kocer/actions/workflows/tests.yml/badge.svg)](https://github.com/Choi-kwan-u/kocer/actions/workflows/tests.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

한국어 STT를 공정하게 채점하는 CER — 띄어쓰기·숫자·문장부호·영문 약어 표기 차이를 오류로 세지 않습니다.

*Fair CER/WER for Korean speech recognition. Spacing, punctuation, number notation (3개 ↔ 세 개) and Latin acronyms (AI ↔ 에이아이) are not counted as errors. Unlike jiwer and nlptutti, kocer scores numbers against every valid Korean reading, keeps the original CER alongside, and tells you where your errors come from. Pure Python, zero dependencies, `jiwer`-compatible API.*

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Choi-kwan-u/kocer/v0.1.6/docs/breakdown-dark.svg">
  <img alt="공개 한국어 ASR 모델 7개 설정의 raw CER 오류를 띄어쓰기·문장부호·숫자/영문·진짜 오류로 나눈 누적 막대. 모델에 따라 46~68%가 표기 차이다." src="https://raw.githubusercontent.com/Choi-kwan-u/kocer/v0.1.6/docs/breakdown-light.svg">
</picture>

위 그림을 **내 모델 출력으로 한 줄에** 얻습니다. 기존 CER 숫자는 그대로 두고, 그 오류가 어디서 왔는지만 나눠 보여줍니다.

```python
>>> import kocer
>>> print(kocer.breakdown(refs, hyps))      # whisper-large-v3, Zeroth test 457발화
raw CER 8.60%  →  kocer CER 2.93%   (2,191 raw errors, 457 pairs, kocer 0.1.5)
띄어쓰기     1,142   52%  █████████████████████
문장부호       226   10%  ████
숫자·영문      258   12%  █████
진짜 오류      565   26%  ██████████
```

문장 하나로 보면 이렇습니다.

```
ref: 사과 세 개 주세요
hyp: 사과 3개 주세요
jiwer CER 0.200   nlptutti CER 0.143   kocer CER 0.000
```

## 설치

```bash
pip install kocer          # 순수 파이썬, 의존성 없음
pip install kocer[fast]    # rapidfuzz로 채점 수십 배 빠름. 긴 문장(자막·회의록)을 많이 재면 권장
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

b = kocer.breakdown(refs, hyps)   # 오류가 어디서 왔는지 개수로 분해
b.spacing, b.punctuation, b.numbers_letters, b.remaining   # 합이 b.raw_errors
b.shares                          # 비율
b.cer                             # {'raw':…, 'nospace':…, 'nopunct':…, 'kocer':…}
print(b)                          # 위의 막대 출력

# 단어처럼 읽는 약어는 직접 넘김 (내장 사전 위에 덮어씀)
kocer.cer("엘지 트윈스", "LG 트윈스")                      # 0.0  철자 읽기
kocer.cer("케이비오 리그", "KBO 리그")                      # 0.0
kocer.cer("유니스트 입학", "UNIST 입학", aliases={"UNIST": "유니스트"})  # 0.0
```

```bash
kocer ref.txt hyp.txt          # 줄 단위 쌍. raw CER, kocer CER, 오류 분해를 출력
kocer ref.txt hyp.txt --diff   # 틀린 글자만 색으로 표시
```

## 계산식

CER = (치환 + 삭제 + 삽입) / 정답 글자 수. 정규화는 정답과 결과 양쪽에 같은 순서로 적용하고, 공백을 뺀 글자 단위로 편집거리를 셉니다. 분모는 정규화 후 정답 글자 수라서 `raw_cer`와 `cer`의 분모가 다릅니다. 둘을 비율로 비교하지 말고, 오류 개수가 필요하면 `breakdown()`을 쓰세요. 정답이 빈 문자열이면 분모를 1로 둡니다. 숫자·영문은 가능한 읽기 후보 중 편집거리가 최소인 것을 고르므로, 같은 문장을 다시 채점해도 결과는 항상 같습니다(결정적).

## 무엇을 무시하고, 무엇을 세는가

정규화는 순서대로 적용되고 각 단계를 끌 수 있습니다.

| 단계 | 기본 | 끄기 | 예 |
|---|---|---|---|
| 유니코드 NFC | 켬 | - | 자모 분리 입력 |
| 문장부호 제거 | 켬 | `punct=False` | `네, 알겠습니다.` = `네 알겠습니다` |
| 필러 제거 (음, 어, 그) | **끔** | `fillers=True` | 실제 단어 "그"도 지워질 수 있어 기본은 끔 |
| 영문 약어·단위 | 켬 | `letters=False` | `AI` = `에이아이`, `NASA` = `나사`, `50%` = `50퍼센트` |
| 숫자 후보 전개 | 켬 | `numbers=False` | `3개` = `세 개`, `3층` = `삼 층` |
| 공백 제거 | CER만 | - | WER은 공백 유지 |

`normalize=False`면 jiwer와 같은 순수 CER을 돌려줍니다.

### 숫자: 정답 하나가 아니라 후보 집합

숫자는 조수사에 따라 읽기가 달라서(3개=세 개, 3층=삼 층, 3시 30분=세 시 삼십 분) 규칙 하나로 정답을 만들 수 없습니다. kocer는 숫자마다 `{원문 숫자, 한자어 읽기, 고유어 읽기, 자릿수 읽기}` 후보를 만들고 CER이 최소가 되는 조합을 고릅니다.

- 조수사 사전([counters.py](src/kocer/counters.py))에 있으면 그 읽기만, **없으면 두 읽기 모두 허용**합니다. 틀리게 감점하는 것보다 관대한 쪽이 안전하다는 정책입니다.
- 반대 방향(ref가 한글 수사, hyp가 숫자)도 처리합니다.
- 전화번호·연도는 자릿수 읽기(010 = 공일공, 2024 = 이공이사)도 후보에 들어갑니다.
- 고유어 읽기는 1~99까지. `100개`는 `백 개`만 허용하고, `백스무 명`(120명)은 아직 안 됩니다.
- 고유어는 관형형(세, 스무)과 단독형(셋, 스물) 둘 다 후보에 넣습니다. 소수점은 `점`만 허용하고 구어 `쩜`은 받지 않습니다.
- 숫자 하나에 후보가 많아 조합이 64개를 넘으면 숫자 구간마다 따로 최적 후보를 고르는 근사를 씁니다.

### "너무 관대하다"는 비판에 대해

정규화는 실제 오류를 숨길 수 있습니다. 그래서 `raw_cer`를 항상 같이 돌려주고, 모든 단계를 끌 수 있게 했습니다. 두 값을 같이 보고하세요.

## 기존 도구와 무엇이 다른가

한국어 STT 채점에는 보통 [jiwer](https://github.com/jitsi/jiwer)나 [nlptutti](https://github.com/hyeonsangjeon/computing-Korean-STT-error-rates)를 씁니다. 셋 다 같은 편집거리로 CER을 계산합니다. 다른 점은 **무엇을 오류로 세느냐**입니다.

- **jiwer**는 언어를 가리지 않는 범용 도구입니다. 띄어쓰기와 문장부호도 기본으로 오류로 셉니다.
- **nlptutti**는 한국어용입니다. 띄어쓰기와 문장부호는 무시하지만, 숫자와 영문 표기 차이는 오류로 셉니다.
- **kocer**는 여기에 더해 숫자 읽기(3개 = 세 개)와 영문 약어 읽기(AI = 에이아이)까지 같은 말로 봅니다.

### 같은 문장, 세 도구의 CER

2026-10-24 실측. jiwer 4.0.0, nlptutti 0.0.0.24, kocer 0.1.2, 모두 기본 설정.

| 정답 | STT 결과 | jiwer | nlptutti | kocer |
|---|---|---|---|---|
| 네, 알겠습니다. | 네 알겠습니다 | 0.222 | 0.000 | 0.000 |
| 사과 세 개 주세요 | 사과 3개 주세요 | 0.200 | 0.143 | **0.000** |
| 세 시 삼십 분 | 3시 30분 | 0.625 | 0.600 | **0.000** |
| 이천이십사 년 십이 월 | 2024년 12월 | 0.750 | 0.778 | **0.000** |
| 오십 퍼센트 | 50% | 1.000 | 1.000 | **0.000** |
| 에이아이 모델 | AI 모델 | 0.571 | 0.667 | **0.000** |
| 사과 세 개 주세요 | 사과 **네** 개 주세요 | 0.100 | 0.143 | 0.143 |
| 세 시 삼십 분 | 3시 **13**분 | 0.625 | 0.600 | 0.400 |

마지막 두 줄은 진짜 인식 오류입니다. kocer도 오류로 셉니다. "세 시 삼십 분"과 "3시 13분"에서 kocer가 낮은 이유는 "3시"는 맞게 인식한 부분이라 감점하지 않고, 틀린 "13분"만 세기 때문입니다.

### 기능 비교

| | jiwer | nlptutti | kocer |
|---|---|---|---|
| 띄어쓰기·문장부호 무시 | 직접 설정 | 기본 | 기본 |
| 숫자 읽기 차이 무시 (3개 = 세 개) | 없음 | 없음 | 기본 |
| 영문 약어 읽기 차이 무시 (AI = 에이아이) | 없음 | 없음 | 기본, 사용자 사전 지원 |
| 정규화 전·후 CER을 한 번에 반환 | 없음 | 없음 | `raw_cer`, `cer` |
| 오류를 띄어쓰기·문장부호·숫자·진짜 오류로 분해 | 없음 | 없음 | `breakdown()` |
| 여러 모델 비교 리포트, 품질 게이트 | 없음 | 있음 | 없음 |
| 개체명·키워드 오류율 | 없음 | 있음 | 없음 |
| 지원 지표 | WER, CER, MER, WIL, WIP | CER, WER, CRR | CER, WER |
| 필수 의존성 | rapidfuzz, click | jiwer | 없음 |

**이럴 때 kocer를 쓰세요.** 정답 전사와 STT 결과의 숫자·영문 표기 방식이 다를 때입니다. 예를 들어 정답은 한글로 읽은 대로 적었는데 모델은 아라비아 숫자로 출력하는 경우입니다. 이 차이를 오류로 세면 모델 간 비교가 표기 습관 비교가 됩니다.

**이럴 때는 nlptutti가 낫습니다.** 여러 모델의 리포트를 만들거나, 개체명·키워드 단위로 평가하거나, 기준 점수로 CI를 막고 싶을 때입니다. 두 도구를 같이 써도 됩니다.

## 공개 모델 7개, 같은 출력을 네 가지로 채점

공개 한국어 ASR 7개 설정을 공개 테스트셋 세 개(Zeroth 457, FLEURS 382, Common Voice 27 579발화)에서 같은 조건(greedy, 언어 고정)으로 돌리고, 출력은 그대로 둔 채 채점만 바꿨습니다. 맨 위 그림이 그 오류 분해이고, 아래는 kocer CER입니다(단위 %, 총 오류 / 총 정답 글자).

| 모델 | Zeroth | FLEURS | Common Voice 27 | 합산 | 합산 순위 raw → kocer |
|---|---|---|---|---|---|
| BuzzASR/korean | 3.16 | 4.72 | **3.88** | **3.90** | 4 → **1** |
| TeamUNIVA/qwen3_asr_1.7b_ko | 2.37 | **4.25** | 6.00 | 3.92 | 2 → **2** |
| TeamUNIVA/qwen3_asr_1.7b_ko_beta | 2.46 | 4.31 | 6.08 | 3.99 | 3 → 3 |
| openai/whisper-large-v3 | 2.93 | 4.37 | 5.80 | 4.13 | 7 → 4 |
| Qwen/Qwen3-ASR-1.7B | 2.91 | 4.31 | 6.61 | 4.30 | 1 → 5 |
| SenseVoiceSmall (itn 켬 / 끔) | **2.40** / 2.41 | 6.95 / 6.91 | 9.68 / 9.72 | 5.78 / 5.79 | 5, 6 → 6, 7 |

- raw CER이 오류로 센 것의 **46~68%는 표기 차이**였습니다. 대부분은 띄어쓰기와 문장부호이고, 그것만 지워도 whisper-large-v3가 꼴찌에서 2위로 올라옵니다.
- kocer만 처리하는 숫자·영문 몫은 합산 raw 오류의 5~13%이고 거의 전부 Zeroth에서 나옵니다. Zeroth 정답은 숫자를 전부 한글로 적는데 모델은 아라비아 숫자를 뱉기 때문입니다. 이 몫만으로 합산 상위권이 바뀝니다(공백·부호만 지운 단계 대비 TeamUNIVA 정식판 4위 → 2위, BuzzASR 3위 → 1위). 상위 셋(BuzzASR, TeamUNIVA 정식판, beta)은 통계적으로 구분되지 않습니다.
- TeamUNIVA는 beta → 정식판에서 모든 데이터셋이 조금씩 좋아졌지만(합산 −0.07%p) 신뢰구간 안입니다. 숫자를 아라비아로 쓰는 습관(Zeroth 출력의 31%)은 그대로입니다. 그래서 공백·부호만 지우는 채점에서는 두 버전 모두 기본 모델보다 나빠 보이고, 숫자까지 맞추면 기본 모델보다 낫습니다. [비교표](benchmarks/results/univa_compare.md)
- raw > 0이고 kocer = 0인 문장 100건을 저자가 직접 읽은 결과, 99건은 표기 차이만, 0건이 실제 오류를 숨김, 1건이 띄어쓰기 동형이의어로 애매했습니다. 표본은 검수 당시의 6개 설정, Zeroth·FLEURS 출력에서 뽑았고, 그 뒤에 추가한 Common Voice와 TeamUNIVA 정식판 출력은 포함하지 않습니다.

**데이터셋 출처.** 모두 공개 데이터이고 레포의 jsonl에는 정답 전사와 모델 출력만 있습니다(음성 없음).

| 데이터셋 | 분할 | 발화 | 출처 | 라이선스 |
|---|---|---|---|---|
| Zeroth-Korean | test | 457 | [kresnik/zeroth_korean](https://huggingface.co/datasets/kresnik/zeroth_korean) (원본 [goodatlas/zeroth](https://github.com/goodatlas/zeroth)) | CC BY 4.0 |
| FLEURS ko_kr | test | 382 | [google/fleurs](https://huggingface.co/datasets/google/fleurs), 정답은 `raw_transcription` | CC BY 4.0 |
| Common Voice Scripted Speech 27.0 Korean | test | 579 | [Mozilla Data Collective](https://mozilladatacollective.com/datasets/cmu5rwtaf003dnq07e7n3q6tf) | CC0 1.0 |

모든 데이터셋에서 이기는 모델은 없고, 0.3%p 이하 차이는 신뢰구간과 함께 읽어야 합니다. 단계별 CER, 오류 개수 분해, 쌍별 부트스트랩, 디코딩 설정, 모델 출력 전체, 재현 스크립트는 [benchmarks/](benchmarks/)에 있습니다.

### KsponSpeech: 정답을 철자로 쓰느냐 발음으로 쓰느냐

AI-Hub KsponSpeech 평가셋(eval_clean·eval_other 6,000발화, 6.4시간, 대화체)은 숫자 같은 부분을 `(3시)/(세 시)`처럼 철자와 발음 두 가지로 적습니다. 논문마다 어느 쪽을 정답으로 쓰는지 다릅니다. 같은 출력을 두 정답으로 각각 채점했습니다.

| 모델 | kocer CER, 철자 정답 (clean / other) | 정답을 철자 → 발음으로 바꿀 때 변화: 공백·부호 제거 | 같은 변화: kocer |
|---|---|---|---|
| TeamUNIVA/qwen3_asr_1.7b_ko | **6.10 / 6.48** | +0.85 | −0.18 |
| TeamUNIVA/qwen3_asr_1.7b_ko_beta | 6.81 / 7.26 | +0.20 | −0.35 |
| Qwen/Qwen3-ASR-1.7B | 8.70 / 8.59 | −0.77 | −0.03 |
| BuzzASR/korean | 10.14 / 9.41 | +0.53 | −0.10 |
| openai/whisper-large-v3 | 11.07 / 11.87 | +0.66 | +0.07 |
| SenseVoiceSmall (itn 켬 / 끔) | 13.28 / 13.82, 13.09 / 13.72 | +0.20 / +0.19 | −0.19 / −0.19 |

- 공백·부호만 지우는 채점에서는 정답을 어느 쪽으로 고르느냐 하나로 점수가 −0.77~+0.85%p 움직이고, 방향도 모델마다 반대입니다. 숫자를 아라비아로 쓰는 모델은 발음 정답에서, 한글로 쓰는 Qwen 기본 모델은 철자 정답에서 손해를 봅니다. kocer로 채점하면 이 폭이 −0.35~+0.07%p로 줄어듭니다. 남는 차이는 두 정답이 다른 1,110발화 중 452발화가 숫자·영문이 아닌 표기 차이라서 생깁니다.
- 이 데이터에서는 모델 간 차이가 커서(SenseVoice 두 설정끼리를 빼면 바로 아래 순위와 최소 0.76%p) 정답 선택으로 순위가 바뀌지는 않았고, 모든 모델 쌍이 통계적으로 구분됩니다.
- kocer만 처리하는 숫자·영문 몫은 raw 오류의 1~6%로 작습니다. 대화체에서는 띄어쓰기와 문장부호가 raw 오류의 44~52%입니다.
- TeamUNIVA는 KsponSpeech로 학습했을 가능성이 높습니다(모델카드상 개선 폭이 가장 큰 데이터셋). BuzzASR와 whisper는 반복 억제 없는 greedy 디코딩에서 19·25발화가 반복 출력으로 폭주했고(각 오류의 6.7%·4.5%), 이 발화를 빼도 순위는 같습니다.
- 이 결과는 한국지능정보사회진흥원(NIA)의 AI-Hub에서 제공한 '한국어 음성' 데이터를 활용했습니다. 약관상 데이터와 문장별 출력은 레포에 없고, 숫자 표([benchmarks/results/kspon_tables.md](benchmarks/results/kspon_tables.md))와 재현 스크립트만 있습니다.

## 한계

- 대문자 연속은 철자로 읽습니다(`AI` = `에이아이`). 단어처럼 읽는 약어는 `aliases`로 넘기세요. `NASA`, `UNESCO`, `COVID` 등 16개만 내장되어 있습니다.
- 단위 기호는 `%`, `km`, `kg`, `cm`, `mm`, `ml`만 한글로 바꿉니다. `3m`은 `삼 미터`와 다른 것으로 봅니다.
- WER은 띄어쓰기 차이를 오류로 셉니다. 한국어 WER의 본질적 한계이고, CER을 권합니다.
- 조수사 사전은 완전하지 않습니다. 사전에 없는 조수사는 두 읽기를 다 허용합니다. 케이스를 [tests/cases.tsv](tests/cases.tsv)에 추가하는 PR을 환영합니다.
- 입력은 텍스트 쌍만 받습니다. 음성 파일·모델 실행은 다루지 않습니다.

## 인용과 보고

점수를 논문·모델카드·보고서에 적을 때는 **버전을 함께** 적어 주세요. 정규화 규칙(조수사 사전, 약어 사전)이 버전마다 바뀌어서, 버전이 다르면 같은 출력도 점수가 다릅니다. `raw_cer`도 같이 적으면 다른 도구로 잰 숫자와 비교할 수 있습니다.

```
CER 4.13% (raw) / 2.93% (kocer 0.1.5)
```

```bibtex
@software{kocer,
  author  = {Choi, Kwan-u},
  title   = {kocer: fair CER/WER for Korean speech recognition},
  year    = {2026},
  version = {0.1.5},
  url     = {https://github.com/Choi-kwan-u/kocer}
}
```

깃허브 레포 오른쪽의 "Cite this repository"에서 같은 내용을 복사할 수 있습니다([CITATION.cff](CITATION.cff)). 버전은 `kocer.__version__` 또는 `kocer --version`으로 확인합니다.

### 사용 사례

kocer로 채점한 모델·논문·데이터셋이 있으면 [이슈](https://github.com/Choi-kwan-u/kocer/issues)로 알려주세요. 여기에 목록을 유지합니다.

- (아직 없음)

## 관련 연구와 구현

- [jiwer](https://github.com/jitsi/jiwer): 범용 WER/CER. kocer의 `cer()`·`wer()` 시그니처가 이것을 따릅니다.
- [nlptutti](https://github.com/hyeonsangjeon/computing-Korean-STT-error-rates): 한국어 STT 평가. 띄어쓰기·문장부호 무시, 시스템 비교 리포트, 개체명 평가.
- [Open ASR Leaderboard](https://github.com/huggingface/open_asr_leaderboard)의 OIWER: 참조에 허용되는 철자가 여럿일 때 그중 하나와 맞으면 정답으로 치는 방식. kocer의 숫자 후보 집합은 같은 발상을 한국어 숫자·조수사에 적용한 것입니다.
- "What is lost in Normalization?" (EMNLP 2024): Whisper식 정규화가 비영어권 문자에서 점수를 왜곡한다는 분석.
- [whisper_normalizer](https://github.com/kurianbenoy/whisper_normalizer): Whisper 논문의 영어·기본 정규화기 구현.

## 라이선스

MIT. 사용·수정·재배포에 제한이 없고, 인용은 의무가 아니라 부탁입니다.
