# BuzzASR/korean: greedy vs model-card settings vs beam search

Scores are **kocer 0.5.0** (0.5.1–0.5.3 give identical scores). Same audio, same prompts, same 16 kHz input and 440-token limit for all three runs; only the decoding settings differ.

- **greedy**: `num_beams=1`, no sampling, no repetition penalty (the setting used in the main tables).
- **card**: the model card's recommendation, `no_repeat_ngram_size=3, repetition_penalty=1.2`.
- **beam 5**: `num_beams=5`, no repetition penalty.

KsponSpeech and telephone are AI-Hub sets: only aggregate numbers and utterance IDs appear here, no transcript text. KsponSpeech and telephone use the spelling-side reference.

## kocer CER (%) on six sets

| decoding | Zeroth (457) | FLEURS (382) | Common Voice 27 (579) | Telephone HR (1,936) | KsponSpeech clean (3,000) | KsponSpeech other (3,000) |
|---|---|---|---|---|---|---|
| greedy | 3.08 | 4.28 | 3.88 | 5.31 | 10.06 | 9.29 |
| card | 3.43 | 4.85 | 4.15 | 6.21 | 10.02 | 10.05 |
| beam 5 | **2.79** | **4.19** | **3.63** | **4.99** | **9.64** | **8.89** |

## Paired differences against greedy

Sentence-level paired bootstrap, 2,000 resamples, seed 0, 95% interval (`kocer.compare`). `*` = interval excludes 0.

| set | beam 5 − greedy | card − greedy |
|---|---|---|
| Zeroth | −0.29 [−0.72, −0.02] * | +0.35 [+0.23, +0.48] * |
| FLEURS | −0.08 [−0.21, −0.01] * | +0.57 [+0.34, +0.78] * |
| Common Voice 27 | −0.24 [−0.41, −0.08] * | +0.27 [+0.13, +0.42] * |
| Telephone HR | −0.32 [−0.42, −0.23] * | +0.90 [+0.78, +1.02] * |
| KsponSpeech clean | −0.42 [−2.74, +1.39] | −0.04 [−1.99, +0.97] |
| KsponSpeech other | −0.41 [−1.18, +0.19] | +0.76 [+0.11, +1.15] * |

Beam 5 is lower than greedy on all six sets; the difference excludes 0 on the read and telephone sets but not on the two KsponSpeech halves, where a few long bad outputs make the intervals wide. The card settings are higher than greedy everywhere except KsponSpeech clean (a tie). The greedy-over-card result also holds on spacing + punctuation CER on all sets, so it is not a normalization artefact (`decoding_check.md`).

## The two KsponSpeech repetition loops

Under greedy decoding, two KsponSpeech utterances are genuine repetition loops (one character repeated until the generation limit or far past the reference). Both the card settings and beam 5 fix them; beam 5 does it without the CER cost elsewhere.

| utterance | reference (kocer chars) | greedy output chars / CER | card output chars / CER | beam 5 output chars / CER |
|---|---|---|---|---|
| KsponSpeech_E00521 (eval_clean, 12.2 s) | 52 | 440 / 8.40 | 55 / 0.02 | 47 / 0.10 |
| KsponSpeech_E03096 (eval_other, 10.1 s) | 48 | 241 / 4.33 | 45 / 0.19 | 46 / 0.10 |

Utterances with more kocer errors than reference characters (the "runaway" flag used in `README.md`), KsponSpeech clean + other: greedy 19, card 17, beam 5 25. The 17 that remain under the card settings, and the extra ones under beam 5, are short mis-heard clips (3–7 reference characters), not loops; see `README.md` item 4 for their shape.

## Decoding cost

One RTX 4060 Ti (8 GB), fp16, 100 FLEURS utterances, wall-clock per utterance:

| decoding | batch 1 | batch 8 |
|---|---|---|
| greedy | 1.22 s | 0.30 s |
| card | 1.13 s | — |
| beam 5 | 1.49 s | did not fit in 8 GB |

Beam 5 costs 1.22× greedy at the same batch size. It could not be batched on this GPU (the cross-attention cache is roughly 250 MB per beam), so against batched greedy it was about 5× slower here; on a larger GPU the gap shrinks.

## Files

- Public-set outputs: `buzzasr-korean/` (greedy), `_buzzasr-korean-cardgen/` (card), `_buzzasr-korean-beam5/` (beam 5). Each `*.meta.json` has the exact generation arguments and `pip freeze`.
- Card vs greedy with runaway counts per set: `decoding_check.md` (`scripts/decoding_check.py`).
