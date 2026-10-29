# KsponSpeech eval (clean + other), 6000 utterances. Numbers only.


## Reference = spelling side. CER (%) per level

| model | split | raw | nospace | nopunct | kocer | kocer+fillers |
|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | kspon_clean | 8.38 | 8.32 | 6.29 | 6.08 | 6.12 |
| qwen3-asr-1.7b-ko-univa-release | kspon_other | 8.95 | 8.74 | 6.70 | 6.46 | 6.58 |
| qwen3-asr-1.7b-ko-univa-release | both | 8.71 | 8.57 | 6.53 | 6.30 | 6.39 |
| qwen3-asr-1.7b-ko-univa | kspon_clean | 8.98 | 9.19 | 7.10 | 6.80 | 6.89 |
| qwen3-asr-1.7b-ko-univa | kspon_other | 9.79 | 9.76 | 7.74 | 7.23 | 7.36 |
| qwen3-asr-1.7b-ko-univa | both | 9.46 | 9.52 | 7.48 | 7.05 | 7.17 |
| qwen3-asr-1.7b | kspon_clean | 12.47 | 13.05 | 9.51 | 8.69 | 8.45 |
| qwen3-asr-1.7b | kspon_other | 12.66 | 12.82 | 9.77 | 8.57 | 8.50 |
| qwen3-asr-1.7b | both | 12.58 | 12.91 | 9.66 | 8.62 | 8.48 |
| buzzasr-korean | kspon_clean | 14.44 | 15.04 | 10.45 | 10.06 | 9.71 |
| buzzasr-korean | kspon_other | 13.54 | 13.48 | 9.79 | 9.29 | 9.03 |
| buzzasr-korean | both | 13.91 | 14.12 | 10.06 | 9.61 | 9.31 |
| whisper-large-v3 | kspon_clean | 14.81 | 14.32 | 11.32 | 11.06 | 10.26 |
| whisper-large-v3 | kspon_other | 15.65 | 14.80 | 12.20 | 11.85 | 11.29 |
| whisper-large-v3 | both | 15.30 | 14.60 | 11.84 | 11.53 | 10.87 |
| sensevoice-small-noitn | kspon_clean | 19.53 | 17.81 | 13.49 | 13.07 | 12.95 |
| sensevoice-small-noitn | kspon_other | 20.39 | 17.57 | 14.20 | 13.67 | 13.60 |
| sensevoice-small-noitn | both | 20.03 | 17.66 | 13.91 | 13.42 | 13.34 |
| sensevoice-small-itn | kspon_clean | 19.14 | 17.19 | 13.68 | 13.26 | 13.12 |
| sensevoice-small-itn | kspon_other | 20.34 | 17.49 | 14.29 | 13.77 | 13.69 |
| sensevoice-small-itn | both | 19.84 | 17.37 | 14.04 | 13.56 | 13.46 |

## Reference = pronunciation side. CER (%) per level

| model | split | raw | nospace | nopunct | kocer | kocer+fillers |
|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | kspon_clean | 9.23 | 9.11 | 7.13 | 6.09 | 6.12 |
| qwen3-asr-1.7b-ko-univa-release | kspon_other | 9.98 | 9.59 | 7.57 | 6.15 | 6.26 |
| qwen3-asr-1.7b-ko-univa-release | both | 9.67 | 9.39 | 7.39 | 6.12 | 6.20 |
| qwen3-asr-1.7b-ko-univa | kspon_clean | 9.40 | 9.52 | 7.46 | 6.65 | 6.74 |
| qwen3-asr-1.7b-ko-univa | kspon_other | 10.09 | 9.83 | 7.83 | 6.76 | 6.88 |
| qwen3-asr-1.7b-ko-univa | both | 9.80 | 9.70 | 7.68 | 6.71 | 6.82 |
| qwen3-asr-1.7b | kspon_clean | 12.20 | 12.68 | 9.08 | 8.83 | 8.60 |
| qwen3-asr-1.7b | kspon_other | 11.91 | 11.86 | 8.76 | 8.43 | 8.36 |
| qwen3-asr-1.7b | both | 12.03 | 12.20 | 8.89 | 8.60 | 8.46 |
| buzzasr-korean | kspon_clean | 15.00 | 15.54 | 10.98 | 10.09 | 9.73 |
| buzzasr-korean | kspon_other | 14.23 | 13.98 | 10.31 | 9.11 | 8.84 |
| buzzasr-korean | both | 14.55 | 14.63 | 10.59 | 9.51 | 9.21 |
| whisper-large-v3 | kspon_clean | 15.52 | 15.00 | 11.99 | 11.05 | 10.26 |
| whisper-large-v3 | kspon_other | 16.45 | 15.44 | 12.85 | 11.66 | 11.10 |
| whisper-large-v3 | both | 16.06 | 15.26 | 12.50 | 11.41 | 10.75 |
| sensevoice-small-noitn | kspon_clean | 19.75 | 18.09 | 13.81 | 13.10 | 12.99 |
| sensevoice-small-noitn | kspon_other | 20.48 | 17.65 | 14.30 | 13.40 | 13.34 |
| sensevoice-small-noitn | both | 20.18 | 17.83 | 14.10 | 13.28 | 13.19 |
| sensevoice-small-itn | kspon_clean | 19.36 | 17.46 | 13.98 | 13.27 | 13.14 |
| sensevoice-small-itn | kspon_other | 20.47 | 17.62 | 14.42 | 13.50 | 13.43 |
| sensevoice-small-itn | both | 20.01 | 17.55 | 14.24 | 13.40 | 13.31 |

## Reference choice sensitivity (clean+other): spelling vs pronunciation reference

| model | raw spelling | raw pron | gap | nopunct spelling | nopunct pron | gap | kocer spelling | kocer pron | gap |
|---|---|---|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | 8.71 | 9.67 | +0.96 | 6.53 | 7.39 | +0.85 | 6.30 | 6.12 | -0.18 |
| qwen3-asr-1.7b-ko-univa | 9.46 | 9.80 | +0.34 | 7.48 | 7.68 | +0.20 | 7.05 | 6.71 | -0.34 |
| qwen3-asr-1.7b | 12.58 | 12.03 | -0.56 | 9.66 | 8.89 | -0.77 | 8.62 | 8.60 | -0.02 |
| buzzasr-korean | 13.91 | 14.55 | +0.63 | 10.06 | 10.59 | +0.53 | 9.61 | 9.51 | -0.10 |
| whisper-large-v3 | 15.30 | 16.06 | +0.76 | 11.84 | 12.50 | +0.66 | 11.53 | 11.41 | -0.11 |
| sensevoice-small-noitn | 20.03 | 20.18 | +0.15 | 13.91 | 14.10 | +0.19 | 13.42 | 13.28 | -0.14 |
| sensevoice-small-itn | 19.84 | 20.01 | +0.17 | 14.04 | 14.24 | +0.20 | 13.56 | 13.40 | -0.15 |

## Ranks (clean+other) by reference and level

| model | spell raw | spell nopunct | spell kocer | pronu raw | pronu nopunct | pronu kocer |
|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | 1 | 1 | 1 | 1 | 1 | 1 |
| qwen3-asr-1.7b-ko-univa | 2 | 2 | 2 | 2 | 2 | 2 |
| qwen3-asr-1.7b | 3 | 3 | 3 | 3 | 3 | 3 |
| buzzasr-korean | 4 | 4 | 4 | 4 | 4 | 4 |
| whisper-large-v3 | 5 | 5 | 5 | 5 | 5 | 5 |
| sensevoice-small-noitn | 7 | 6 | 6 | 7 | 6 | 6 |
| sensevoice-small-itn | 6 | 7 | 7 | 6 | 7 | 7 |

## Where raw errors go (clean+other, spelling reference; counts, share of raw)

| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | fillers (extra) | remaining |
|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | 14264 | 3746 (26%) | 2876 (20%) | 269 (2%) | 36 (0%) | 7337 (51%) |
| qwen3-asr-1.7b-ko-univa | 15489 | 3796 (25%) | 2946 (19%) | 497 (3%) | 22 (0%) | 8228 (53%) |
| qwen3-asr-1.7b | 20611 | 4754 (23%) | 4552 (22%) | 1218 (6%) | 352 (2%) | 9735 (47%) |
| buzzasr-korean | 22791 | 5448 (24%) | 5570 (24%) | 532 (2%) | 558 (2%) | 10683 (47%) |
| whisper-large-v3 | 25061 | 7135 (28%) | 4075 (16%) | 366 (1%) | 1006 (4%) | 12479 (50%) |
| sensevoice-small-noitn | 32805 | 11115 (34%) | 5415 (17%) | 573 (2%) | 392 (1%) | 15310 (47%) |
| sensevoice-small-itn | 32496 | 11172 (34%) | 4902 (15%) | 559 (2%) | 408 (1%) | 15455 (48%) |

## Pairwise paired bootstrap, kocer level — KsponSpeech only (spelling ref), n=6000. CER(row) - CER(col), %p, 95% CI, * = excludes 0

| | qwen3-asr-1.7b-k | qwen3-asr-1.7b-k | qwen3-asr-1.7b | buzzasr-korean | whisper-large-v3 | sensevoice-small | sensevoice-small |
|---|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-k | . | -0.75 [-0.88,-0.62]* | -2.32 [-2.49,-2.15]* | -3.31 [-4.23,-2.64]* | -5.22 [-6.10,-4.65]* | -7.12 [-7.37,-6.88]* | -7.26 [-7.51,-7.02]* |
| qwen3-asr-1.7b-k | +0.75 [+0.62,+0.88]* | . | -1.57 [-1.75,-1.40]* | -2.56 [-3.48,-1.89]* | -4.47 [-5.33,-3.90]* | -6.37 [-6.61,-6.12]* | -6.51 [-6.75,-6.26]* |
| qwen3-asr-1.7b | +2.32 [+2.15,+2.49]* | +1.57 [+1.40,+1.75]* | . | -0.99 [-1.92,-0.33]* | -2.90 [-3.80,-2.34]* | -4.80 [-5.04,-4.57]* | -4.94 [-5.18,-4.70]* |
| buzzasr-korean | +3.31 [+2.64,+4.23]* | +2.56 [+1.89,+3.48]* | +0.99 [+0.33,+1.92]* | . | -1.92 [-2.99,-0.83]* | -3.81 [-4.48,-2.86]* | -3.95 [-4.62,-3.03]* |
| whisper-large-v3 | +5.22 [+4.65,+6.10]* | +4.47 [+3.90,+5.33]* | +2.90 [+2.34,+3.80]* | +1.92 [+0.83,+2.99]* | . | -1.89 [-2.47,-1.02]* | -2.03 [-2.60,-1.15]* |
| sensevoice-small | +7.12 [+6.88,+7.37]* | +6.37 [+6.12,+6.61]* | +4.80 [+4.57,+5.04]* | +3.81 [+2.86,+4.48]* | +1.89 [+1.02,+2.47]* | . | -0.14 [-0.20,-0.08]* |
| sensevoice-small | +7.26 [+7.02,+7.51]* | +6.51 [+6.26,+6.75]* | +4.94 [+4.70,+5.18]* | +3.95 [+3.03,+4.62]* | +2.03 [+1.15,+2.60]* | +0.14 [+0.08,+0.20]* | . |

Rank intervals: qwen3-asr-1.7b-ko-univa-release [1, 1] P(1st)=1.00; qwen3-asr-1.7b-ko-univa [2, 2] P(1st)=0.00; qwen3-asr-1.7b [3, 3] P(1st)=0.00; buzzasr-korean [4, 4] P(1st)=0.00; whisper-large-v3 [5, 5] P(1st)=0.00; sensevoice-small-noitn [6, 6] P(1st)=0.00; sensevoice-small-itn [7, 7] P(1st)=0.00

## Pairwise paired bootstrap, kocer level — Kspon + Zeroth + FLEURS + CV27 (spelling ref for Kspon), n=7418. CER(row) - CER(col), %p, 95% CI, * = excludes 0

| | qwen3-asr-1.7b-k | qwen3-asr-1.7b-k | qwen3-asr-1.7b | buzzasr-korean | whisper-large-v3 | sensevoice-small | sensevoice-small |
|---|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-k | . | -0.55 [-0.65,-0.45]* | -1.76 [-1.89,-1.63]* | -2.29 [-3.04,-1.82]* | -3.76 [-4.40,-3.33]* | -5.58 [-5.79,-5.39]* | -5.68 [-5.89,-5.47]* |
| qwen3-asr-1.7b-k | +0.55 [+0.45,+0.65]* | . | -1.21 [-1.35,-1.06]* | -1.74 [-2.49,-1.28]* | -3.20 [-3.85,-2.79]* | -5.03 [-5.24,-4.83]* | -5.12 [-5.34,-4.93]* |
| qwen3-asr-1.7b | +1.76 [+1.63,+1.89]* | +1.21 [+1.06,+1.35]* | . | -0.53 [-1.27,-0.06]* | -2.00 [-2.63,-1.59]* | -3.82 [-4.03,-3.63]* | -3.92 [-4.13,-3.72]* |
| buzzasr-korean | +2.29 [+1.82,+3.04]* | +1.74 [+1.28,+2.49]* | +0.53 [+0.06,+1.27]* | . | -1.46 [-2.26,-0.68]* | -3.29 [-3.77,-2.55]* | -3.39 [-3.88,-2.64]* |
| whisper-large-v3 | +3.76 [+3.33,+4.40]* | +3.20 [+2.79,+3.85]* | +2.00 [+1.59,+2.63]* | +1.46 [+0.68,+2.26]* | . | -1.82 [-2.24,-1.18]* | -1.92 [-2.34,-1.27]* |
| sensevoice-small | +5.58 [+5.39,+5.79]* | +5.03 [+4.83,+5.24]* | +3.82 [+3.63,+4.03]* | +3.29 [+2.55,+3.77]* | +1.82 [+1.18,+2.24]* | . | -0.10 [-0.14,-0.05]* |
| sensevoice-small | +5.68 [+5.47,+5.89]* | +5.12 [+4.93,+5.34]* | +3.92 [+3.72,+4.13]* | +3.39 [+2.64,+3.88]* | +1.92 [+1.27,+2.34]* | +0.10 [+0.05,+0.14]* | . |

Rank intervals: qwen3-asr-1.7b-ko-univa-release [1, 1] P(1st)=1.00; qwen3-asr-1.7b-ko-univa [2, 2] P(1st)=0.00; qwen3-asr-1.7b [3, 3] P(1st)=0.00; buzzasr-korean [4, 4] P(1st)=0.00; whisper-large-v3 [5, 5] P(1st)=0.00; sensevoice-small-noitn [6, 6] P(1st)=0.00; sensevoice-small-itn [7, 7] P(1st)=0.00
