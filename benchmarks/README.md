# Leaderboard re-scoring (2026-10-24)

Six public Korean ASR settings, three public test sets (1,418 utterances), one set of model outputs, four ways of scoring. Everything needed to recompute the tables is in this folder except the audio.

- `scripts/`: data download (`prepare_data.py` for Zeroth/FLEURS, `get_cv27.py` for Common Voice 27 from Mozilla Data Collective), inference (greedy, identical settings for all models), four-level scoring with paired bootstrap (`score2.py`). Written for Windows + CUDA; paths in `setup_envs.sh` are the author's machine.
- `results/<model>/<dataset>.jsonl`: every hypothesis exactly as emitted, with the reference. `*.meta.json` has the decoding settings and the full `pip freeze`.
- `results/tables2.md`: all tables (per dataset, pooled, error-count decomposition, ranks, bootstrap matrices). `results/scores2.json` is the raw data behind them.
- `results/fake_review.tsv`: the 100 sampled sentences with raw CER > 0 and kocer CER = 0. `verdict` is the author's reading (99 notation-only, 0 hidden errors, 1 ambiguous); `claude_first_pass` is the AI assistant's first pass kept for comparison.
- `results/NOTES.md`: environment, pitfalls, and the two kocer fixes found during the run (shipped in kocer 0.1.3).
- Missing: `results/buzzasr-korean/fleurs.jsonl` and `commonvoice.jsonl` could not be published (the model emitted U+FFFD characters); their numbers are in `scores2.json`.

Re-score with the installed kocer:

```bash
pip install "kocer[fast]==0.1.4" numpy nlptutti
python scripts/score2.py      # expects data/<dataset>/test.jsonl from the download scripts
```

With kocer 0.1.4 (same scorer as 0.1.3) the `kocer` column of all 16 available files reproduces `scores2.json` to two decimals (checked 2026-10-24).

## Datasets

All three are public. The jsonl files here contain only the reference transcripts and model outputs, no audio. Reference text is redistributed under each dataset's license with attribution below.

| Dataset | Split | Utterances | Source | License |
|---|---|---|---|---|
| Zeroth-Korean | test | 457 | [kresnik/zeroth_korean](https://huggingface.co/datasets/kresnik/zeroth_korean) (original: [goodatlas/zeroth](https://github.com/goodatlas/zeroth)) | CC BY 4.0 |
| FLEURS ko_kr | test | 382 | [google/fleurs](https://huggingface.co/datasets/google/fleurs); reference = `raw_transcription` | CC BY 4.0 |
| Common Voice Scripted Speech 27.0 Korean | test | 579 | [Mozilla Data Collective](https://mozilladatacollective.com/datasets/cmu5rwtaf003dnq07e7n3q6tf); needs a free account, terms acceptance and `MDC_API_KEY` | CC0 1.0 |

## The tables

Same models, same audio, same model outputs. Only the scoring changes. Every normalization step is applied identically to reference and hypothesis.

| level | what is removed / expanded | tool |
|---|---|---|
| raw | nothing; spaces count as characters | `jiwer.cer` / `kocer.cer(normalize=False)` |
| nospace | whitespace | — |
| nospace+punct | whitespace + punctuation (NFC) | `nlptutti.get_cer(rate_mode="standard")` gives the same numbers to 2 decimals |
| kocer | + number candidate sets (`3개`=`세 개`, `2016년`=`이천 십 육 년`) + Latin acronyms | `kocer.cer` |

Test sets (all public, 1,418 utterances, ~2.9 h): Zeroth-Korean test (457 utt.), FLEURS ko_kr test (382 utt., `raw_transcription` as reference), Common Voice Scripted Speech 27.0 Korean test (579 utt., official Mozilla Data Collective release). CER in %.

### kocer CER per test set

| Model | Zeroth | FLEURS | Common Voice 27 | pooled |
|---|---|---|---|---|
| BuzzASR/korean | 3.16 | 4.72 | **3.88** | **3.90** |
| TeamUNIVA/qwen3_asr_1.7b_ko_beta | 2.46 | **4.31** | 6.08 | 3.99 |
| openai/whisper-large-v3 | 2.93 | 4.37 | 5.80 | 4.13 |
| Qwen/Qwen3-ASR-1.7B | 2.91 | **4.31** | 6.61 | 4.30 |
| FunAudioLLM/SenseVoiceSmall (use_itn=True) | **2.40** | 6.95 | 9.68 | 5.78 |
| FunAudioLLM/SenseVoiceSmall (use_itn=False) | 2.41 | 6.91 | 9.72 | 5.79 |

No model wins everywhere. BuzzASR, fine-tuned on Common Voice and FLEURS training data, is far ahead on Common Voice and behind on Zeroth. SenseVoice is best on Zeroth and last everywhere else. The pooled column depends on the mix of test sets, so read the per-set columns first.

### Pooled CER at each level

| Model | raw | nospace | nospace+punct | kocer | rank raw → nospace+punct → kocer |
|---|---|---|---|---|---|
| BuzzASR/korean | 7.83 | 7.81 | 5.02 | 3.90 | 3 → 3 → **1** |
| TeamUNIVA ko | 7.61 | 7.45 | 5.26 | 3.99 | 2 → 4 → **2** |
| whisper-large-v3 | 9.58 | 7.18 | 4.91 | 4.13 | 6 → 2 → 3 |
| Qwen3-ASR-1.7B | 6.97 | 6.72 | 4.73 | 4.30 | 1 → 1 → 4 |
| SenseVoice (itn on) | 7.98 | 8.43 | 6.36 | 5.78 | 4 → 6 → 5 |
| SenseVoice (itn off) | 8.45 | 9.05 | 6.36 | 5.79 | 5 → 5 → 6 |

Do not compare the columns as ratios: removing spaces shrinks the denominator by ~25% (64,833 → 48,470 reference characters), which is why a model whose spacing already matches the reference can get a *higher* nospace CER than raw. The honest view is error **counts**:

| Model | raw errors | spacing | punctuation | numbers / Latin (kocer only) | real errors left | notation share |
|---|---|---|---|---|---|---|
| BuzzASR/korean | 5,077 | 23% | 29% | 11% | 37% | 63% |
| TeamUNIVA ko | 4,935 | 25% | 24% | 12% | 39% | 61% |
| whisper-large-v3 | 6,210 | 42% | 19% | 6% | 32% | 68% |
| Qwen3-ASR-1.7B | 4,521 | 26% | 23% | 5% | 46% | 54% |
| SenseVoice (itn on) | 5,171 | 19% | 22% | 5% | 54% | 46% |
| SenseVoice (itn off) | 5,479 | 18% | 26% | 5% | 51% | 49% |

**What this says.**
1. 46–68% of what raw CER counts as errors on these sets is notation, not recognition. Most of it is spacing and punctuation. Removing those alone, which nlptutti and many Korean papers already do, moves whisper-large-v3 from last to 2nd.
2. Numbers and Latin acronyms, the part only kocer handles, are 5–12% of raw errors pooled, and nearly all of it comes from **Zeroth**: its references spell every number in Hangul (`이천 십 육 년`) while most models emit digits (`2016년`). There it is 8–27% of raw errors for the digit-emitting models. On FLEURS and Common Voice it is 0–3% for every model except SenseVoice on FLEURS (9–11%). That slice still reorders the top pooled: TeamUNIVA 4th → 2nd and BuzzASR 3rd → 1st.
3. Which pooled differences are real? Pairwise paired bootstrap (2,000 sentence resamples, kocer level): BuzzASR ≈ TeamUNIVA (−0.09 pt [−0.32, +0.13]); both are ahead of Qwen3-ASR (0.40 [0.16, 0.64] and 0.31 [0.15, 0.46]); BuzzASR is ahead of whisper (0.23 [0.06, 0.40]); whisper vs TeamUNIVA and whisper vs Qwen3-ASR are not distinguishable; SenseVoice trails everyone by 1.5–1.9 pt and its two settings are identical. Rank intervals: BuzzASR [1, 2], TeamUNIVA [1, 3], whisper [2, 4], Qwen3-ASR [3, 4], SenseVoice [5, 6]. Full matrices for all levels: `results/tables2.md`.

**Does the normalization hide real errors?** 100 sentences with raw CER > 0 and kocer CER = 0 were drawn at random (seed 20261024) from the Zeroth and FLEURS pool and read side by side by the author: 99 were spacing / punctuation / number-notation differences only, 0 hid a recognition error, 1 was ambiguous (`일 세기 전`/`일세기 전`: "one century ago" vs "the 1st century"). That ambiguous class is a spacing difference that creates a Korean homograph; an earlier draw with the unpatched scorer had two more (`세 배`/`세배`, `정 전 의원`/`정전 의원`). Every space-removing CER scores these as 0; none came from kocer's number candidates. Common Voice was added after the review; its kocer-only share is 0–2%, so its zero-CER sentences are almost all spacing and punctuation. Full list: `results/fake_review.tsv`.

<details><summary>Setup, caveats, and what is not claimed</summary>

- Decoding identical for all models: language fixed to Korean, task transcribe, **greedy** (num_beams=1, no sampling, no repetition penalty), no prompt, no chunking (all clips ≤ 30 s), 16 kHz. This is deliberately not each model's best-score recipe (BuzzASR's card recommends `no_repeat_ngram_size=3, repetition_penalty=1.2`).
- Hypotheses stored exactly as emitted, including Whisper's leading space and trailing period. SenseVoice output passed through funasr's `rich_transcription_postprocess` (tag removal only). For Korean, SenseVoice emits numbers in Hangul even with `use_itn=True`; the flag only toggles punctuation.
- Whisper / BuzzASR: transformers 5.20.2, fp16, batch 8. Qwen: qwen-asr 0.0.6, transformers 4.57.6, bf16, batch 4, `generation_config.do_sample=False`. SenseVoice: funasr 1.4.16. torch 2.6.0+cu124, RTX 4060 Ti 8 GB, 2026-10-24. No failed or empty outputs; all 1,418 utterances scored for every model.
- kocer version: 0.1.3 (= 0.1.2 plus two fixes found during this run: counter `주` accepts both readings; standalone native numerals `스물`, `셋`). Colloquial decimal `쩜` is **not** accepted. The scorer was fixed *before* the review sample was drawn.
- **Common Voice.** Hugging Face copies of Common Voice are empty since October 2025; the data came from Mozilla Data Collective ("Common Voice Scripted Speech 27.0 - Korean", CC0). BuzzASR's card reports Common Voice **25**, so the test set is not identical. Overlap check: none of the 579 CV27 test sentences, clips or speakers appear in the CV17 train split; 195 are the CV17 test set carried forward. CV keeps its test split stable across releases, so the BuzzASR lead on CV reads as in-domain training data, not test leakage. We cannot check CV25 train directly.
- BuzzASR's card: CV 4.24, FLEURS 5.16 ("normalized CER"). Ours at the spacing+punctuation level: CV 3.98, FLEURS 4.79. Same picture: a large CV gain, near-parity with whisper on FLEURS.
- Each test set is 0.8–1.1 h of audio. Gaps under ~0.3 pt should be read with the bootstrap intervals, not the point estimates.
- TeamUNIVA/qwen3_asr_1.7b_ko_beta currently lacks `chat_template.json`; the base model's file was copied in to load it with qwen-asr 0.0.6.

</details>


