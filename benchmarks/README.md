# Leaderboard re-scoring (2026-10-24)

Six public Korean ASR settings, two public test sets, one set of model outputs, four ways of scoring. Everything needed to recompute the tables is in this folder except the audio.

- `scripts/`: data download, inference (greedy, identical settings for all models), four-level scoring with paired bootstrap. Written for Windows + CUDA; paths in `setup_envs.sh` are the author's machine.
- `results/<model>/<dataset>.jsonl`: every hypothesis exactly as emitted, with the reference. `*.meta.json` has the decoding settings and the full `pip freeze`.
- `results/tables2.md`: all tables (per dataset, pooled, error-count decomposition, ranks, bootstrap matrices). `results/scores2.json` is the raw data behind them.
- `results/fake_review.tsv`: the 100 sampled sentences with raw CER > 0 and kocer CER = 0, with verdicts. **First-pass verdicts were made by an AI assistant and have not yet been re-checked by the author.**
- `results/NOTES.md`: environment, pitfalls, and the two kocer fixes found during the run (shipped in kocer 0.1.3).
- Missing: `results/buzzasr-korean/fleurs.jsonl` could not be published (the model emitted U+FFFD characters); its numbers are in `scores2.json`. Common Voice ko was not run (gated).

Re-score with the installed kocer:

```bash
pip install "kocer[fast]==0.1.3" numpy nlptutti
python scripts/score2.py      # expects data/<dataset>/test.jsonl from scripts/prepare_data.py
```

With kocer 0.1.3 the `kocer` column of every available file reproduces `scores2.json` to two decimals (checked 2026-10-24).

## Leaderboard: the same hypotheses, scored four ways

Same models, same audio, same model outputs. Only the scoring changes. Every normalization step is applied identically to reference and hypothesis.

| level | what is removed / expanded | tool |
|---|---|---|
| raw | nothing; spaces count as characters | `jiwer.cer` / `kocer.cer(normalize=False)` |
| nospace | whitespace | — |
| nospace+punct | whitespace + punctuation (NFC) | `nlptutti.get_cer(rate_mode="standard")` gives the same numbers to 2 decimals |
| kocer | + number candidate sets (`3개`=`세 개`, `2016년`=`이천 십 육 년`) + Latin acronyms | `kocer.cer` |

Test sets: Zeroth-Korean test (457 utt., ~1 h), FLEURS ko_kr test (382 utt., ~1 h, `raw_transcription` as reference). Overall = pooled errors / pooled reference characters over both sets. CER in %.

| Model | raw | nospace | nospace+punct | kocer | rank raw → nospace+punct → kocer |
|---|---|---|---|---|---|
| TeamUNIVA/qwen3_asr_1.7b_ko_beta | 7.79 | 7.51 | 4.94 | **3.35** | 4 → 3 → **1** |
| Qwen/Qwen3-ASR-1.7B | 6.86 | 6.44 | 4.13 | 3.58 | 1 → 1 → 2 |
| openai/whisper-large-v3 | 8.77 | 6.59 | 4.62 | 3.62 | 6 → 2 → 3 |
| BuzzASR/korean | 7.98 | 7.68 | 5.34 | 3.91 | 5 → 6 → 4 |
| FunAudioLLM/SenseVoiceSmall (use_itn=False) | 7.07 | 7.59 | 5.28 | 4.57 | 2 → 4 → 5 |
| FunAudioLLM/SenseVoiceSmall (use_itn=True) | 7.23 | 7.76 | 5.30 | 4.57 | 3 → 5 → 6 |

Do not compare the columns as ratios: the denominator shrinks by ~25% once spaces are removed (49,360 → 37,000 reference characters), which is why a model whose spacing already matches the reference can get a *higher* nospace CER than raw (SenseVoice). The honest view is error **counts**:

| Model | raw errors | spacing | punctuation | numbers / Latin (kocer only) | real errors left | notation share |
|---|---|---|---|---|---|---|
| TeamUNIVA ko | 3,846 | 26% | 26% | 15% | 32% | 68% |
| Qwen3-ASR-1.7B | 3,388 | 28% | 27% | 6% | 39% | 61% |
| whisper-large-v3 | 4,327 | 42% | 18% | 9% | 31% | 69% |
| BuzzASR/korean | 3,938 | 26% | 24% | 13% | 37% | 63% |
| SenseVoice (itn off) | 3,488 | 18% | 26% | 8% | 48% | 52% |
| SenseVoice (itn on) | 3,567 | 18% | 28% | 7% | 47% | 53% |

**What this says.**
1. 52–69% of what raw CER counts as errors on these sets is notation, not recognition. Most of that is spacing and punctuation. Removing them alone (which nlptutti and most Korean papers already do) moves whisper-large-v3 from last to 2nd and SenseVoice from the top to the middle.
2. Numbers and Latin acronyms, the part only kocer handles, are a smaller slice (6–15% of raw errors overall; on Zeroth 8–27% for the digit-emitting models and 0% for SenseVoice, which writes numbers in Hangul) but they still reorder the top: TeamUNIVA goes 3rd → 1st and BuzzASR 6th → 4th. Reason: Zeroth references spell every number in Hangul (`이천 십 육 년`) while these models emit digits (`2016년`); 24–27% of TeamUNIVA's and BuzzASR's raw Zeroth errors are exactly that.
3. Which differences are real? Pairwise paired bootstrap (2,000 sentence resamples, both sets pooled, kocer level): TeamUNIVA < Qwen3-ASR by 0.24 pt [0.08, 0.39]; Qwen3-ASR ≈ whisper-large-v3 (−0.04 [−0.23, +0.15], not significant); whisper < BuzzASR by 0.29 [0.13, 0.46]; BuzzASR < SenseVoice by 0.67 [0.36, 0.94]; the two SenseVoice settings are identical. Rank intervals: TeamUNIVA [1,1], Qwen [2,3], whisper [2,3], BuzzASR [4,4], SenseVoice [5,6]. Full matrices for all levels: `results/tables2.md`.

**Does the normalization hide real errors?** 100 sentences with raw CER > 0 and kocer CER = 0, drawn at random (seed 20261024) from the 1,325 distinct such pairs across all six systems, read side by side: 100 were spacing / punctuation / number-notation differences only, 0 hid a recognition error. One class to be aware of: a spacing difference can create a Korean homograph (`세 배`/`세배`, `정 전 의원`/`정전 의원`); kocer, like every space-removing CER, scores these as 0. Two such cases appeared in an earlier draw with the unpatched scorer; none in this one. Full list: `results/fake_review.tsv`. First-pass verdicts by an AI assistant; author re-check pending.

<details><summary>Setup, caveats, and what is not claimed</summary>

- Decoding identical for all models: language fixed to Korean, task transcribe, **greedy** (num_beams=1, no sampling, no repetition penalty), no prompt, no chunking (all clips ≤ 30 s), 16 kHz. This is deliberately not each model's best-score recipe (BuzzASR's card recommends `no_repeat_ngram_size=3, repetition_penalty=1.2`).
- Hypotheses stored exactly as emitted, including Whisper's leading space and trailing period. SenseVoice output passed through funasr's `rich_transcription_postprocess` (tag removal only). For Korean, SenseVoice emits numbers in Hangul even with `use_itn=True`; the flag only toggles punctuation.
- Whisper / BuzzASR: transformers 5.20.2, fp16, batch 8. Qwen: qwen-asr 0.0.6, transformers 4.57.6, bf16, batch 4, `generation_config.do_sample=False`. SenseVoice: funasr 1.4.16. torch 2.6.0+cu124, RTX 4060 Ti 8 GB, 2026-10-24. No failed or empty outputs; all 839 utterances scored for every model.
- kocer version: 0.1.3 (= 0.1.2 plus two fixes found during this run: counter `주` accepts both readings; standalone native numerals `스물`, `셋`). Colloquial decimal `쩜` is **not** accepted. The scorer was fixed *before* the 100-sentence review was drawn.
- **Common Voice ko is not included** (gated). BuzzASR's card reports its largest gain over whisper-large-v3 on Common Voice (6.01 → 4.24) and near-parity on FLEURS (5.31 vs 5.16). On FLEURS alone we also see near-parity (4.37 vs 4.72 at kocer level). No claim about BuzzASR vs whisper overall is made until Common Voice is added.
- Each test set is ~1 h of audio. Model-to-model gaps under 0.3 pt should be read with the bootstrap intervals above, not the point estimates.
- TeamUNIVA/qwen3_asr_1.7b_ko_beta currently lacks `chat_template.json`; the base model's file was copied in to load it with qwen-asr 0.0.6.

</details>


