# KsponSpeech eval (clean + other), 6000 utterances. Numbers only.


## Reference = spelling side. CER (%) per level

| model | split | raw | nospace | nopunct | kocer | kocer+fillers |
|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | kspon_clean | 8.38 | 8.32 | 6.29 | 6.10 | 6.13 |
| qwen3-asr-1.7b-ko-univa-release | kspon_other | 8.95 | 8.74 | 6.70 | 6.48 | 6.60 |
| qwen3-asr-1.7b-ko-univa-release | both | 8.71 | 8.57 | 6.53 | 6.32 | 6.41 |
| qwen3-asr-1.7b-ko-univa | kspon_clean | 8.98 | 9.19 | 7.10 | 6.81 | 6.91 |
| qwen3-asr-1.7b-ko-univa | kspon_other | 9.79 | 9.76 | 7.74 | 7.26 | 7.39 |
| qwen3-asr-1.7b-ko-univa | both | 9.46 | 9.52 | 7.48 | 7.08 | 7.19 |
| qwen3-asr-1.7b | kspon_clean | 12.47 | 13.05 | 9.51 | 8.70 | 8.46 |
| qwen3-asr-1.7b | kspon_other | 12.66 | 12.82 | 9.77 | 8.59 | 8.52 |
| qwen3-asr-1.7b | both | 12.58 | 12.91 | 9.66 | 8.63 | 8.49 |
| buzzasr-korean | kspon_clean | 14.73 | 15.04 | 10.45 | 10.14 | 9.79 |
| buzzasr-korean | kspon_other | 13.70 | 13.48 | 9.79 | 9.41 | 9.14 |
| buzzasr-korean | both | 14.12 | 14.12 | 10.06 | 9.71 | 9.41 |
| whisper-large-v3 | kspon_clean | 17.53 | 14.32 | 11.32 | 11.07 | 10.28 |
| whisper-large-v3 | kspon_other | 17.62 | 14.80 | 12.20 | 11.87 | 11.31 |
| whisper-large-v3 | both | 17.58 | 14.60 | 11.84 | 11.55 | 10.89 |
| sensevoice-small-noitn | kspon_clean | 19.53 | 17.81 | 13.49 | 13.09 | 12.97 |
| sensevoice-small-noitn | kspon_other | 20.39 | 17.57 | 14.20 | 13.72 | 13.66 |
| sensevoice-small-noitn | both | 20.03 | 17.66 | 13.91 | 13.46 | 13.38 |
| sensevoice-small-itn | kspon_clean | 19.14 | 17.19 | 13.68 | 13.28 | 13.15 |
| sensevoice-small-itn | kspon_other | 20.34 | 17.49 | 14.29 | 13.82 | 13.75 |
| sensevoice-small-itn | both | 19.84 | 17.37 | 14.04 | 13.60 | 13.50 |

## Reference = pronunciation side. CER (%) per level

| model | split | raw | nospace | nopunct | kocer | kocer+fillers |
|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | kspon_clean | 9.23 | 9.11 | 7.13 | 6.10 | 6.13 |
| qwen3-asr-1.7b-ko-univa-release | kspon_other | 9.98 | 9.59 | 7.57 | 6.17 | 6.28 |
| qwen3-asr-1.7b-ko-univa-release | both | 9.67 | 9.39 | 7.39 | 6.14 | 6.22 |
| qwen3-asr-1.7b-ko-univa | kspon_clean | 9.40 | 9.52 | 7.46 | 6.66 | 6.75 |
| qwen3-asr-1.7b-ko-univa | kspon_other | 10.09 | 9.83 | 7.83 | 6.78 | 6.90 |
| qwen3-asr-1.7b-ko-univa | both | 9.80 | 9.70 | 7.68 | 6.73 | 6.84 |
| qwen3-asr-1.7b | kspon_clean | 12.20 | 12.68 | 9.08 | 8.84 | 8.61 |
| qwen3-asr-1.7b | kspon_other | 11.91 | 11.86 | 8.76 | 8.44 | 8.37 |
| qwen3-asr-1.7b | both | 12.03 | 12.20 | 8.89 | 8.60 | 8.47 |
| buzzasr-korean | kspon_clean | 15.27 | 15.54 | 10.98 | 10.16 | 9.80 |
| buzzasr-korean | kspon_other | 14.37 | 13.98 | 10.31 | 9.22 | 8.96 |
| buzzasr-korean | both | 14.75 | 14.63 | 10.59 | 9.61 | 9.31 |
| whisper-large-v3 | kspon_clean | 18.21 | 15.00 | 11.99 | 11.07 | 10.28 |
| whisper-large-v3 | kspon_other | 18.35 | 15.44 | 12.85 | 12.00 | 11.44 |
| whisper-large-v3 | both | 18.29 | 15.26 | 12.50 | 11.62 | 10.96 |
| sensevoice-small-noitn | kspon_clean | 19.75 | 18.09 | 13.81 | 13.09 | 12.99 |
| sensevoice-small-noitn | kspon_other | 20.48 | 17.65 | 14.30 | 13.41 | 13.34 |
| sensevoice-small-noitn | both | 20.18 | 17.83 | 14.10 | 13.28 | 13.20 |
| sensevoice-small-itn | kspon_clean | 19.36 | 17.46 | 13.98 | 13.26 | 13.14 |
| sensevoice-small-itn | kspon_other | 20.47 | 17.62 | 14.42 | 13.51 | 13.44 |
| sensevoice-small-itn | both | 20.01 | 17.55 | 14.24 | 13.41 | 13.32 |

## Reference choice sensitivity (clean+other): spelling vs pronunciation reference

| model | raw spelling | raw pron | gap | nopunct spelling | nopunct pron | gap | kocer spelling | kocer pron | gap |
|---|---|---|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | 8.71 | 9.67 | +0.96 | 6.53 | 7.39 | +0.85 | 6.32 | 6.14 | -0.18 |
| qwen3-asr-1.7b-ko-univa | 9.46 | 9.80 | +0.34 | 7.48 | 7.68 | +0.20 | 7.08 | 6.73 | -0.35 |
| qwen3-asr-1.7b | 12.58 | 12.03 | -0.56 | 9.66 | 8.89 | -0.77 | 8.63 | 8.60 | -0.03 |
| buzzasr-korean | 14.12 | 14.75 | +0.62 | 10.06 | 10.59 | +0.53 | 9.71 | 9.61 | -0.10 |
| whisper-large-v3 | 17.58 | 18.29 | +0.71 | 11.84 | 12.50 | +0.66 | 11.55 | 11.62 | +0.07 |
| sensevoice-small-noitn | 20.03 | 20.18 | +0.15 | 13.91 | 14.10 | +0.19 | 13.46 | 13.28 | -0.19 |
| sensevoice-small-itn | 19.84 | 20.01 | +0.17 | 14.04 | 14.24 | +0.20 | 13.60 | 13.41 | -0.19 |

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
| qwen3-asr-1.7b-ko-univa-release | 14264 | 3746 (26%) | 2876 (20%) | 248 (2%) | 36 (0%) | 7358 (52%) |
| qwen3-asr-1.7b-ko-univa | 15489 | 3796 (25%) | 2946 (19%) | 468 (3%) | 22 (0%) | 8257 (53%) |
| qwen3-asr-1.7b | 20611 | 4754 (23%) | 4552 (22%) | 1202 (6%) | 352 (2%) | 9751 (47%) |
| buzzasr-korean | 23135 | 5792 (25%) | 5570 (24%) | 418 (2%) | 558 (2%) | 10797 (47%) |
| whisper-large-v3 | 28801 | 10875 (38%) | 4075 (14%) | 346 (1%) | 1006 (3%) | 12499 (43%) |
| sensevoice-small-noitn | 32805 | 11115 (34%) | 5415 (17%) | 525 (2%) | 392 (1%) | 15358 (47%) |
| sensevoice-small-itn | 32496 | 11172 (34%) | 4902 (15%) | 512 (2%) | 408 (1%) | 15502 (48%) |

## Pairwise paired bootstrap, kocer level — KsponSpeech only (spelling ref), n=6000. CER(row) - CER(col), %p, 95% CI, * = excludes 0

| | qwen3-asr-1.7b-k | qwen3-asr-1.7b-k | qwen3-asr-1.7b | buzzasr-korean | whisper-large-v3 | sensevoice-small | sensevoice-small |
|---|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-k | . | -0.76 [-0.89,-0.63]* | -2.31 [-2.48,-2.15]* | -3.39 [-4.31,-2.73]* | -5.23 [-6.11,-4.65]* | -7.14 [-7.39,-6.91]* | -7.28 [-7.53,-7.04]* |
| qwen3-asr-1.7b-k | +0.76 [+0.63,+0.89]* | . | -1.56 [-1.74,-1.39]* | -2.63 [-3.57,-1.96]* | -4.47 [-5.33,-3.89]* | -6.39 [-6.63,-6.15]* | -6.52 [-6.76,-6.28]* |
| qwen3-asr-1.7b | +2.31 [+2.15,+2.48]* | +1.56 [+1.39,+1.74]* | . | -1.07 [-2.00,-0.42]* | -2.91 [-3.79,-2.35]* | -4.83 [-5.07,-4.60]* | -4.96 [-5.21,-4.73]* |
| buzzasr-korean | +3.39 [+2.73,+4.31]* | +2.63 [+1.96,+3.57]* | +1.07 [+0.42,+2.00]* | . | -1.84 [-2.91,-0.76]* | -3.76 [-4.43,-2.81]* | -3.89 [-4.57,-2.96]* |
| whisper-large-v3 | +5.23 [+4.65,+6.11]* | +4.47 [+3.89,+5.33]* | +2.91 [+2.35,+3.79]* | +1.84 [+0.76,+2.91]* | . | -1.92 [-2.49,-1.04]* | -2.05 [-2.62,-1.18]* |
| sensevoice-small | +7.14 [+6.91,+7.39]* | +6.39 [+6.15,+6.63]* | +4.83 [+4.60,+5.07]* | +3.76 [+2.81,+4.43]* | +1.92 [+1.04,+2.49]* | . | -0.14 [-0.20,-0.07]* |
| sensevoice-small | +7.28 [+7.04,+7.53]* | +6.52 [+6.28,+6.76]* | +4.96 [+4.73,+5.21]* | +3.89 [+2.96,+4.57]* | +2.05 [+1.18,+2.62]* | +0.14 [+0.07,+0.20]* | . |

Rank intervals: qwen3-asr-1.7b-ko-univa-release [1, 1] P(1st)=1.00; qwen3-asr-1.7b-ko-univa [2, 2] P(1st)=0.00; qwen3-asr-1.7b [3, 3] P(1st)=0.00; buzzasr-korean [4, 4] P(1st)=0.00; whisper-large-v3 [5, 5] P(1st)=0.00; sensevoice-small-noitn [6, 6] P(1st)=0.00; sensevoice-small-itn [7, 7] P(1st)=0.00

## Pairwise paired bootstrap, kocer level — Kspon + Zeroth + FLEURS + CV27 (spelling ref for Kspon), n=7418. CER(row) - CER(col), %p, 95% CI, * = excludes 0

| | qwen3-asr-1.7b-k | qwen3-asr-1.7b-k | qwen3-asr-1.7b | buzzasr-korean | whisper-large-v3 | sensevoice-small | sensevoice-small |
|---|---|---|---|---|---|---|---|
| qwen3-asr-1.7b-k | . | -0.56 [-0.65,-0.46]* | -1.75 [-1.88,-1.62]* | -2.39 [-3.13,-1.93]* | -3.76 [-4.40,-3.33]* | -5.60 [-5.81,-5.40]* | -5.69 [-5.90,-5.49]* |
| qwen3-asr-1.7b-k | +0.56 [+0.46,+0.65]* | . | -1.19 [-1.33,-1.05]* | -1.83 [-2.58,-1.37]* | -3.20 [-3.85,-2.79]* | -5.04 [-5.25,-4.85]* | -5.14 [-5.35,-4.94]* |
| qwen3-asr-1.7b | +1.75 [+1.62,+1.88]* | +1.19 [+1.05,+1.33]* | . | -0.64 [-1.39,-0.17]* | -2.01 [-2.64,-1.60]* | -3.85 [-4.06,-3.65]* | -3.94 [-4.15,-3.75]* |
| buzzasr-korean | +2.39 [+1.93,+3.13]* | +1.83 [+1.37,+2.58]* | +0.64 [+0.17,+1.39]* | . | -1.37 [-2.15,-0.57]* | -3.21 [-3.69,-2.47]* | -3.30 [-3.78,-2.56]* |
| whisper-large-v3 | +3.76 [+3.33,+4.40]* | +3.20 [+2.79,+3.85]* | +2.01 [+1.60,+2.64]* | +1.37 [+0.57,+2.15]* | . | -1.84 [-2.26,-1.20]* | -1.93 [-2.35,-1.28]* |
| sensevoice-small | +5.60 [+5.40,+5.81]* | +5.04 [+4.85,+5.25]* | +3.85 [+3.65,+4.06]* | +3.21 [+2.47,+3.69]* | +1.84 [+1.20,+2.26]* | . | -0.10 [-0.14,-0.05]* |
| sensevoice-small | +5.69 [+5.49,+5.90]* | +5.14 [+4.94,+5.35]* | +3.94 [+3.75,+4.15]* | +3.30 [+2.56,+3.78]* | +1.93 [+1.28,+2.35]* | +0.10 [+0.05,+0.14]* | . |

Rank intervals: qwen3-asr-1.7b-ko-univa-release [1, 1] P(1st)=1.00; qwen3-asr-1.7b-ko-univa [2, 2] P(1st)=0.00; qwen3-asr-1.7b [3, 3] P(1st)=0.00; buzzasr-korean [4, 4] P(1st)=0.00; whisper-large-v3 [5, 5] P(1st)=0.00; sensevoice-small-noitn [6, 6] P(1st)=0.00; sensevoice-small-itn [7, 7] P(1st)=0.00
