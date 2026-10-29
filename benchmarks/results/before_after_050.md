# Re-scoring the same outputs: kocer 0.4.1 → 0.5.0

Nothing was re-run; only the scorer changed. Rule changes: joint search over reference x hypothesis candidates (up to 4,096 combinations) and a fallback that never does worse than the unexpanded text (#7); fractions (1/2 = 이분의 일) and more unit symbols (m2, kWh, W, L, t, GB, Hz, ℉) (#4).

## Public sets: CER % per level (before → after)

| model | set | raw | nospace | nospace+punct | kocer | notation share of raw |
|---|---|---|---|---|---|---|
| TeamUNIVA ko | zeroth | 8.89 → 8.89 | 8.01 → 8.01 | 5.36 → 5.36 | 2.34 → 2.32 | 80% → 80% |
| TeamUNIVA ko | fleurs | 6.25 → 6.25 | 6.61 → 6.61 | 4.39 → 4.39 | 4.19 → 4.19 | 50% → 50% |
| TeamUNIVA ko | commonvoice | 6.85 → 6.85 | 7.00 → 7.00 | 6.18 → 6.18 | 6.00 → 5.97 | 35% → 35% |
| TeamUNIVA ko | overall | 7.43 → 7.43 | 7.24 → 7.24 | 5.20 → 5.20 | 3.89 → 3.87 | 61% → 61% |
| TeamUNIVA ko beta | zeroth | 9.28 → 9.28 | 8.55 → 8.55 | 5.44 → 5.44 | 2.44 → 2.42 | 80% → 80% |
| TeamUNIVA ko beta | fleurs | 6.20 → 6.20 | 6.43 → 6.43 | 4.40 → 4.40 | 4.25 → 4.25 | 49% → 49% |
| TeamUNIVA ko beta | commonvoice | 7.04 → 7.04 | 7.28 → 7.28 | 6.30 → 6.30 | 6.08 → 6.05 | 36% → 36% |
| TeamUNIVA ko beta | overall | 7.61 → 7.61 | 7.45 → 7.45 | 5.26 → 5.26 | 3.96 → 3.94 | 61% → 61% |
| Qwen3-ASR base | zeroth | 7.60 → 7.60 | 6.35 → 6.35 | 3.73 → 3.73 | 2.90 → 2.90 | 71% → 71% |
| Qwen3-ASR base | fleurs | 6.08 → 6.08 | 6.53 → 6.53 | 4.56 → 4.56 | 4.25 → 4.25 | 48% → 48% |
| Qwen3-ASR base | commonvoice | 7.32 → 7.32 | 7.59 → 7.59 | 6.68 → 6.68 | 6.61 → 6.61 | 33% → 33% |
| Qwen3-ASR base | overall | 6.97 → 6.97 | 6.72 → 6.72 | 4.73 → 4.73 | 4.27 → 4.27 | 54% → 54% |
| BuzzASR | zeroth | 7.60 → 7.60 | 5.87 → 5.87 | 5.85 → 5.85 | 3.10 → 3.08 | 69% → 69% |
| BuzzASR | fleurs | 8.37 → 8.37 | 9.54 → 9.54 | 4.79 → 4.79 | 4.31 → 4.28 | 62% → 62% |
| BuzzASR | commonvoice | 7.36 → 7.36 | 8.23 → 8.23 | 3.98 → 3.98 | 3.88 → 3.88 | 61% → 61% |
| BuzzASR | overall | 7.83 → 7.83 | 7.81 → 7.81 | 5.02 → 5.02 | 3.72 → 3.71 | 64% → 65% |
| whisper-large-v3 | zeroth | 6.88 → 6.88 | 5.44 → 5.44 | 4.27 → 4.27 | 2.90 → 2.90 | 68% → 68% |
| whisper-large-v3 | fleurs | 7.44 → 7.44 | 7.77 → 7.77 | 5.00 → 5.00 | 4.25 → 4.24 | 58% → 58% |
| whisper-large-v3 | commonvoice | 8.52 → 8.52 | 9.06 → 9.06 | 5.85 → 5.85 | 5.80 → 5.80 | 50% → 50% |
| whisper-large-v3 | overall | 7.48 → 7.48 | 7.18 → 7.18 | 4.91 → 4.91 | 4.08 → 4.08 | 59% → 59% |
| SenseVoice itn | zeroth | 4.27 → 4.27 | 4.88 → 4.88 | 2.40 → 2.40 | 2.40 → 2.40 | 57% → 57% |
| SenseVoice itn | fleurs | 10.38 → 10.38 | 10.74 → 10.74 | 8.46 → 8.46 | 6.83 → 6.81 | 51% → 51% |
| SenseVoice itn | commonvoice | 10.37 → 10.37 | 10.53 → 10.53 | 9.80 → 9.80 | 9.68 → 9.68 | 31% → 31% |
| SenseVoice itn | overall | 7.98 → 7.98 | 8.43 → 8.43 | 6.36 → 6.36 | 5.74 → 5.73 | 46% → 46% |
| SenseVoice noitn | zeroth | 2.39 → 2.39 | 2.41 → 2.41 | 2.41 → 2.41 | 2.41 → 2.41 | 24% → 24% |
| SenseVoice noitn | fleurs | 12.05 → 12.05 | 12.95 → 12.95 | 8.41 → 8.41 | 6.79 → 6.76 | 58% → 58% |
| SenseVoice noitn | commonvoice | 12.87 → 12.87 | 13.66 → 13.66 | 9.83 → 9.83 | 9.72 → 9.72 | 44% → 44% |
| SenseVoice noitn | overall | 8.45 → 8.45 | 9.05 → 9.05 | 6.36 → 6.36 | 5.74 → 5.73 | 49% → 49% |

## Ranks at the kocer level (before / after)

- zeroth: TeamUNIVA ko < SenseVoice itn < SenseVoice noitn < TeamUNIVA ko beta < Qwen3-ASR base < whisper-large-v3 < BuzzASR
- fleurs: TeamUNIVA ko < Qwen3-ASR base < whisper-large-v3 < TeamUNIVA ko beta < BuzzASR < SenseVoice noitn < SenseVoice itn
  → after: TeamUNIVA ko < whisper-large-v3 < TeamUNIVA ko beta < Qwen3-ASR base < BuzzASR < SenseVoice noitn < SenseVoice itn
- commonvoice: BuzzASR < whisper-large-v3 < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn
- overall: BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < whisper-large-v3 < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn
  → after: BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < whisper-large-v3 < Qwen3-ASR base < SenseVoice noitn < SenseVoice itn

Notation share of raw errors, pooled public sets: 46%–64% → **46%–65%**

## KsponSpeech (spelling reference), CER % raw / nospace / nopunct / kocer / kocer+fillers

- qwen3-asr-1.7b-ko-univa-release|kspon_clean: 8.38 → 8.38 | 8.32 → 8.32 | 6.29 → 6.29 | 6.09 → 6.08 | 6.13 → 6.12
- qwen3-asr-1.7b-ko-univa-release|kspon_other: 8.95 → 8.95 | 8.74 → 8.74 | 6.70 → 6.70 | 6.46 → 6.46 | 6.58 → 6.58
- qwen3-asr-1.7b-ko-univa-release|both: 8.71 → 8.71 | 8.57 → 8.57 | 6.53 → 6.53 | 6.31 → 6.30 | 6.40 → 6.39
- qwen3-asr-1.7b-ko-univa|kspon_clean: 8.98 → 8.98 | 9.19 → 9.19 | 7.10 → 7.10 | 6.80 → 6.80 | 6.89 → 6.89
- qwen3-asr-1.7b-ko-univa|kspon_other: 9.79 → 9.79 | 9.76 → 9.76 | 7.74 → 7.74 | 7.24 → 7.23 | 7.37 → 7.36
- qwen3-asr-1.7b-ko-univa|both: 9.46 → 9.46 | 9.52 → 9.52 | 7.48 → 7.48 | 7.06 → 7.05 | 7.18 → 7.17
- qwen3-asr-1.7b|kspon_clean: 12.47 → 12.47 | 13.05 → 13.05 | 9.51 → 9.51 | 8.69 → 8.69 | 8.45 → 8.45
- qwen3-asr-1.7b|kspon_other: 12.66 → 12.66 | 12.82 → 12.82 | 9.77 → 9.77 | 8.58 → 8.57 | 8.50 → 8.50
- qwen3-asr-1.7b|both: 12.58 → 12.58 | 12.91 → 12.91 | 9.66 → 9.66 | 8.62 → 8.62 | 8.48 → 8.48
- buzzasr-korean|kspon_clean: 14.44 → 14.44 | 15.04 → 15.04 | 10.45 → 10.45 | 10.07 → 10.06 | 9.72 → 9.71
- buzzasr-korean|kspon_other: 13.54 → 13.54 | 13.48 → 13.48 | 9.79 → 9.79 | 9.30 → 9.29 | 9.04 → 9.03
- buzzasr-korean|both: 13.91 → 13.91 | 14.12 → 14.12 | 10.06 → 10.06 | 9.62 → 9.61 | 9.31 → 9.31
- whisper-large-v3|kspon_clean: 14.81 → 14.81 | 14.32 → 14.32 | 11.32 → 11.32 | 11.06 → 11.06 | 10.27 → 10.26
- whisper-large-v3|kspon_other: 15.65 → 15.65 | 14.80 → 14.80 | 12.20 → 12.20 | 11.86 → 11.85 | 11.30 → 11.29
- whisper-large-v3|both: 15.30 → 15.30 | 14.60 → 14.60 | 11.84 → 11.84 | 11.53 → 11.53 | 10.88 → 10.87
- sensevoice-small-noitn|kspon_clean: 19.53 → 19.53 | 17.81 → 17.81 | 13.49 → 13.49 | 13.09 → 13.07 | 12.97 → 12.95
- sensevoice-small-noitn|kspon_other: 20.39 → 20.39 | 17.57 → 17.57 | 14.20 → 14.20 | 13.69 → 13.67 | 13.62 → 13.60
- sensevoice-small-noitn|both: 20.03 → 20.03 | 17.66 → 17.66 | 13.91 → 13.91 | 13.44 → 13.42 | 13.36 → 13.34
- sensevoice-small-itn|kspon_clean: 19.14 → 19.14 | 17.19 → 17.19 | 13.68 → 13.68 | 13.28 → 13.26 | 13.15 → 13.12
- sensevoice-small-itn|kspon_other: 20.34 → 20.34 | 17.49 → 17.49 | 14.29 → 14.29 | 13.79 → 13.77 | 13.71 → 13.69
- sensevoice-small-itn|both: 19.84 → 19.84 | 17.37 → 17.37 | 14.04 → 14.04 | 13.58 → 13.56 | 13.48 → 13.46

## KsponSpeech (pronunciation reference)

- qwen3-asr-1.7b-ko-univa-release|kspon_clean: 9.23 → 9.23 | 9.11 → 9.11 | 7.13 → 7.13 | 6.09 → 6.09 | 6.12 → 6.12
- qwen3-asr-1.7b-ko-univa-release|kspon_other: 9.98 → 9.98 | 9.59 → 9.59 | 7.57 → 7.57 | 6.15 → 6.15 | 6.26 → 6.26
- qwen3-asr-1.7b-ko-univa-release|both: 9.67 → 9.67 | 9.39 → 9.39 | 7.39 → 7.39 | 6.12 → 6.12 | 6.20 → 6.20
- qwen3-asr-1.7b-ko-univa|kspon_clean: 9.40 → 9.40 | 9.52 → 9.52 | 7.46 → 7.46 | 6.65 → 6.65 | 6.74 → 6.74
- qwen3-asr-1.7b-ko-univa|kspon_other: 10.09 → 10.09 | 9.83 → 9.83 | 7.83 → 7.83 | 6.76 → 6.76 | 6.88 → 6.88
- qwen3-asr-1.7b-ko-univa|both: 9.80 → 9.80 | 9.70 → 9.70 | 7.68 → 7.68 | 6.71 → 6.71 | 6.82 → 6.82
- qwen3-asr-1.7b|kspon_clean: 12.20 → 12.20 | 12.68 → 12.68 | 9.08 → 9.08 | 8.83 → 8.83 | 8.60 → 8.60
- qwen3-asr-1.7b|kspon_other: 11.91 → 11.91 | 11.86 → 11.86 | 8.76 → 8.76 | 8.43 → 8.43 | 8.36 → 8.36
- qwen3-asr-1.7b|both: 12.03 → 12.03 | 12.20 → 12.20 | 8.89 → 8.89 | 8.60 → 8.60 | 8.46 → 8.46
- buzzasr-korean|kspon_clean: 15.00 → 15.00 | 15.54 → 15.54 | 10.98 → 10.98 | 10.09 → 10.09 | 9.73 → 9.73
- buzzasr-korean|kspon_other: 14.23 → 14.23 | 13.98 → 13.98 | 10.31 → 10.31 | 9.11 → 9.11 | 8.84 → 8.84
- buzzasr-korean|both: 14.55 → 14.55 | 14.63 → 14.63 | 10.59 → 10.59 | 9.51 → 9.51 | 9.21 → 9.21
- whisper-large-v3|kspon_clean: 15.52 → 15.52 | 15.00 → 15.00 | 11.99 → 11.99 | 11.05 → 11.05 | 10.26 → 10.26
- whisper-large-v3|kspon_other: 16.45 → 16.45 | 15.44 → 15.44 | 12.85 → 12.85 | 11.97 → 11.66 | 11.41 → 11.10
- whisper-large-v3|both: 16.06 → 16.06 | 15.26 → 15.26 | 12.50 → 12.50 | 11.59 → 11.41 | 10.94 → 10.75
- sensevoice-small-noitn|kspon_clean: 19.75 → 19.75 | 18.09 → 18.09 | 13.81 → 13.81 | 13.10 → 13.10 | 12.99 → 12.99
- sensevoice-small-noitn|kspon_other: 20.48 → 20.48 | 17.65 → 17.65 | 14.30 → 14.30 | 13.40 → 13.40 | 13.34 → 13.34
- sensevoice-small-noitn|both: 20.18 → 20.18 | 17.83 → 17.83 | 14.10 → 14.10 | 13.28 → 13.28 | 13.19 → 13.19
- sensevoice-small-itn|kspon_clean: 19.36 → 19.36 | 17.46 → 17.46 | 13.98 → 13.98 | 13.27 → 13.27 | 13.14 → 13.14
- sensevoice-small-itn|kspon_other: 20.47 → 20.47 | 17.62 → 17.62 | 14.42 → 14.42 | 13.50 → 13.50 | 13.43 → 13.43
- sensevoice-small-itn|both: 20.01 → 20.01 | 17.55 → 17.55 | 14.24 → 14.24 | 13.40 → 13.40 | 13.31 → 13.31

## Telephone HR: spelling raw / nospace+punct / kocer, pronunciation raw / nospace+punct / kocer, raw transcript kocer

- whisper-large-v3: 5.92 → 5.92 | 5.44 → 5.44 | 5.02 → 4.97 | 11.03 → 11.03 | 10.25 → 10.25 | 5.04 → 5.04 | 4.95 → 4.95
- BuzzASR: 6.38 → 6.38 | 5.97 → 5.97 | 5.36 → 5.31 | 11.36 → 11.36 | 10.62 → 10.62 | 5.40 → 5.40 | 5.29 → 5.29
- TeamUNIVA ko: 6.73 → 6.73 | 6.26 → 6.26 | 5.75 → 5.69 | 11.48 → 11.48 | 10.78 → 10.78 | 5.76 → 5.76 | 5.68 → 5.68
- TeamUNIVA ko beta: 10.64 → 10.64 | 9.83 → 9.83 | 9.12 → 9.05 | 14.93 → 14.93 | 13.86 → 13.86 | 9.09 → 9.09 | 9.02 → 9.02
- Qwen3-ASR base: 12.96 → 12.96 | 12.01 → 12.01 | 10.75 → 10.69 | 16.18 → 16.18 | 14.92 → 14.92 | 10.71 → 10.71 | 10.66 → 10.66
- SenseVoice itn: 23.32 → 23.32 | 21.66 → 21.66 | 21.33 → 21.29 | 26.85 → 26.85 | 24.85 → 24.85 | 21.31 → 21.31 | 21.25 → 21.25
- SenseVoice noitn: 24.57 → 24.57 | 21.86 → 21.86 | 21.53 → 21.49 | 28.04 → 28.04 | 25.01 → 25.01 | 21.55 → 21.55 | 21.45 → 21.45

## number_subset.md: lines that changed

- before: | qwen3-asr-1.7b-ko-univa-release | 11.09 | 2.78 | 8.30 | 7 -> 3 |
  after:  | qwen3-asr-1.7b-ko-univa-release | 11.09 | 2.73 | 8.36 | 7 -> 3 |
- before: | qwen3-asr-1.7b-ko-univa | 11.06 | 2.78 | 8.28 | 5 -> 4 |
  after:  | qwen3-asr-1.7b-ko-univa | 11.06 | 2.73 | 8.33 | 5 -> 4 |
- before: | buzzasr-korean | 11.07 | 3.50 | 7.58 | 6 -> 7 |
  after:  | buzzasr-korean | 11.07 | 3.45 | 7.62 | 6 -> 7 |
- before: version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct +5.49 [+4.35,+6.71]* | kocer -0.50 [-0.91,-0.09]*; release-base nopunct +5.
  after:  version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct +5.49 [+4.35,+6.71]* | kocer -0.56 [-0.95,-0.16]*; release-base nopunct +5.
- before: | qwen3-asr-1.7b-ko-univa | 5.73 | 5.43 | 0.30 | 2 -> 3 |
  after:  | qwen3-asr-1.7b-ko-univa | 5.73 | 5.40 | 0.32 | 2 -> 3 |
- before: | buzzasr-korean | 6.82 | 5.58 | 1.24 | 3 -> 4 |
  after:  | buzzasr-korean | 6.82 | 5.53 | 1.29 | 3 -> 4 |
- before: | sensevoice-small-noitn | 15.07 | 8.65 | 6.42 | 6 -> 6 |
  after:  | sensevoice-small-noitn | 15.07 | 8.48 | 6.59 | 6 -> 6 |
- before: | sensevoice-small-itn | 15.22 | 8.73 | 6.49 | 7 -> 7 |
  after:  | sensevoice-small-itn | 15.22 | 8.60 | 6.62 | 7 -> 7 |
- before: version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -1.19 [-1.91,-0.49]* | kocer -0.32 [-0.77,+0.12]; release-base nopunct -1.2
  after:  version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -1.19 [-1.91,-0.49]* | kocer -0.35 [-0.79,+0.10]; release-base nopunct -1.2
- before: | qwen3-asr-1.7b-ko-univa-release | 6.85 | 5.82 | 1.03 | 1 -> 1 |
  after:  | qwen3-asr-1.7b-ko-univa-release | 6.85 | 5.77 | 1.08 | 1 -> 1 |
- before: | qwen3-asr-1.7b-ko-univa | 9.27 | 6.59 | 2.68 | 2 -> 2 |
  after:  | qwen3-asr-1.7b-ko-univa | 9.27 | 6.53 | 2.74 | 2 -> 2 |
- before: | qwen3-asr-1.7b | 15.35 | 8.14 | 7.21 | 5 -> 3 |
  after:  | qwen3-asr-1.7b | 15.35 | 8.13 | 7.22 | 5 -> 3 |
- before: | buzzasr-korean | 10.73 | 8.34 | 2.39 | 3 -> 4 |
  after:  | buzzasr-korean | 10.73 | 8.28 | 2.45 | 3 -> 4 |
- before: | whisper-large-v3 | 14.88 | 13.08 | 1.81 | 4 -> 5 |
  after:  | whisper-large-v3 | 14.88 | 13.03 | 1.85 | 4 -> 5 |
- before: | sensevoice-small-noitn | 16.81 | 13.96 | 2.85 | 6 -> 6 |
  after:  | sensevoice-small-noitn | 16.81 | 13.82 | 2.99 | 6 -> 6 |
- before: | sensevoice-small-itn | 16.88 | 14.09 | 2.79 | 7 -> 7 |
  after:  | sensevoice-small-itn | 16.88 | 13.95 | 2.93 | 7 -> 7 |
- before: version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -6.08 [-6.84,-5.34]* | kocer -1.55 [-2.04,-1.06]*; release-base nopunct -8.
  after:  version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -6.08 [-6.84,-5.34]* | kocer -1.60 [-2.08,-1.09]*; release-base nopunct -8.
- before: | sensevoice-small-noitn | 19.06 | 13.59 | 5.47 | 5 -> 5 |
  after:  | whisper-large-v3 | 20.02 | 12.83 | 7.19 | 7 -> 5 |
- before: | sensevoice-small-itn | 19.28 | 13.70 | 5.58 | 6 -> 6 |
  after:  | sensevoice-small-noitn | 19.06 | 13.59 | 5.47 | 5 -> 6 |
- before: | whisper-large-v3 | 20.02 | 14.11 | 5.91 | 7 -> 7 |
  after:  | sensevoice-small-itn | 19.28 | 13.70 | 5.58 | 6 -> 7 |

## decoding_check.md: lines that changed

- before: | greedy, no repetition penalty (published) | 10.06 | 9.62 | 19 | 10 | 8.98 |
  after:  | greedy, no repetition penalty (published) | 10.06 | 9.61 | 19 | 10 | 8.97 |
- before: | model-card settings | 10.49 | 10.05 | 17 | 8 | 9.95 |
  after:  | model-card settings | 10.49 | 10.04 | 17 | 8 | 9.94 |
- before: kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 6.31; 2. qwen3-asr-1.7b-ko-univa 7.06; 3. qwen3-asr-1.7b 8.62; 4. BuzzASR greedy 9.62; 
  after:  kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 6.30; 2. qwen3-asr-1.7b-ko-univa 7.05; 3. qwen3-asr-1.7b 8.62; 4. BuzzASR greedy 9.61; 
- before: | greedy, no repetition penalty (published) | 5.85 | 3.10 | 0 | 0 | 3.10 |
  after:  | greedy, no repetition penalty (published) | 5.85 | 3.08 | 0 | 0 | 3.08 |
- before: card - greedy, kocer: +0.34 pt [+0.21, +0.46] *
  after:  card - greedy, kocer: +0.35 pt [+0.23, +0.48] *
- before: kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 2.34; 2. sensevoice-small-itn 2.40; 3. sensevoice-small-noitn 2.41; 4. qwen3-asr-1.7b-k
  after:  kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 2.32; 2. sensevoice-small-itn 2.40; 3. sensevoice-small-noitn 2.41; 4. qwen3-asr-1.7b-k
- before: | greedy, no repetition penalty (published) | 4.79 | 4.31 | 0 | 0 | 4.31 |
  after:  | greedy, no repetition penalty (published) | 4.79 | 4.28 | 0 | 0 | 4.28 |
- before: | model-card settings | 5.37 | 4.90 | 0 | 0 | 4.90 |
  after:  | model-card settings | 5.37 | 4.85 | 0 | 0 | 4.85 |
- before: card - greedy, kocer: +0.59 pt [+0.39, +0.78] *
  after:  card - greedy, kocer: +0.57 pt [+0.34, +0.78] *
- before: kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 4.19; 2. qwen3-asr-1.7b 4.25; 3. whisper-large-v3 4.25; 4. qwen3-asr-1.7b-ko-univa 4.25
  after:  kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 4.19; 2. whisper-large-v3 4.24; 3. qwen3-asr-1.7b 4.25; 4. qwen3-asr-1.7b-ko-univa 4.25
- before: kocer ranking with both BuzzASR runs: 1. BuzzASR greedy 3.88; 2. BuzzASR card settings 4.15; 3. whisper-large-v3 5.80; 4. qwen3-asr-1.7b-ko-univa-release 6.00; 
  after:  kocer ranking with both BuzzASR runs: 1. BuzzASR greedy 3.88; 2. BuzzASR card settings 4.15; 3. whisper-large-v3 5.80; 4. qwen3-asr-1.7b-ko-univa-release 5.97; 
- before: | greedy, no repetition penalty (published) | 5.97 | 5.36 | 0 | 0 | 5.36 |
  after:  | greedy, no repetition penalty (published) | 5.97 | 5.31 | 0 | 0 | 5.31 |
- before: | model-card settings | 6.87 | 6.26 | 0 | 0 | 6.26 |
  after:  | model-card settings | 6.87 | 6.21 | 0 | 0 | 6.21 |
- before: kocer ranking with both BuzzASR runs: 1. whisper-large-v3 5.02; 2. BuzzASR greedy 5.36; 3. qwen3-asr-1.7b-ko-univa-release 5.75; 4. BuzzASR card settings 6.26; 
  after:  kocer ranking with both BuzzASR runs: 1. whisper-large-v3 4.97; 2. BuzzASR greedy 5.31; 3. qwen3-asr-1.7b-ko-univa-release 5.69; 4. BuzzASR card settings 6.21; 

## univa_compare.md: lines that changed

- before: | beta | 2.44 | 4.25 | 6.08 | 3.96 |
  after:  | beta | 2.42 | 4.25 | 6.05 | 3.94 |
- before: | release | 2.34 | 4.19 | 6.00 | 3.89 |
  after:  | release | 2.32 | 4.19 | 5.97 | 3.87 |
- before: | beta | 4935 | 2389 (48%) | 626 (13%) | 1920 (39%) |
  after:  | beta | 4935 | 2389 (48%) | 635 (13%) | 1911 (39%) |
- before: | release | 4816 | 2302 (48%) | 631 (13%) | 1883 (39%) |
  after:  | release | 4816 | 2302 (48%) | 640 (13%) | 1874 (39%) |
- before: | release - base | kocer | -0.56 [-0.82,-0.31]* | -0.05 [-0.28,+0.18] | -0.61 [-1.06,-0.14]* | -0.39 [-0.55,-0.22]* |
  after:  | release - base | kocer | -0.58 [-0.83,-0.33]* | -0.06 [-0.28,+0.17] | -0.64 [-1.09,-0.19]* | -0.40 [-0.56,-0.24]* |
