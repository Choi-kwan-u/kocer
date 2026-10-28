# Public Korean ASR models: same outputs, four scorings (run 2026-10-24, scored with kocer 0.4.0 on 2026-10-26)

Seven public Korean ASR settings, three public test sets (1,418 utterances) plus KsponSpeech eval (6,000 utterances, numbers only) and AI-Hub telephone speech (1,936 utterances, numbers only), one set of model outputs, four ways of scoring. Everything needed to recompute the tables is in this folder except the audio.

Model names used here: **Qwen3-ASR base** = [Qwen/Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B); **TeamUNIVA ko beta** = [TeamUNIVA/qwen3_asr_1.7b_ko_beta](https://huggingface.co/TeamUNIVA/qwen3_asr_1.7b_ko_beta), a Korean fine-tune of the base (Aug 2026); **TeamUNIVA ko** = [TeamUNIVA/qwen3_asr_1.7b_ko](https://huggingface.co/TeamUNIVA/qwen3_asr_1.7b_ko), its successor trained further from the beta (Oct 2026). Result folders: `qwen3-asr-1.7b` = base, `qwen3-asr-1.7b-ko-univa` = TeamUNIVA ko beta, `qwen3-asr-1.7b-ko-univa-release` = TeamUNIVA ko, `_buzzasr-korean-cardgen` = BuzzASR with its model-card decoding settings.

- `scripts/`: data download (`prepare_data.py` for Zeroth/FLEURS, `get_cv27.py` for Common Voice 27 from Mozilla Data Collective), inference (greedy, identical settings for all models), four-level scoring with paired bootstrap (`score2.py`). Written for Windows + CUDA; paths in `setup_envs.sh` are the author's machine.
- `results/<model>/<dataset>.jsonl`: every hypothesis exactly as emitted, with the reference. `*.meta.json` has the decoding settings and the full `pip freeze`.
- `results/tables2.md`: all tables (per dataset, pooled, error-count decomposition, ranks, bootstrap matrices). `results/scores2.json` is the raw data behind them.
- `results/fake_review.tsv`: the 100 sampled sentences with raw CER > 0 and kocer CER = 0. `verdict` is the author's reading (99 notation-only, 0 hidden errors, 1 ambiguous); `claude_first_pass` is the AI assistant's first pass kept for comparison.
- `results/NOTES.md`: environment, pitfalls, and the two kocer fixes found during the run (shipped in kocer 0.1.3).
- `results/univa_compare.md`: Qwen3-ASR base → TeamUNIVA ko beta → TeamUNIVA ko under the model card's normalization (punctuation removed, case-folded) and kocer, the number-writing habit, and paired bootstrap between versions (`scripts/compare_univa.py`).
- Two BuzzASR files (`fleurs.jsonl`, `commonvoice.jsonl`) contain U+FFFD characters exactly as the model emitted them.

Re-score with the installed kocer:

```bash
pip install "kocer[fast]==0.4.1" numpy nlptutti
python scripts/score2.py      # expects data/<dataset>/test.jsonl from the download scripts
```

All tables here are scored with **kocer 0.4.0**, which changed the scoring rules (reference-only denominator, raw CER strips outer whitespace like jiwer, more notation candidates, digit-wise readings restricted). The same outputs scored with 0.3.0 are compared line by line in `results/before_after_040.md`: kocer-level CER moves by at most 0.4 pt (BuzzASR on FLEURS), raw CER drops for whisper-large-v3 (leading spaces no longer count), and no rank changes except whisper/TeamUNIVA beta swapping 3rd/4th on FLEURS. With kocer 0.1.5–0.3.0 the tables were reproducible exactly from the same files; from 0.4.0 on use `kocer==0.4.x`. Since 0.3.0 the pairwise bootstrap tables can be reproduced with `kocer.compare(refs, {name: hyps, ...})`; on the pooled public sets it gives the same differences and intervals as `scripts/score2.py` (same seed, numpy installed).

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
| BuzzASR/korean | 3.10 | 4.31 | **3.88** | **3.72** |
| TeamUNIVA/qwen3_asr_1.7b_ko | 2.34 | **4.19** | 6.00 | 3.89 |
| TeamUNIVA/qwen3_asr_1.7b_ko_beta | 2.44 | 4.25 | 6.08 | 3.96 |
| openai/whisper-large-v3 | 2.90 | 4.25 | 5.80 | 4.08 |
| Qwen/Qwen3-ASR-1.7B | 2.90 | 4.25 | 6.61 | 4.27 |
| FunAudioLLM/SenseVoiceSmall (use_itn=True) | **2.40** | 6.83 | 9.68 | 5.74 |
| FunAudioLLM/SenseVoiceSmall (use_itn=False) | 2.41 | 6.79 | 9.72 | 5.74 |

No model wins everywhere. BuzzASR, fine-tuned on Common Voice and FLEURS training data, is far ahead on Common Voice and behind on Zeroth. SenseVoice is best on Zeroth and last everywhere else. The pooled column depends on the mix of test sets, so read the per-set columns first.

### Pooled CER at each level

| Model | raw | nospace | nospace+punct | kocer | rank raw → nospace+punct → kocer |
|---|---|---|---|---|---|
| BuzzASR/korean | 7.83 | 7.81 | 5.02 | 3.72 | 5 → 3 → **1** |
| TeamUNIVA ko | 7.43 | 7.24 | 5.20 | 3.89 | 2 → 4 → **2** |
| TeamUNIVA ko beta | 7.61 | 7.45 | 5.26 | 3.96 | 4 → 5 → 3 |
| whisper-large-v3 | 7.48 | 7.18 | 4.91 | 4.08 | 3 → 2 → 4 |
| Qwen3-ASR-1.7B | 6.97 | 6.72 | 4.73 | 4.27 | 1 → 1 → 5 |
| SenseVoice (itn on) | 7.98 | 8.43 | 6.36 | 5.74 | 6 → 7 → 6 |
| SenseVoice (itn off) | 8.45 | 9.05 | 6.36 | 5.74 | 7 → 6 → 7 |

Do not compare the columns as ratios: removing spaces shrinks the denominator by ~25% (64,833 → 48,453 reference characters), which is why a model whose spacing already matches the reference can get a *higher* nospace CER than raw. The honest view is error **counts**:

| Model | raw errors | spacing | punctuation | numbers / Latin (kocer only) | real errors left | notation share |
|---|---|---|---|---|---|---|
| BuzzASR/korean | 5,076 | 23% | 29% | 12% | 36% | 64% |
| TeamUNIVA ko | 4,816 | 25% | 23% | 13% | 39% | 61% |
| TeamUNIVA ko beta | 4,935 | 25% | 24% | 13% | 39% | 61% |
| whisper-large-v3 | 4,849 | 26% | 25% | 8% | 41% | 59% |
| Qwen3-ASR-1.7B | 4,521 | 26% | 23% | 5% | 46% | 54% |
| SenseVoice (itn on) | 5,171 | 19% | 22% | 6% | 54% | 46% |
| SenseVoice (itn off) | 5,479 | 18% | 26% | 5% | 51% | 49% |

**What this says.**
1. 46–64% of what raw CER counts as errors on these sets is notation, not recognition. Most of it is spacing and punctuation. Removing those alone, which nlptutti and many Korean papers already do, moves whisper-large-v3 from 3rd to 2nd and BuzzASR from 5th to 3rd. (Before 0.4.0 raw CER also counted Whisper's leading space on every sentence, which put it last; jiwer never counted it, and now neither does kocer.)
2. Numbers and Latin acronyms, the part only kocer handles, are 5–13% of raw errors pooled, and nearly all of it comes from **Zeroth**: its references spell every number in Hangul (`이천 십 육 년`) while most models emit digits (`2016년`). There it is 8–27% of raw errors for the digit-emitting models. On FLEURS and Common Voice it is 0–4% for every model except whisper-large-v3 (8%) and SenseVoice (10–12%) on FLEURS. That slice still reorders the top pooled: from the nospace+punct level to kocer, TeamUNIVA ko 4th → 2nd, TeamUNIVA ko beta 5th → 3rd, BuzzASR 3rd → 1st.
3. Which pooled differences are real? Pairwise paired bootstrap (2,000 sentence resamples, kocer level): BuzzASR and TeamUNIVA ko are not distinguishable (BuzzASR − TeamUNIVA ko −0.16 pt [−0.37, +0.04]), nor are TeamUNIVA ko and its beta (−0.08 [−0.20, +0.05]); BuzzASR is ahead of the beta (−0.24 [−0.45, −0.03]); all three are ahead of the Qwen3-ASR base (TeamUNIVA ko −0.39 [−0.56, −0.21]); BuzzASR and TeamUNIVA ko are ahead of whisper (−0.35 [−0.50, −0.21], −0.19 [−0.37, −0.01]); whisper vs beta (+0.12 [−0.07, +0.30]) and whisper vs Qwen3-ASR (−0.19 [−0.40, +0.00]) are not distinguishable; SenseVoice trails everyone by 1.5–2.0 pt and its two settings are identical. Rank intervals: BuzzASR [1, 2], TeamUNIVA ko [1, 3], TeamUNIVA ko beta [2, 4], whisper [3, 5], Qwen3-ASR [4, 5], SenseVoice [6, 7].
4. TeamUNIVA ko beta → TeamUNIVA ko: the number-writing habit did not change (share of outputs with a digit: Zeroth 31.7% → 31.3%, FLEURS 23.8% → 25.4%, Common Voice 2.1% → 1.9%; base was 8.5% on Zeroth). Under the model card's own normalization (punctuation removed, case-folded) with a single public reference, both fine-tunes score *worse* than the base on Zeroth; with number readings handled, both are better. The card avoids this with hand-made TN/ITN dual references. Details: `results/univa_compare.md`. Full matrices for all levels: `results/tables2.md`.

**Does the normalization hide real errors?** 100 sentences with raw CER > 0 and kocer CER = 0 were drawn at random (seed 20261024) from the Zeroth and FLEURS pool and read side by side by the author: 99 were spacing / punctuation / number-notation differences only, 0 hid a recognition error, 1 was ambiguous (`일 세기 전`/`일세기 전`: "one century ago" vs "the 1st century"). That ambiguous class is a spacing difference that creates a Korean homograph; an earlier draw with the unpatched scorer had two more (`세 배`/`세배`, `정 전 의원`/`정전 의원`). Every space-removing CER scores these as 0; none came from kocer's number candidates. Common Voice and TeamUNIVA ko were added after the review and are not in the sample: Common Voice's kocer-only share is 0–2%, so its zero-CER sentences are almost all spacing and punctuation, and TeamUNIVA ko writes numbers the same way as its beta, which was in the pool. Full list: `results/fake_review.tsv`. All 100 still score 0 under kocer 0.4.0. Because 0.4.0 widened the number and Latin candidates, a second sample was drawn for it: 100 sentences where only the number/Latin step makes the sentence correct (nospace+punct errors > 0, kocer errors = 0), from a pool of 282 over the three public sets, seed 20261026 (`scripts/sample_number_review.py` → `results/number_review.tsv`, with the candidates kocer actually chose; `results/number_review.html` for reading). Verdicts (author, 2026-10-26): 99 notation-only, 0 hidden recognition errors, 1 ambiguous, and that one is the same spacing homograph as before (`일 세기 전`/`1세기 전`, "a century ago" vs "before the 1st century"), which every space-removing CER also scores as 0; it did not come from a number candidate. Sample: Zeroth 69, FLEURS 27, Common Voice 4.

## KsponSpeech (AI-Hub; data and per-sentence outputs not redistributed)

KsponSpeech eval_clean + eval_other: 6,000 utterances, 6.4 h of conversational speech. Its transcripts give some spans twice, spelling and pronunciation, e.g. `(3시)/(세 시)` (1,236 utterances; in 1,110 the two references differ, 452 of those without any digit or Latin letter). Papers pick one side or the other. We scored the same outputs against both. Full numbers: `results/kspon_tables.md`.

| Model | kocer CER, spelling ref (clean / other) | spelling → pronunciation ref, nospace+punct | same, kocer |
|---|---|---|---|
| TeamUNIVA/qwen3_asr_1.7b_ko | **6.09 / 6.46** | +0.85 | −0.18 |
| TeamUNIVA/qwen3_asr_1.7b_ko_beta | 6.80 / 7.24 | +0.20 | −0.35 |
| Qwen/Qwen3-ASR-1.7B | 8.69 / 8.58 | −0.77 | −0.03 |
| BuzzASR/korean | 10.07 / 9.30 | +0.53 | −0.11 |
| openai/whisper-large-v3 | 11.06 / 11.86 | +0.66 | +0.06 |
| SenseVoiceSmall (itn on / off) | 13.28 / 13.79, 13.09 / 13.69 | +0.20 / +0.19 | −0.17 / −0.17 |

**On the 628 utterances whose spelling reference contains a digit**, the same comparison (TeamUNIVA ko minus Qwen3-ASR base, negative = TeamUNIVA ko better) flips direction under the usual normalization and stays put under kocer:

| reference side | nospace+punct | kocer |
|---|---|---|
| spelling (`3시`) | −8.50 pt [−9.32, −7.70] | −2.32 pt [−2.79, −1.88] |
| pronunciation (`세 시`) | **+4.13 pt** [+3.40, +4.91] | −2.41 pt [−2.86, −1.96] |

With the pronunciation reference and nospace+punct scoring the Qwen3-ASR base ranks 1st and TeamUNIVA ko 3rd; with kocer TeamUNIVA ko is 1st and the base 3rd. Zeroth shows the same pattern on its 152 utterances where any system wrote a digit (beta minus base: +5.49 pt vs −0.50 pt, both CIs exclude 0). Full tables: `results/number_subset.md` (`scripts/number_subset.py`). Over all 6,000 KsponSpeech utterances the effect is diluted by the many sentences without numbers:

1. With spacing and punctuation removed, the choice of reference side alone moves a model's CER by −0.77 to +0.85 pt, in opposite directions for digit-writing models and for the base Qwen model, which writes numbers in Hangul. With kocer the range is −0.35 to +0.06 pt; the remainder comes from the 452 non-numeric dual spellings, which kocer does not handle.
2. Model gaps here are large (at least 0.75 pt between neighbours, except the two SenseVoice settings at 0.14 pt), so the reference choice did not change any rank. Every pair is separated by the paired bootstrap (2,000 resamples).
3. The kocer-only share (numbers and Latin) is 1–6% of raw errors; spacing and punctuation are 44–51%.
4. TeamUNIVA likely trained on KsponSpeech (its largest reported gain). BuzzASR and whisper-large-v3 have 19 and 25 utterances with more kocer errors than reference characters (6.8% and 4.5% of their kocer errors); ranks are unchanged without them. **Criterion:** sentence kocer error count > normalized reference length (sentence kocer CER > 1). A second criterion, hypothesis at least twice as long as the reference (spaces removed), flags 10 and 14. **What they look like** (`scripts/runaway_shape.py`, numbers only, no transcript text read): only 2 of BuzzASR's 19 (and 2 of whisper's 25) are genuine runaway repeats, 100–440 characters of one short unit looped; those 2 hold 84% of the errors in BuzzASR's 19. The other 17 are very short utterances (3–7 reference characters, median 1.7 s) with garbled output of about the same length: 58% carry an overlapping-speech tag (`o/`) and 37% a laughter tag (`l/`) in the raw transcript, against 9% and 5% over all 6,000 (whisper: 52% and 28%). So "runaway" overstates it: the model loops on 2 utterances and mis-hears short laughter or overlapped speech on the rest.
5. **Is BuzzASR's 4th place an artefact of our decoding?** No. Re-running BuzzASR with its model card's settings (`no_repeat_ngram_size=3, repetition_penalty=1.2`, everything else identical) made it *worse* on every set. It did stop both genuine loops (that is the whole 19 → 17 drop below); the 17 short mis-hearings stay:

| BuzzASR kocer CER | KsponSpeech | Zeroth | FLEURS | Common Voice 27 | Telephone (HR) |
|---|---|---|---|---|---|
| greedy, no repetition penalty (main tables) | **9.62** | **3.10** | **4.31** | **3.88** | **5.36** |
| model-card settings | 10.05 | 3.43 | 4.90 | 4.15 | 6.26 |
| card − greedy, 95% CI | +0.43 [−0.49, +1.02] | +0.34 [+0.21, +0.46] | +0.59 [+0.39, +0.78] | +0.27 [+0.13, +0.42] | +0.90 [+0.78, +1.02] |
| runaway utterances (greedy → card) | 19 → 17 | 0 → 0 | 0 → 0 | 0 → 0 | 0 → 0 |

   BuzzASR stays 4th on KsponSpeech and 1st on Common Voice either way. Details: `results/decoding_check.md` (`scripts/decoding_check.py`); public-set outputs with the card settings are in `results/_buzzasr-korean-cardgen/`. The telephone column is from the section below.
6. Pooled with the three public sets (7,418 utterances, KsponSpeech dominating), every pair is separated and the order is TeamUNIVA ko, TeamUNIVA ko beta, Qwen3-ASR base, BuzzASR, whisper, SenseVoice. This order reflects the KsponSpeech share of the pool; read the per-set tables first.

**Raw AI-Hub transcripts, no cleaning (since kocer 0.2.0).** kocer reads the dual notation `(3시)/(세 시)` and accepts either side span by span, and `aihub=True` strips the noise tags (`b/`, `n/`, ...), filler slashes, `+` and `*`. Feeding the original `.trn` text straight in:

| Model | kocer, spelling ref | kocer, pronunciation ref | kocer, raw transcript (`aihub=True`) |
|---|---|---|---|
| TeamUNIVA/qwen3_asr_1.7b_ko | 6.31 | 6.12 | 5.79 |
| TeamUNIVA/qwen3_asr_1.7b_ko_beta | 7.06 | 6.71 | 6.45 |
| Qwen/Qwen3-ASR-1.7B | 8.62 | 8.60 | 8.15 |
| BuzzASR/korean | 9.62 | 9.51 | 9.10 |
| openai/whisper-large-v3 | 11.53 | 11.59 | 11.01 |
| SenseVoiceSmall (itn off) | 13.44 | 13.28 | 12.92 |

The raw-transcript score is lower than either single side because each utterance gets credit for whichever written form matches; no utterance has more errors than with the better of the two cleaned references (checked on all 6,000 for six systems, again with 0.4.0: `results/kspon_raw_transcript.md`). No need to pick a side or clean the transcripts yourself.

This work uses the "Korean speech" (한국어 음성) dataset provided by the National Information Society Agency (NIA) through AI-Hub. AI-Hub terms forbid redistribution, so only aggregate numbers are published here. To reproduce, apply for the dataset on AI-Hub (Korean residents), extract the eval audio and scripts, then run `scripts/prepare_kspon.py <folder>`, `scripts/run_kspon.sh`, `scripts/score_kspon.py`. The scripts print counts only, never transcript text.

## Telephone speech (AI-Hub; data and per-sentence outputs not redistributed)

AI-Hub "Low-quality telephone network speech recognition data" (저음질 전화망 음성인식 데이터), **validation** split, HR domain (D03: calls from job applicants and job seekers, and enquiries about corporate training): 1,936 utterances, 3.6 h, 85 calls. The audio is 8 kHz, upsampled to 16 kHz, and no clip is longer than 30 s. Decoding is the same as everywhere else (greedy). The transcripts use the same dual notation as KsponSpeech: in 563 utterances the spelling and pronunciation references differ. Numbers are twice as common as in KsponSpeech: 408 of 1,936 utterances (21%) have a digit in the spelling reference, against 628 of 6,000 (10%). Full numbers: `results/tel_hr_tables.md`.

| Model | kocer, spelling ref | nospace+punct, spelling ref | raw, spelling ref | spelling → pronunciation ref, nospace+punct | same, kocer | kocer, raw transcript (`aihub=True`) |
|---|---|---|---|---|---|---|
| openai/whisper-large-v3 | **5.02** | **5.44** | **5.92** | +4.81 | +0.03 | **4.95** |
| BuzzASR/korean | 5.36 | 5.97 | 6.38 | +4.65 | +0.04 | 5.29 |
| TeamUNIVA/qwen3_asr_1.7b_ko | 5.75 | 6.26 | 6.73 | +4.52 | +0.00 | 5.68 |
| TeamUNIVA/qwen3_asr_1.7b_ko_beta | 9.12 | 9.83 | 10.64 | +4.03 | −0.04 | 9.02 |
| Qwen/Qwen3-ASR-1.7B | 10.75 | 12.01 | 12.96 | +2.92 | −0.04 | 10.66 |
| SenseVoiceSmall (itn on / off) | 21.33 / 21.53 | 21.66 / 21.86 | 23.32 / 24.57 | +3.18 / +3.15 | −0.02 / +0.02 | 21.25 / 21.45 |

1. **Reference choice.** With spacing and punctuation removed, choosing the pronunciation side instead of the spelling side raises every model's CER by 2.9–4.8 pt. With kocer the shift is at most 0.04 pt.
2. **The 408 utterances whose spelling reference contains a digit** (TeamUNIVA ko minus Qwen3-ASR base, negative = TeamUNIVA ko better):

   | reference side | nospace+punct | kocer |
   |---|---|---|
   | spelling | −6.58 pt [−7.46, −5.73] | −3.79 pt [−4.34, −3.25] |
   | pronunciation | −0.47 pt [−1.30, +0.43], not separated | −3.66 pt [−4.21, −3.12] |

   With conventional scoring, the reference side decides whether the fine-tune is 6.6 pt better or not distinguishable from the base. kocer gives about the same answer with either side. This is the KsponSpeech pattern again, on a second dataset.
3. **Ranks** are the same at every level and with every reference. whisper-large-v3 is ahead of everyone, and every pair is separated (paired bootstrap, 2,000 resamples; BuzzASR − TeamUNIVA ko −0.39 pt [−0.67, −0.14]).
4. **Runaway outputs** (criterion in KsponSpeech item 4): 0 for BuzzASR and TeamUNIVA ko, 1 for whisper, the Qwen3-ASR base and each SenseVoice setting, 2 for the beta. BuzzASR with its model-card settings: 6.26 (+0.90 pt [+0.78, +1.02] against greedy), still no runaways.
5. One domain only. The dataset has other domains.

This work uses the "Low-quality telephone network speech recognition" (저음질 전화망 음성인식) dataset provided by the National Information Society Agency (NIA) through AI-Hub. Only aggregate numbers are published here. To reproduce: download `VL_D03.zip` and `VS_D03.zip` from the validation split, then run `scripts/prepare_tel.py VL_D03.zip VS_D03.zip tel_hr`, `scripts/run_tel.sh`, and `scripts/score_tel.py tel_hr`.

<details><summary>Setup, caveats, and what is not claimed</summary>

- Decoding identical for all models: language fixed to Korean, task transcribe, **greedy** (num_beams=1, no sampling, no repetition penalty), no prompt, no chunking (all clips ≤ 30 s), 16 kHz. This is deliberately not each model's best-score recipe. BuzzASR's card recommends `no_repeat_ngram_size=3, repetition_penalty=1.2`; we checked it and it scores worse than greedy on all five sets (KsponSpeech item 5).
- Hypotheses stored exactly as emitted, including Whisper's leading space and trailing period (since kocer 0.4.0 the raw level strips outer whitespace, as jiwer does, so that space no longer counts). SenseVoice output passed through funasr's `rich_transcription_postprocess` (tag removal only). For Korean, `use_itn` hardly changes how SenseVoice writes numbers. Outputs containing a digit, with the flag on / off: Zeroth 0 / 0, FLEURS 32 / 32, Common Voice 12 / 11, KsponSpeech 435 / 430, telephone 410 / 408.
- Whisper / BuzzASR: transformers 5.20.2, fp16, batch 8. Qwen: qwen-asr 0.0.6, transformers 4.57.6, bf16, batch 4, `generation_config.do_sample=False`. SenseVoice: funasr 1.4.16. torch 2.6.0+cu124, RTX 4060 Ti 8 GB, 2026-10-24. No failed or empty outputs; all 1,418 utterances scored for every model.
- kocer version: every table is scored with 0.4.0 (2026-10-26). The run itself used 0.1.3 (= 0.1.2 plus two fixes found during it: counter `주` accepts both readings; standalone native numerals `스물`, `셋`), and the 0.3.0 → 0.4.0 differences are listed in `results/before_after_040.md`. Colloquial decimal `쩜` is **not** accepted. The 100-sentence review sample was drawn after the 0.1.3 fixes.
- **Common Voice.** Hugging Face copies of Common Voice are empty since October 2025; the data came from Mozilla Data Collective ("Common Voice Scripted Speech 27.0 - Korean", CC0). BuzzASR's card reports Common Voice **25**, so the test set is not identical. Overlap check: none of the 579 CV27 test sentences, clips or speakers appear in the CV17 train split; 195 are the CV17 test set carried forward. CV keeps its test split stable across releases, so the BuzzASR lead on CV reads as in-domain training data, not test leakage. We cannot check CV25 train directly.
- BuzzASR's card: CV 4.24, FLEURS 5.16 ("normalized CER"). Ours at the spacing+punctuation level: CV 3.98, FLEURS 4.79. Same picture: a large CV gain, near-parity with whisper on FLEURS.
- Each test set is 0.8–1.1 h of audio. Gaps under ~0.3 pt should be read with the bootstrap intervals, not the point estimates.
- TeamUNIVA/qwen3_asr_1.7b_ko_beta lacks `chat_template.json`; the base model's file was copied in to load it with qwen-asr 0.0.6. TeamUNIVA/qwen3_asr_1.7b_ko loads as-is and was run in the same environment as the base and beta.
- The TeamUNIVA cards report much lower CER (e.g. FLEURS 1.26%) on hand-corrected references with 106 records removed and best-of-TN/ITN scoring. Our references are the public transcripts as-is, so absolute values are not comparable; only the order between models and how it moves with normalization are.

</details>


