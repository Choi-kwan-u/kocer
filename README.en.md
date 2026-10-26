# kocer

[한국어](README.md) · **English**

[![PyPI](https://img.shields.io/pypi/v/kocer)](https://pypi.org/project/kocer/) [![Python](https://img.shields.io/pypi/pyversions/kocer)](https://pypi.org/project/kocer/) [![tests](https://github.com/Choi-kwan-u/kocer/actions/workflows/tests.yml/badge.svg)](https://github.com/Choi-kwan-u/kocer/actions/workflows/tests.yml)

A fair character error rate (CER) for Korean speech recognition. Differences in spacing, punctuation, number notation and Latin acronyms are not counted as errors.

**[Try it in your browser, no install →](https://choi-kwan-u.github.io/kocer/)** Paste references and ASR outputs to see plain CER, kocer CER and where the errors come from. The demo page is in Korean, but the input boxes and numbers work the same.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Choi-kwan-u/kocer/main/docs/breakdown-en-dark.svg">
  <img alt="Stacked bars for 7 public Korean ASR settings, splitting plain CER errors into spacing, punctuation, number/Latin notation and real errors. 46 to 68 percent are notation." src="https://raw.githubusercontent.com/Choi-kwan-u/kocer/main/docs/breakdown-en-light.svg">
</picture>

You get the chart above for your own model in one call. Your existing CER stays as it is; kocer shows where those errors came from.

> **Plain CER** compares the reference and the hypothesis character by character, including spaces and punctuation. This is what [jiwer](https://github.com/jitsi/jiwer)'s `cer()` and Hugging Face `evaluate`'s `cer` compute, and it is the `raw CER` in the output below.

```python
>>> import kocer
>>> print(kocer.breakdown(refs, hyps))      # whisper-large-v3, Zeroth test, 457 utterances
raw CER 8.60%  →  kocer CER 2.93%   (2,191 raw errors, 457 pairs, kocer 0.3.0)
띄어쓰기     1,142   52%  █████████████████████
문장부호       226   10%  ████
숫자·영문      258   12%  █████
진짜 오류      565   26%  ██████████
```

The four rows are spacing, punctuation, number/Latin notation and real errors. They always add up to the raw error count.

## Why it is needed

Korean reads the same digit differently depending on the counter word that follows it. `3개` (three items) is read `세 개` with the native Korean numeral, but `3층` (third floor) is read `삼 층` with the Sino-Korean numeral, and `3시 30분` (3:30) mixes both: `세 시 삼십 분`. Transcripts write these either way. Some references spell numbers out in Hangul, others use digits, and models differ in the same way.

So when the reference says `세 시에 만나` ("see you at three") and the model writes `3시에 만나`, a person would call it correct, but plain CER counts it wrong. Korean tools such as [nlptutti](https://github.com/hyeonsangjeon/computing-Korean-STT-error-rates) remove spacing and punctuation first, but they still count number notation as errors.

This matters most **when comparing models**. If one model writes digits and the other writes Hangul, the winner depends on how the reference happens to be written. You end up comparing number-writing habits instead of recognition.

We checked this directly. Same two models, same outputs; only the number notation in the reference changes:

| Number notation in the reference | Spacing and punctuation removed | kocer |
|---|---|---|
| Digits (`3시`) | new model is better | new model is better |
| Hangul (`세 시`) | new model is **worse** | new model is better |

Even with spacing and punctuation removed, the conclusion flips with the reference. kocer accepts every valid reading, so both references give the same answer.

<details>
<summary>Details</summary>

- Data: 628 utterances containing numbers from the AI-Hub KsponSpeech eval set. This corpus writes numbers both ways, as in `(3시)/(세 시)`, so two references can be built for the same audio.
- Models: [Qwen/Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) and its Korean fine-tune [TeamUNIVA/qwen3_asr_1.7b_ko](https://huggingface.co/TeamUNIVA/qwen3_asr_1.7b_ko).
- Spacing and punctuation removed (nlptutti style): with the digit reference the fine-tune is 8.50 points better; with the Hangul reference it is 4.13 points worse.
- kocer: the fine-tune is 2.34 points better with the digit reference and 2.36 points better with the Hangul reference.
- All four differences have sentence-level paired bootstrap 95% intervals that exclude zero.
- The same happens on AI-Hub telephone speech (408 utterances with numbers). With spacing and punctuation removed, the fine-tune is 6.58 points better with the digit reference and not distinguishable from the base with the Hangul reference (0.47 points). With kocer it is better with both (3.82 and 3.55 points).

See [benchmarks/](benchmarks/README.md) for the full numbers.

</details>

kocer matters most for close models, especially when a new version changes how it writes numbers. When models differ a lot, any metric gives roughly the same ranking. `kocer.compare()` tells you whether a difference is statistically distinguishable.

## Install

```bash
pip install kocer            # pure Python, no dependencies
pip install "kocer[fast]"    # uses rapidfuzz; much faster on long text
```

## Usage

```python
import kocer

kocer.cer("사과 세 개 주세요", "사과 3개 주세요")    # 0.0  ("three apples, please")
kocer.cer(refs, hyps)                                 # lists are pooled over the corpus, like jiwer

r = kocer.measure("세 시 삼십 분", "3시 30분")
r.cer, r.raw_cer                                      # 0.0, 0.625  (normalized, plain)

print(kocer.breakdown(refs, hyps))                    # error breakdown (output above)
print(kocer.compare(refs, {"new": new, "old": old}))  # ranking and 95% intervals for pairwise differences
kocer.cer("유니스트 입학", "UNIST 입학", aliases={"UNIST": "유니스트"})   # acronyms read as words
kocer.cer("(7시)/(일곱 시)에 만나", "7시에 만나")    # 0.0  AI-Hub dual transcripts: both sides count
kocer.cer("b/ 그거+ 그거 *좋아", "그거 그거 좋아", aihub=True)   # 0.0  raw AI-Hub transcripts as-is
```

```bash
kocer ref.txt hyp.txt          # one pair per line: raw CER, kocer CER, breakdown
kocer ref.txt hyp.txt --diff   # color only the wrong characters
kocer ref.txt new.txt old.txt  # two or more hypothesis files: compare models
```

<details>
<summary>Full API</summary>

```python
kocer.wer(ref, hyp)

r = kocer.measure("세 시 삼십 분", "3시 30분")
r.ops         # {'S': 0, 'D': 0, 'I': 0}
r.alignment   # [('H', '세', '세'), ...]
r.chosen_ref  # the reading chosen for the reference
r.chosen_hyp  # '세시 삼십분'

b = kocer.breakdown(refs, hyps)
b.spacing, b.punctuation, b.numbers_letters, b.remaining   # sums to b.raw_errors
b.shares                          # as fractions
b.cer                             # {'raw':…, 'nospace':…, 'nopunct':…, 'kocer':…}

c = kocer.compare(refs, {"A": hyps_a, "B": hyps_b, "C": hyps_c}, n_boot=2000, seed=0)
c.cer                             # CER per system
c.pairs[("A", "B")]               # (CER A − CER B, 95% low, high), sentence-level paired bootstrap
c.significant("A", "B")           # is the difference non-zero?
c.ranks["A"]                      # (best rank, worst rank, probability of rank 1)
print(c)                          # table; uses numpy if installed, pure Python otherwise

kocer.cer("엘지 트윈스", "LG 트윈스")      # 0.0  runs of capitals are spelled out letter by letter
kocer.cer("케이비오 리그", "KBO 리그")      # 0.0
```

</details>

## Compared with existing tools

[jiwer](https://github.com/jitsi/jiwer), [nlptutti](https://github.com/hyeonsangjeon/computing-Korean-STT-error-rates) and kocer all compute CER with the same edit distance. They differ in **what counts as an error**. jiwer counts spacing and punctuation. nlptutti ignores those but counts number and Latin notation. kocer also treats different readings of numbers and acronyms as the same word.

| Reference | Hypothesis | jiwer | nlptutti | kocer |
|---|---|---|---|---|
| 네, 알겠습니다. | 네 알겠습니다 | 0.222 | 0.000 | 0.000 |
| 사과 세 개 주세요 | 사과 3개 주세요 | 0.200 | 0.143 | **0.000** |
| 세 시 삼십 분 | 3시 30분 | 0.625 | 0.600 | **0.000** |
| 이천이십사 년 십이 월 | 2024년 12월 | 0.750 | 0.778 | **0.000** |
| 에이아이 모델 | AI 모델 | 0.571 | 0.667 | **0.000** |
| 사과 세 개 주세요 | 사과 **네** 개 주세요 | 0.100 | 0.143 | 0.143 |
| 세 시 삼십 분 | 3시 **13**분 | 0.625 | 0.600 | 0.400 |

The last two rows are real recognition errors ("four apples", "3:13"), and kocer counts them. jiwer 4.0.0, nlptutti 0.0.0.24, kocer 0.3.0, all with default settings.

If you need entity or keyword error rates, or a quality gate that fails CI below a threshold, nlptutti is the better tool. The two work fine side by side.

<details>
<summary>Feature table</summary>

| | jiwer | nlptutti | kocer |
|---|---|---|---|
| Ignore spacing and punctuation | configurable | default | default |
| Ignore number readings (3개 = 세 개) | no | no | default |
| Ignore acronym readings (AI = 에이아이) | no | no | default, plus user dictionary |
| Plain and normalized CER in one call | no | no | `raw_cer`, `cer` |
| Split errors into spacing, punctuation, numbers, real | no | no | `breakdown()` |
| Compare systems with pairwise intervals | no | yes | `compare()` |
| Quality gate (fail CI below a threshold) | no | yes | no |
| Entity and keyword error rates | no | yes | no |
| Metrics | WER, CER, MER, WIL, WIP | CER, WER, CRR | CER, WER |
| Required dependencies | rapidfuzz, click | jiwer | none |

For `오십 퍼센트` / `50%` ("fifty percent"), jiwer and nlptutti give 1.000 and kocer gives 0.000.

</details>

## Scoring rules

Spacing and punctuation are removed, and numbers and acronyms are scored against the reading that gives the lowest CER. Every step can be turned off, and the plain CER (`raw_cer`) is always returned alongside. Normalization can hide real errors, so report both values.

<details>
<summary>Steps, number candidates, formula</summary>

| Step | Default | Switch | Example |
|---|---|---|---|
| Unicode NFC | on | - | decomposed jamo input |
| Remove punctuation | on | `punct=False` | `네, 알겠습니다.` = `네 알겠습니다` |
| Remove fillers (음, 어, 그) | **off** | `fillers=True` | off by default because "그" is also a real word |
| Acronyms and units | on | `letters=False` | `AI` = `에이아이`, `NASA` = `나사`, `50%` = `50퍼센트` |
| Number candidates | on | `numbers=False` | `3개` = `세 개`, `3층` = `삼 층` |
| AI-Hub dual transcripts | on | `dual=False` | `(7시)/(일곱 시)` = `7시` = `일곱 시` |
| Strip AI-Hub noise tags and marks | **off** | `aihub=True` | removes `b/`, `n/`, `어/`, `+`, `*`; off by default to keep things like `C++` intact |
| Remove spaces | CER only | - | WER keeps spaces |

`normalize=False` returns the same plain CER as jiwer.

**Numbers: a set of candidates, not one answer.** Because the reading depends on the counter word, no single rule produces the right reference. kocer builds candidates for every number, `{digits as written, Sino-Korean reading, native Korean reading, digit-by-digit reading}`, and picks the combination with the lowest CER.

- If the counter word is in the counter dictionary ([counters.py](src/kocer/counters.py)), only its reading is allowed; otherwise both readings are accepted.
- It works in both directions: Hangul in the reference and digits in the hypothesis, or the reverse.
- Phone numbers and years also get the digit-by-digit reading (010 = 공일공, 2024 = 이공이사).
- Native readings cover 1 to 99, in both the attributive form (세, 스무) and the standalone form (셋, 스물). Decimals accept `점` only, not the colloquial `쩜`.
- If there are more than 64 candidate combinations, each number span is optimized separately.

**Formula.** CER = (substitutions + deletions + insertions) / reference characters. Normalization is applied to both sides in the same order, and characters are counted with spaces removed. The denominator is the normalized reference length, so `raw_cer` and `cer` have different denominators. Do not compare them as ratios; use `breakdown()` for error counts. Results are deterministic.

</details>

## Benchmark on public models

Seven public Korean ASR settings were run on Zeroth, FLEURS, Common Voice 27 and KsponSpeech (7,418 utterances in total), and the same outputs were scored at four normalization levels. AI-Hub telephone speech (1,936 utterances) was checked separately.

- On Zeroth, FLEURS and Common Voice (1,418 utterances), **46–68% of what plain CER counts as errors is notation**, mostly spacing and punctuation.
- Where the transcripts give numbers both ways, picking one side as the reference moves CER with spacing and punctuation removed by 2.9–4.8 points per model (telephone set; at most 0.33 points with kocer), and on sentences with numbers it can reverse the direction of a two-model comparison ([table above](#why-it-is-needed)). Averaged over everything, the effect shrinks because most sentences have no numbers.
- To check that normalization does not hide real errors, 100 sentences with plain CER > 0 and kocer CER = 0 were read by hand (14 involved the number step). None hid a recognition error; one was ambiguous, a spacing-induced homograph.

Per-model scores, CER at each level, confidence intervals, decoding settings and scripts are in [benchmarks/](benchmarks/README.md). KsponSpeech and telephone results use the "Korean speech" and "Low-quality telephone network speech recognition" data from AI-Hub, provided by the National Information Society Agency (NIA); under its terms only score tables are published.

<details>
<summary>kocer CER per model</summary>

| Model | Zeroth | FLEURS | Common Voice 27 | KsponSpeech clean / other | Telephone (HR) |
|---|---|---|---|---|---|
| TeamUNIVA/qwen3_asr_1.7b_ko | 2.37 | **4.25** | 6.00 | **6.10 / 6.48** | 5.76 |
| TeamUNIVA/qwen3_asr_1.7b_ko_beta | 2.46 | 4.31 | 6.08 | 6.81 / 7.26 | 9.17 |
| BuzzASR/korean | 3.16 | 4.72 | **3.88** | 10.14 / 9.41 | 5.61 |
| openai/whisper-large-v3 | 2.93 | 4.37 | 5.80 | 11.07 / 11.87 | **5.02** |
| Qwen/Qwen3-ASR-1.7B | 2.91 | 4.31 | 6.61 | 8.70 / 8.59 | 10.76 |
| SenseVoiceSmall (itn on) | **2.40** | 6.95 | 9.68 | 13.28 / 13.82 | 21.30 |
| SenseVoiceSmall (itn off) | 2.41 | 6.91 | 9.72 | 13.09 / 13.72 | 21.55 |

In %, pooled errors / pooled reference characters. KsponSpeech and telephone use the spelling-side reference. Telephone is the HR domain of the AI-Hub low-quality telephone validation split (calls from job seekers and enquiries about corporate training), 1,936 utterances. No model wins everywhere; each is strongest on data close to its training set (BuzzASR on Common Voice, TeamUNIVA apparently on KsponSpeech). On telephone speech whisper-large-v3 was strongest, and BuzzASR, fine-tuned from it on read speech (FLEURS, Common Voice), did not beat it (cause not investigated). All decoding is greedy. Re-running BuzzASR with its model-card settings (repetition penalties) made all five test sets worse ([details](benchmarks/README.md)).

</details>

## Limitations

- Notation differences other than numbers and acronyms (colloquial contractions, spelling as pronounced) are counted as errors.
- Acronym handling could not be validated, because the public test sets contain almost no Latin text. The measured effect comes from numbers.
- The built-in acronym dictionary has 16 entries. Pass acronyms that are read as words through `aliases`.
- Only `%`, `km`, `kg`, `cm`, `mm` and `ml` are converted as unit symbols, and the counter dictionary is incomplete. Pull requests that add cases to [tests/cases.tsv](tests/cases.tsv) are welcome.
- WER counts spacing differences as errors. For Korean, CER is recommended.

## Citing and reporting

Please report the version with any score. Normalization rules change between versions, so the same outputs can score differently. Reporting `raw_cer` as well makes your numbers comparable with other tools.

```
CER 8.60% (raw) / 2.93% (kocer 0.3.0)
```

Use "Cite this repository" on the right side of the repo page to copy a citation ([CITATION.cff](CITATION.cff)).

<details>
<summary>BibTeX, related work</summary>

```bibtex
@software{kocer,
  author  = {Choi, Kwan-u},
  title   = {kocer: fair CER/WER for Korean speech recognition},
  year    = {2026},
  version = {0.3.1},
  url     = {https://github.com/Choi-kwan-u/kocer}
}
```

- [jiwer](https://github.com/jitsi/jiwer): general WER/CER. kocer's `cer()` and `wer()` follow its signatures.
- [nlptutti](https://github.com/hyeonsangjeon/computing-Korean-STT-error-rates): Korean STT evaluation with spacing and punctuation removal, system comparison reports and entity evaluation.
- OIWER in the [Open ASR Leaderboard](https://github.com/huggingface/open_asr_leaderboard): a hypothesis counts as correct if it matches any of several accepted spellings. kocer's number candidates apply the same idea to Korean numerals and counter words.
- "What is lost in Normalization?" (EMNLP 2024): shows that Whisper-style normalization distorts scores for non-English scripts.
- [whisper_normalizer](https://github.com/kurianbenoy/whisper_normalizer): an implementation of the English and basic normalizers from the Whisper paper.

</details>

## License

[MIT](LICENSE)

---

If kocer is useful to you, a ⭐ helps other Korean ASR researchers find it.
