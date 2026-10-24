# 실험 노트 (2026-10-24)

## 환경
- RTX 4060 Ti 8GB, Windows 11, Python 3.10.11 (Thonny base)
- venv_whisper: torch 2.6.0+cu124, transformers 5.20.2, kocer 0.1.2, nlptutti 0.0.0.24, jiwer 4.0.0, datasets 5.1.0
- venv_qwen: qwen-asr 0.0.6, transformers 4.57.6, torch 2.6.0+cu124
- venv_sense: funasr 1.4.16, torch 2.6.0+cu124

## 데이터
- Zeroth test 457 (kresnik/zeroth_korean parquet), FLEURS ko_kr test 382 (raw_transcription을 ref로 사용), 16 kHz wav로 변환
- Common Voice 17 ko: gated — HF 토큰 없음. **사용자 `hf auth login` + 약관 동의 후 `prepare_data.py commonvoice` 실행 필요**
- 참조 전사 통계: results/ref_stats.md (Zeroth: 숫자·영문·문장부호 0%; FLEURS: 숫자 22.5%, 영문 16.0%, 문장부호 100%)

## 디코딩
- 전 모델 greedy(num_beams=1, do_sample=False), 언어 ko 고정, 프롬프트 없음, chunking 없음
- whisper/BuzzASR: fp16, batch 8, max_new_tokens 440. BuzzASR 모델카드의 no_repeat_ngram_size=3/repetition_penalty=1.2는 **쓰지 않음**(공통 조건 우선)
- Qwen: bf16, batch 4, max_new_tokens 256, generation_config do_sample=False 확인
- SenseVoice: language="ko", use_itn True/False, rich_transcription_postprocess 적용(태그 제거). **한국어는 use_itn=True여도 숫자가 한글로 나옴**(천 구백 육십 칠 년) — itn 효과는 사실상 문장부호뿐

## 관찰
- raw CER 분모에는 공백이 포함됨(Zeroth ref 25,472자 중 공백 ~24%). 정규화 후 분모가 줄어 띄어쓰기를 잘 맞춘 모델(SenseVoice noitn)은 kocer CER이 raw보다 약간 높아질 수 있음(2.39→2.41)
- Zeroth 105_003_0478: whisper-large-v3가 "아 또 말씀 하셔서 ... 녹음되고 있는 거야"로 환각. 다른 모델은 앞부분이 잘린 전사를 냄 → 오디오가 문장 중간에서 시작하는 듯. 제외하지 않고 그대로 둠(OOM/빈 출력만 제외하는 규칙)

## kocer 수정 후보 (tests/cases.tsv)
| ref | hyp | 현재 kocer | 문제 |
|---|---|---|---|
| 마흔일곱 주 | 47주 | 0.80 | counters.py에서 "주"(week)가 SINO 전용. Zeroth는 "마흔 일곱 주", "두 주"처럼 고유어로 읽음 → NATIVE에도 추가(_BOTH) |
| 스물 센티미터 | 20cm | 0.17 | 20 고유어 후보가 관형형 "스무"만 생성. 단독형 "스물"도 후보에 추가(하나/둘/셋/넷/스물 vs 한/두/세/네/스무) |
| 오 쩜 구 사 시간 | 5.94시간 | 0.17 | 소수점 읽기 후보에 "점"만 있음. 구어 "쩜"도 추가 |

## 함정 (실제로 밟은 것)
- `pip install qwen-asr`가 1회 ResolutionImpossible(flask 해상 실패)로 죽음 → 재실행으로 해결(일시적 네트워크)
- venv_qwen의 huggingface_hub로 snapshot_download 시 WinError 1314(심볼릭 링크 권한) → venv_whisper(최신 huggingface_hub)로 받음
- **TeamUNIVA/qwen3_asr_1.7b_ko_beta 레포에 `chat_template.json`이 없어** qwen-asr 0.0.6 + transformers 4.57.6에서 `apply_chat_template` 실패. 기본 모델(Qwen/Qwen3-ASR-1.7B)의 chat_template.json을 스냅샷 폴더에 복사하고, HF 캐시의 `.no_exist/` 마커를 지운 뒤 `HF_HUB_OFFLINE=1`로 실행하면 됨. (모델 팀에 Discussion으로 알려줄 거리)
- Python 3.10 f-string 안에 백슬래시 불가(`\d`) → 변수로 빼기
- nlptutti `compare_systems`는 시스템 2개 이상 요구 → 같은 hyp를 더미로 넣어 micro 값 사용

## 2026-10-24 재채점 (리뷰 반영)
- **분모 문제**: raw CER 분모(공백 포함)와 kocer 분모(공백 제거)가 달라 비율 비교가 오염됨. 해결: `scripts/score2.py`에서 4단계(raw → 공백 제거 → 공백·부호 제거 → kocer)를 ref·hyp에 동일 적용하고, **가짜 오류 비율은 오류 개수 기준**(E_raw − E_kocer)/E_raw 으로 계산. 단계별 CER도 각자 분모로 병기하되 "ref chars raw / kocer" 열로 분모 차이를 표에 노출.
  - 부작용 확인: 공백만 제거하면 분모가 ~25% 줄어 CER이 오히려 오르는 모델이 있음(SenseVoice itn Zeroth 4.27→4.88, BuzzASR FLEURS 8.38→9.54). 비율로 비교하면 안 되는 이유의 실증.
- **kocer 고유 몫 분리**: 공백·부호 제거 열(= kocer numbers/letters off; nlptutti standard와 소수점 둘째 자리까지 일치)과 kocer 열의 차이가 숫자·약어 몫. 종합 raw 오류의 6~15%, Zeroth에서 8~27%. 띄어쓰기 18~42%, 문장부호 18~28%.
- **순위 검정**: 모델 쌍 paired bootstrap(2000회, 문장 단위, 두 데이터셋 합산). kocer 수준에서 TeamUNIVA < Qwen ≈ whisper < BuzzASR < SenseVoice(itn≈noitn). Qwen–whisper 차이(−0.04%p)만 유의하지 않음.
- **kocer 패치**(kocer_src, 미커밋): counters.py "주"를 양쪽 읽기로, numbers.py 고유어 단독형(하나/둘/셋/넷/스물…) 후보 추가. tests/cases.tsv 8건 추가, 158 통과. "쩜"은 **추가하지 않음** — 구어 표기라 허용 범위를 넓히면 4.4 검수에서 ②가 늘 수 있음. 한계로 명시.
- 100건 검수는 패치된 kocer로 **다시 추출**(seed 20261024, pool 2067 → 중복 제거 후 100).
- BuzzASR 비교는 CV 없이는 결론 내리지 않음. Discussion 글은 CV 추가 후 보냄.

## Common Voice (2026-10-24)
- HF의 mozilla-foundation/common_voice_* 는 2025-10부터 비어 있음(README만). Mozilla Data Collective 전용 배포.
- 사용: "Common Voice Scripted Speech 27.0 - Korean" (MDC id cmu5rwtaf003dnq07e7n3q6tf, CC0, 218 MB, archive cv-corpus-27.0-2026-09-11/ko). test.tsv 579발화, 48.1분, 최대 12.6초. ref = `sentence` 그대로.
- 다운로드: `scripts/get_cv27.py` (MDC_API_KEY 환경변수, 약관 동의 필요; POST는 mozilladatacollective.com 호스트로 — datacollective.mozillafoundation.org는 301로 POST가 GET이 되어 405).
- 참조: 숫자 0%, 영문 0%, 문장부호 87.2%, 평균 26.7자.
- BuzzASR 모델카드는 CV 25 기준이라 test 세트가 다름. 비교 시 각주 필요.

## KsponSpeech 준비 (2026-10-24)
- AI-Hub "한국어 음성"(dataSetSn=123): 내국인만 신청, 재배포 금지, NIA 사업 결과 출처 표기, 국외 반출은 별도 합의. 오디오 16 kHz 16-bit 헤더 없는 PCM, 전사 EUC-KR.
- eval_clean 3,000발화 2.6 h / eval_other 3,000발화 3.8 h.
- 스크립트: `prepare_kspon.py <압축 푼 폴더>` (개수만 출력, 텍스트 출력 안 함), `run_kspon.sh` (7개 설정 일괄, 재시작 가능), `score_kspon.py` (철자/발음 두 참조, 5단계, 참조 선택 민감도, 쌍별 부트스트랩: Kspon 단독 / 공개 3종 합산).
- 공개 원칙: `results/kspon_tables.md`(숫자만)만 공개. `data/kspon_*`, `results/*/kspon_*.jsonl`, `data/kspon_review/` 는 전사가 들어 있으므로 레포·아티팩트에 올리지 않음. 검수가 필요하면 로컬 HTML로.
- 가짜 6발화로 전 과정 테스트 완료 후 삭제.

## 반복 출력 폭주 판정 (2026-10-24)
- **기준**: 문장 단위 kocer 오류 수(S+D+I)가 그 문장의 정규화된 정답 글자 수(hits+S+D)보다 많은 경우, 즉 문장 kocer CER > 1. 삽입이 정답 길이를 넘어야 가능하므로, 사실상 모델이 같은 구절을 반복해 출력이 정답보다 훨씬 길어진 경우만 걸린다.
- **KsponSpeech 6,000발화 결과 (greedy, 반복 억제 없음)**: BuzzASR 19발화(kocer 오류의 6.7%), whisper-large-v3 25발화(4.5%), Qwen3-ASR 기본 5, SenseVoice 5, TeamUNIVA beta 2, 정식판 1. 해당 발화를 빼면 BuzzASR 9.71 → 9.07, whisper 11.55 → 11.04 (철자 정답, clean+other).
- 판정은 텍스트를 보지 않고 숫자로만 했다(AI-Hub 약관). 기준 민감도 확인용으로 "출력 글자 수가 정답의 2배 이상"도 같이 센다(`scripts/decoding_check.py`).
- **검증**: BuzzASR 모델카드 권장 설정(`no_repeat_ngram_size=3, repetition_penalty=1.2`)으로 KsponSpeech와 공개 3종을 다시 돌려 비교한다. 결과 태그 `_buzzasr-korean-cardgen` (밑줄로 시작하는 태그는 score2/score_kspon 본 표에서 제외).
- **재실행 결과 (모델카드 설정, 그 외 조건 동일)**: KsponSpeech 9.71 → 10.14 (+0.43, 95% 구간 [−0.49, +1.02]), Zeroth 3.16 → 3.50, FLEURS 4.72 → 5.30, Common Voice 3.88 → 4.15 (세 공개셋은 구간이 0을 벗어남). 폭주 발화 19 → 17 (기준 B: 10 → 8). 폭주를 빼도 10.04로 greedy(9.07)보다 나쁨. 결론: KsponSpeech 4위는 우리 디코딩 조건 탓이 아니고, 폭주는 디코딩 설정보다 모델의 대화체 반응에 가까움. 표 전체 `results/decoding_check.md`.
