# Re-scoring the same outputs: kocer 0.3.0 → 0.4.0

Nothing was re-run; only the scorer changed. Rule changes: fixed denominator (reference-only), raw CER strips outer whitespace (= jiwer), unit symbols / time / currency / temperature / minus as candidates, Latin case-folding and letter variants, digit-wise reading restricted, NFKC, more AI-Hub tags, WER without number normalization.

## Public sets: CER % per level (before → after)

| model | set | raw | nospace | nospace+punct | kocer | notation share of raw |
|---|---|---|---|---|---|---|
| TeamUNIVA ko | zeroth | 8.89 → 8.89 | 8.01 → 8.01 | 5.36 → 5.36 | 2.37 → 2.34 | 80% → 80% |
| TeamUNIVA ko | fleurs | 6.25 → 6.25 | 6.61 → 6.61 | 4.39 → 4.39 | 4.25 → 4.19 | 50% → 50% |
| TeamUNIVA ko | commonvoice | 6.85 → 6.85 | 7.00 → 7.00 | 6.18 → 6.18 | 6.00 → 6.00 | 35% → 35% |
| TeamUNIVA ko | overall | 7.43 → 7.43 | 7.24 → 7.24 | 5.20 → 5.20 | 3.92 → 3.89 | 61% → 61% |
| TeamUNIVA ko beta | zeroth | 9.28 → 9.28 | 8.55 → 8.55 | 5.44 → 5.44 | 2.46 → 2.44 | 80% → 80% |
| TeamUNIVA ko beta | fleurs | 6.20 → 6.20 | 6.43 → 6.43 | 4.40 → 4.40 | 4.31 → 4.25 | 49% → 49% |
| TeamUNIVA ko beta | commonvoice | 7.04 → 7.04 | 7.28 → 7.28 | 6.30 → 6.30 | 6.08 → 6.08 | 36% → 36% |
| TeamUNIVA ko beta | overall | 7.61 → 7.61 | 7.45 → 7.45 | 5.26 → 5.26 | 3.99 → 3.96 | 61% → 61% |
| Qwen3-ASR base | zeroth | 7.60 → 7.60 | 6.35 → 6.35 | 3.73 → 3.73 | 2.91 → 2.90 | 71% → 71% |
| Qwen3-ASR base | fleurs | 6.08 → 6.08 | 6.53 → 6.53 | 4.56 → 4.56 | 4.31 → 4.25 | 47% → 48% |
| Qwen3-ASR base | commonvoice | 7.32 → 7.32 | 7.59 → 7.59 | 6.68 → 6.68 | 6.61 → 6.61 | 33% → 33% |
| Qwen3-ASR base | overall | 6.97 → 6.97 | 6.72 → 6.72 | 4.73 → 4.73 | 4.30 → 4.27 | 54% → 54% |
| BuzzASR | zeroth | 7.60 → 7.60 | 5.87 → 5.87 | 5.85 → 5.85 | 3.16 → 3.10 | 69% → 69% |
| BuzzASR | fleurs | 8.38 → 8.37 | 9.54 → 9.54 | 4.79 → 4.79 | 4.72 → 4.31 | 58% → 62% |
| BuzzASR | commonvoice | 7.36 → 7.36 | 8.23 → 8.23 | 3.98 → 3.98 | 3.88 → 3.88 | 61% → 61% |
| BuzzASR | overall | 7.83 → 7.83 | 7.81 → 7.81 | 5.02 → 5.02 | 3.90 → 3.72 | 63% → 64% |
| whisper-large-v3 | zeroth | 8.60 → 6.88 | 5.44 → 5.44 | 4.27 → 4.27 | 2.93 → 2.90 | 74% → 68% |
| whisper-large-v3 | fleurs | 8.94 → 7.44 | 7.77 → 7.77 | 5.00 → 5.00 | 4.37 → 4.25 | 64% → 58% |
| whisper-large-v3 | commonvoice | 12.17 → 8.52 | 9.06 → 9.06 | 5.85 → 5.85 | 5.80 → 5.80 | 65% → 50% |
| whisper-large-v3 | overall | 9.58 → 7.48 | 7.18 → 7.18 | 4.91 → 4.91 | 4.13 → 4.08 | 68% → 59% |
| SenseVoice itn | zeroth | 4.27 → 4.27 | 4.88 → 4.88 | 2.40 → 2.40 | 2.40 → 2.40 | 57% → 57% |
| SenseVoice itn | fleurs | 10.38 → 10.38 | 10.74 → 10.74 | 8.46 → 8.46 | 6.95 → 6.83 | 50% → 51% |
| SenseVoice itn | commonvoice | 10.37 → 10.37 | 10.53 → 10.53 | 9.80 → 9.80 | 9.68 → 9.68 | 31% → 31% |
| SenseVoice itn | overall | 7.98 → 7.98 | 8.43 → 8.43 | 6.36 → 6.36 | 5.78 → 5.74 | 46% → 46% |
| SenseVoice noitn | zeroth | 2.39 → 2.39 | 2.41 → 2.41 | 2.41 → 2.41 | 2.41 → 2.41 | 24% → 24% |
| SenseVoice noitn | fleurs | 12.05 → 12.05 | 12.95 → 12.95 | 8.41 → 8.41 | 6.91 → 6.79 | 57% → 58% |
| SenseVoice noitn | commonvoice | 12.87 → 12.87 | 13.66 → 13.66 | 9.83 → 9.83 | 9.72 → 9.72 | 44% → 44% |
| SenseVoice noitn | overall | 8.45 → 8.45 | 9.05 → 9.05 | 6.36 → 6.36 | 5.79 → 5.74 | 49% → 49% |

## Ranks at the kocer level (before / after)

- zeroth: TeamUNIVA ko < SenseVoice itn < SenseVoice noitn < TeamUNIVA ko beta < Qwen3-ASR base < whisper-large-v3 < BuzzASR
- fleurs: TeamUNIVA ko < Qwen3-ASR base < TeamUNIVA ko beta < whisper-large-v3 < BuzzASR < SenseVoice noitn < SenseVoice itn
  → after: TeamUNIVA ko < Qwen3-ASR base < whisper-large-v3 < TeamUNIVA ko beta < BuzzASR < SenseVoice noitn < SenseVoice itn
- commonvoice: BuzzASR < whisper-large-v3 < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn
- overall: BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < whisper-large-v3 < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn

Notation share of raw errors, pooled public sets: 46%–68% → **46%–64%**

## KsponSpeech (spelling reference), CER % raw / nospace / nopunct / kocer / kocer+fillers

- qwen3-asr-1.7b-ko-univa-release|kspon_clean: 8.38 → 8.38 | 8.32 → 8.32 | 6.29 → 6.29 | 6.10 → 6.09 | 6.13 → 6.13
- qwen3-asr-1.7b-ko-univa-release|kspon_other: 8.95 → 8.95 | 8.74 → 8.74 | 6.70 → 6.70 | 6.48 → 6.46 | 6.60 → 6.58
- qwen3-asr-1.7b-ko-univa-release|both: 8.71 → 8.71 | 8.57 → 8.57 | 6.53 → 6.53 | 6.32 → 6.31 | 6.41 → 6.40
- qwen3-asr-1.7b-ko-univa|kspon_clean: 8.98 → 8.98 | 9.19 → 9.19 | 7.10 → 7.10 | 6.81 → 6.80 | 6.91 → 6.89
- qwen3-asr-1.7b-ko-univa|kspon_other: 9.79 → 9.79 | 9.76 → 9.76 | 7.74 → 7.74 | 7.26 → 7.24 | 7.39 → 7.37
- qwen3-asr-1.7b-ko-univa|both: 9.46 → 9.46 | 9.52 → 9.52 | 7.48 → 7.48 | 7.08 → 7.06 | 7.19 → 7.18
- qwen3-asr-1.7b|kspon_clean: 12.47 → 12.47 | 13.05 → 13.05 | 9.51 → 9.51 | 8.70 → 8.69 | 8.46 → 8.45
- qwen3-asr-1.7b|kspon_other: 12.66 → 12.66 | 12.82 → 12.82 | 9.77 → 9.77 | 8.59 → 8.58 | 8.52 → 8.50
- qwen3-asr-1.7b|both: 12.58 → 12.58 | 12.91 → 12.91 | 9.66 → 9.66 | 8.63 → 8.62 | 8.49 → 8.48
- buzzasr-korean|kspon_clean: 14.73 → 14.44 | 15.04 → 15.04 | 10.45 → 10.45 | 10.14 → 10.07 | 9.79 → 9.72
- buzzasr-korean|kspon_other: 13.70 → 13.54 | 13.48 → 13.48 | 9.79 → 9.79 | 9.41 → 9.30 | 9.14 → 9.04
- buzzasr-korean|both: 14.12 → 13.91 | 14.12 → 14.12 | 10.06 → 10.06 | 9.71 → 9.62 | 9.41 → 9.31
- whisper-large-v3|kspon_clean: 17.53 → 14.81 | 14.32 → 14.32 | 11.32 → 11.32 | 11.07 → 11.06 | 10.28 → 10.27
- whisper-large-v3|kspon_other: 17.62 → 15.65 | 14.80 → 14.80 | 12.20 → 12.20 | 11.87 → 11.86 | 11.31 → 11.30
- whisper-large-v3|both: 17.58 → 15.30 | 14.60 → 14.60 | 11.84 → 11.84 | 11.55 → 11.53 | 10.89 → 10.88
- sensevoice-small-noitn|kspon_clean: 19.53 → 19.53 | 17.81 → 17.81 | 13.49 → 13.49 | 13.09 → 13.09 | 12.97 → 12.97
- sensevoice-small-noitn|kspon_other: 20.39 → 20.39 | 17.57 → 17.57 | 14.20 → 14.20 | 13.72 → 13.69 | 13.66 → 13.62
- sensevoice-small-noitn|both: 20.03 → 20.03 | 17.66 → 17.66 | 13.91 → 13.91 | 13.46 → 13.44 | 13.38 → 13.36
- sensevoice-small-itn|kspon_clean: 19.14 → 19.14 | 17.19 → 17.19 | 13.68 → 13.68 | 13.28 → 13.28 | 13.15 → 13.15
- sensevoice-small-itn|kspon_other: 20.34 → 20.34 | 17.49 → 17.49 | 14.29 → 14.29 | 13.82 → 13.79 | 13.75 → 13.71
- sensevoice-small-itn|both: 19.84 → 19.84 | 17.37 → 17.37 | 14.04 → 14.04 | 13.60 → 13.58 | 13.50 → 13.48

## KsponSpeech (pronunciation reference)

- qwen3-asr-1.7b-ko-univa-release|kspon_clean: 9.23 → 9.23 | 9.11 → 9.11 | 7.13 → 7.13 | 6.10 → 6.09 | 6.13 → 6.12
- qwen3-asr-1.7b-ko-univa-release|kspon_other: 9.98 → 9.98 | 9.59 → 9.59 | 7.57 → 7.57 | 6.17 → 6.15 | 6.28 → 6.26
- qwen3-asr-1.7b-ko-univa-release|both: 9.67 → 9.67 | 9.39 → 9.39 | 7.39 → 7.39 | 6.14 → 6.12 | 6.22 → 6.20
- qwen3-asr-1.7b-ko-univa|kspon_clean: 9.40 → 9.40 | 9.52 → 9.52 | 7.46 → 7.46 | 6.66 → 6.65 | 6.75 → 6.74
- qwen3-asr-1.7b-ko-univa|kspon_other: 10.09 → 10.09 | 9.83 → 9.83 | 7.83 → 7.83 | 6.78 → 6.76 | 6.90 → 6.88
- qwen3-asr-1.7b-ko-univa|both: 9.80 → 9.80 | 9.70 → 9.70 | 7.68 → 7.68 | 6.73 → 6.71 | 6.84 → 6.82
- qwen3-asr-1.7b|kspon_clean: 12.20 → 12.20 | 12.68 → 12.68 | 9.08 → 9.08 | 8.84 → 8.83 | 8.61 → 8.60
- qwen3-asr-1.7b|kspon_other: 11.91 → 11.91 | 11.86 → 11.86 | 8.76 → 8.76 | 8.44 → 8.43 | 8.37 → 8.36
- qwen3-asr-1.7b|both: 12.03 → 12.03 | 12.20 → 12.20 | 8.89 → 8.89 | 8.60 → 8.60 | 8.47 → 8.46
- buzzasr-korean|kspon_clean: 15.27 → 15.00 | 15.54 → 15.54 | 10.98 → 10.98 | 10.16 → 10.09 | 9.80 → 9.73
- buzzasr-korean|kspon_other: 14.37 → 14.23 | 13.98 → 13.98 | 10.31 → 10.31 | 9.22 → 9.11 | 8.96 → 8.84
- buzzasr-korean|both: 14.75 → 14.55 | 14.63 → 14.63 | 10.59 → 10.59 | 9.61 → 9.51 | 9.31 → 9.21
- whisper-large-v3|kspon_clean: 18.21 → 15.52 | 15.00 → 15.00 | 11.99 → 11.99 | 11.07 → 11.05 | 10.28 → 10.26
- whisper-large-v3|kspon_other: 18.35 → 16.45 | 15.44 → 15.44 | 12.85 → 12.85 | 12.00 → 11.97 | 11.44 → 11.41
- whisper-large-v3|both: 18.29 → 16.06 | 15.26 → 15.26 | 12.50 → 12.50 | 11.62 → 11.59 | 10.96 → 10.94
- sensevoice-small-noitn|kspon_clean: 19.75 → 19.75 | 18.09 → 18.09 | 13.81 → 13.81 | 13.09 → 13.10 | 12.99 → 12.99
- sensevoice-small-noitn|kspon_other: 20.48 → 20.48 | 17.65 → 17.65 | 14.30 → 14.30 | 13.41 → 13.40 | 13.34 → 13.34
- sensevoice-small-noitn|both: 20.18 → 20.18 | 17.83 → 17.83 | 14.10 → 14.10 | 13.28 → 13.28 | 13.20 → 13.19
- sensevoice-small-itn|kspon_clean: 19.36 → 19.36 | 17.46 → 17.46 | 13.98 → 13.98 | 13.26 → 13.27 | 13.14 → 13.14
- sensevoice-small-itn|kspon_other: 20.47 → 20.47 | 17.62 → 17.62 | 14.42 → 14.42 | 13.51 → 13.50 | 13.44 → 13.43
- sensevoice-small-itn|both: 20.01 → 20.01 | 17.55 → 17.55 | 14.24 → 14.24 | 13.41 → 13.40 | 13.32 → 13.31

## Telephone HR: spelling raw / nospace+punct / kocer, pronunciation raw / nospace+punct / kocer, raw transcript kocer

- whisper-large-v3: 8.10 → 5.92 | 5.44 → 5.44 | 5.02 → 5.02 | 13.02 → 11.03 | 10.25 → 10.25 | 5.33 → 5.04 | 4.92 → 4.95
- BuzzASR: 8.17 → 6.38 | 5.97 → 5.97 | 5.61 → 5.36 | 12.97 → 11.36 | 10.62 → 10.62 | 5.93 → 5.40 | 5.50 → 5.29
- TeamUNIVA ko: 6.73 → 6.73 | 6.26 → 6.26 | 5.76 → 5.75 | 11.48 → 11.48 | 10.78 → 10.78 | 6.04 → 5.76 | 5.64 → 5.68
- TeamUNIVA ko beta: 10.64 → 10.64 | 9.83 → 9.83 | 9.17 → 9.12 | 14.93 → 14.93 | 13.86 → 13.86 | 9.31 → 9.09 | 8.97 → 9.02
- Qwen3-ASR base: 12.96 → 12.96 | 12.01 → 12.01 | 10.76 → 10.75 | 16.18 → 16.18 | 14.92 → 14.92 | 10.94 → 10.71 | 10.59 → 10.66
- SenseVoice itn: 23.32 → 23.32 | 21.66 → 21.66 | 21.30 → 21.33 | 26.85 → 26.85 | 24.85 → 24.85 | 21.38 → 21.31 | 21.08 → 21.25
- SenseVoice noitn: 24.57 → 24.57 | 21.86 → 21.86 | 21.55 → 21.53 | 28.04 → 28.04 | 25.01 → 25.01 | 21.58 → 21.55 | 21.32 → 21.45

## number_subset.md: lines that changed

- before: | qwen3-asr-1.7b-ko-univa | 11.06 | 2.85 | 8.20 | 5 -> 3 |
  after:  | qwen3-asr-1.7b-ko-univa-release | 11.09 | 2.78 | 8.30 | 7 -> 3 |
- before: | qwen3-asr-1.7b-ko-univa-release | 11.09 | 2.87 | 8.22 | 7 -> 4 |
  after:  | qwen3-asr-1.7b-ko-univa | 11.06 | 2.78 | 8.28 | 5 -> 4 |
- before: | whisper-large-v3 | 6.79 | 3.11 | 3.68 | 4 -> 5 |
  after:  | whisper-large-v3 | 6.79 | 3.04 | 3.75 | 4 -> 5 |
- before: | qwen3-asr-1.7b | 5.56 | 3.31 | 2.25 | 3 -> 6 |
  after:  | qwen3-asr-1.7b | 5.56 | 3.28 | 2.28 | 3 -> 6 |
- before: | buzzasr-korean | 11.07 | 3.67 | 7.40 | 6 -> 7 |
  after:  | buzzasr-korean | 11.07 | 3.50 | 7.58 | 6 -> 7 |
- before: version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct +5.49 [+4.35,+6.71]* | kocer -0.46 [-0.90,-0.03]*; release-base nopunct +5.
  after:  version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct +5.49 [+4.35,+6.71]* | kocer -0.50 [-0.91,-0.09]*; release-base nopunct +5.
- before: | qwen3-asr-1.7b-ko-univa-release | 5.68 | 5.57 | 0.10 | 1 -> 1 |
  after:  | qwen3-asr-1.7b-ko-univa-release | 5.68 | 5.35 | 0.32 | 1 -> 1 |
- before: | qwen3-asr-1.7b-ko-univa | 5.73 | 5.65 | 0.08 | 2 -> 2 |
  after:  | whisper-large-v3 | 8.18 | 5.35 | 2.83 | 5 -> 2 |
- before: | whisper-large-v3 | 8.18 | 5.77 | 2.41 | 5 -> 3 |
  after:  | qwen3-asr-1.7b-ko-univa | 5.73 | 5.43 | 0.30 | 2 -> 3 |
- before: | qwen3-asr-1.7b | 6.92 | 5.99 | 0.92 | 4 -> 4 |
  after:  | buzzasr-korean | 6.82 | 5.58 | 1.24 | 3 -> 4 |
- before: | buzzasr-korean | 6.82 | 6.57 | 0.25 | 3 -> 5 |
  after:  | qwen3-asr-1.7b | 6.92 | 5.75 | 1.17 | 4 -> 5 |
- before: | sensevoice-small-noitn | 15.07 | 8.88 | 6.19 | 6 -> 6 |
  after:  | sensevoice-small-noitn | 15.07 | 8.65 | 6.42 | 6 -> 6 |
- before: | sensevoice-small-itn | 15.22 | 8.98 | 6.24 | 7 -> 7 |
  after:  | sensevoice-small-itn | 15.22 | 8.73 | 6.49 | 7 -> 7 |
- before: version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -1.19 [-1.91,-0.49]* | kocer -0.34 [-0.79,+0.09]; release-base nopunct -1.2
  after:  version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -1.19 [-1.91,-0.49]* | kocer -0.32 [-0.77,+0.12]; release-base nopunct -1.2
- before: | qwen3-asr-1.7b-ko-univa-release | 6.85 | 5.89 | 0.96 | 1 -> 1 |
  after:  | qwen3-asr-1.7b-ko-univa-release | 6.85 | 5.82 | 1.03 | 1 -> 1 |
- before: | qwen3-asr-1.7b-ko-univa | 9.27 | 6.68 | 2.59 | 2 -> 2 |
  after:  | qwen3-asr-1.7b-ko-univa | 9.27 | 6.59 | 2.68 | 2 -> 2 |
- before: | qwen3-asr-1.7b | 15.35 | 8.23 | 7.12 | 5 -> 3 |
  after:  | qwen3-asr-1.7b | 15.35 | 8.14 | 7.21 | 5 -> 3 |
- before: | buzzasr-korean | 10.73 | 8.54 | 2.20 | 3 -> 4 |
  after:  | buzzasr-korean | 10.73 | 8.34 | 2.39 | 3 -> 4 |
- before: | whisper-large-v3 | 14.88 | 13.14 | 1.74 | 4 -> 5 |
  after:  | whisper-large-v3 | 14.88 | 13.08 | 1.81 | 4 -> 5 |
- before: | sensevoice-small-noitn | 16.81 | 14.12 | 2.69 | 6 -> 6 |
  after:  | sensevoice-small-noitn | 16.81 | 13.96 | 2.85 | 6 -> 6 |
- before: | sensevoice-small-itn | 16.88 | 14.25 | 2.63 | 7 -> 7 |
  after:  | sensevoice-small-itn | 16.88 | 14.09 | 2.79 | 7 -> 7 |
- before: version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -6.08 [-6.84,-5.34]* | kocer -1.55 [-2.06,-1.07]*; release-base nopunct -8.
  after:  version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -6.08 [-6.84,-5.34]* | kocer -1.55 [-2.04,-1.06]*; release-base nopunct -8.
- before: | qwen3-asr-1.7b-ko-univa-release | 13.80 | 5.51 | 8.28 | 3 -> 1 |
  after:  | qwen3-asr-1.7b-ko-univa-release | 13.80 | 5.42 | 8.38 | 3 -> 1 |
- before: | qwen3-asr-1.7b-ko-univa | 12.59 | 6.13 | 6.45 | 2 -> 2 |
  after:  | qwen3-asr-1.7b-ko-univa | 12.59 | 6.03 | 6.56 | 2 -> 2 |
- before: | qwen3-asr-1.7b | 9.67 | 7.87 | 1.80 | 1 -> 3 |
  after:  | qwen3-asr-1.7b | 9.67 | 7.83 | 1.84 | 1 -> 3 |
- ...

## decoding_check.md: lines that changed

- before: | greedy, no repetition penalty (published) | 10.06 | 9.71 | 19 | 10 | 9.07 |
  after:  | greedy, no repetition penalty (published) | 10.06 | 9.62 | 19 | 10 | 8.98 |
- before: | model-card settings | 10.49 | 10.14 | 17 | 8 | 10.04 |
  after:  | model-card settings | 10.49 | 10.05 | 17 | 8 | 9.95 |
- before: kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 6.32; 2. qwen3-asr-1.7b-ko-univa 7.08; 3. qwen3-asr-1.7b 8.63; 4. BuzzASR greedy 9.71; 
  after:  kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 6.31; 2. qwen3-asr-1.7b-ko-univa 7.06; 3. qwen3-asr-1.7b 8.62; 4. BuzzASR greedy 9.62; 
- before: | greedy, no repetition penalty (published) | 5.85 | 3.16 | 0 | 0 | 3.16 |
  after:  | greedy, no repetition penalty (published) | 5.85 | 3.10 | 0 | 0 | 3.10 |
- before: | model-card settings | 6.17 | 3.50 | 0 | 0 | 3.50 |
  after:  | model-card settings | 6.17 | 3.43 | 0 | 0 | 3.43 |
- before: kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 2.37; 2. sensevoice-small-itn 2.40; 3. sensevoice-small-noitn 2.41; 4. qwen3-asr-1.7b-k
  after:  kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 2.34; 2. sensevoice-small-itn 2.40; 3. sensevoice-small-noitn 2.41; 4. qwen3-asr-1.7b-k
- before: | greedy, no repetition penalty (published) | 4.79 | 4.72 | 0 | 0 | 4.72 |
  after:  | greedy, no repetition penalty (published) | 4.79 | 4.31 | 0 | 0 | 4.31 |
- before: | model-card settings | 5.37 | 5.30 | 0 | 0 | 5.30 |
  after:  | model-card settings | 5.37 | 4.90 | 0 | 0 | 4.90 |
- before: card - greedy, kocer: +0.58 pt [+0.39, +0.77] *
  after:  card - greedy, kocer: +0.59 pt [+0.39, +0.78] *
- before: kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 4.25; 2. qwen3-asr-1.7b 4.31; 3. qwen3-asr-1.7b-ko-univa 4.31; 4. whisper-large-v3 4.37
  after:  kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 4.19; 2. qwen3-asr-1.7b 4.25; 3. whisper-large-v3 4.25; 4. qwen3-asr-1.7b-ko-univa 4.25
- before: | greedy, no repetition penalty (published) | 5.97 | 5.61 | 0 | 0 | 5.61 |
  after:  | greedy, no repetition penalty (published) | 5.97 | 5.36 | 0 | 0 | 5.36 |
- before: | model-card settings | 6.87 | 6.50 | 0 | 0 | 6.50 |
  after:  | model-card settings | 6.87 | 6.26 | 0 | 0 | 6.26 |
- before: card - greedy, kocer: +0.90 pt [+0.77, +1.02] *
  after:  card - greedy, kocer: +0.90 pt [+0.78, +1.02] *
- before: kocer ranking with both BuzzASR runs: 1. whisper-large-v3 5.02; 2. BuzzASR greedy 5.61; 3. qwen3-asr-1.7b-ko-univa-release 5.76; 4. BuzzASR card settings 6.50; 
  after:  kocer ranking with both BuzzASR runs: 1. whisper-large-v3 5.02; 2. BuzzASR greedy 5.36; 3. qwen3-asr-1.7b-ko-univa-release 5.75; 4. BuzzASR card settings 6.26; 

## univa_compare.md: lines that changed

- before: | base | 2.91 | 4.31 | 6.61 | 4.30 |
  after:  | base | 2.90 | 4.25 | 6.61 | 4.27 |
- before: | beta | 2.46 | 4.31 | 6.08 | 3.99 |
  after:  | beta | 2.44 | 4.25 | 6.08 | 3.96 |
- before: | release | 2.37 | 4.25 | 6.00 | 3.92 |
  after:  | release | 2.34 | 4.19 | 6.00 | 3.89 |
- before: | base | 4521 | 2236 (49%) | 201 (4%) | 2084 (46%) |
  after:  | base | 4521 | 2236 (49%) | 215 (5%) | 2070 (46%) |
- before: | beta | 4935 | 2389 (48%) | 610 (12%) | 1936 (39%) |
  after:  | beta | 4935 | 2389 (48%) | 626 (13%) | 1920 (39%) |
- before: | release | 4816 | 2302 (48%) | 614 (13%) | 1900 (39%) |
  after:  | release | 4816 | 2302 (48%) | 631 (13%) | 1883 (39%) |
- before: | release - beta | kocer | -0.09 [-0.25,+0.07] | -0.06 [-0.19,+0.08] | -0.08 [-0.49,+0.34] | -0.07 [-0.20,+0.05] |
  after:  | release - beta | kocer | -0.09 [-0.26,+0.06] | -0.06 [-0.19,+0.08] | -0.08 [-0.49,+0.34] | -0.08 [-0.21,+0.05] |
- before: | release - base | kocer | -0.54 [-0.80,-0.29]* | -0.06 [-0.28,+0.17] | -0.61 [-1.06,-0.14]* | -0.38 [-0.54,-0.21]* |
  after:  | release - base | kocer | -0.56 [-0.82,-0.31]* | -0.05 [-0.28,+0.18] | -0.61 [-1.06,-0.14]* | -0.39 [-0.55,-0.22]* |
