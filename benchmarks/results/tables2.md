
## zeroth: CER (%) at each normalization level

| model | raw | nospace | nospace+punct | kocer | nlptutti std (check) | ref chars raw / kocer |
|---|---|---|---|---|---|---|
| buzzasr-korean | 7.60 | 5.87 | 5.85 | 3.08 | 5.85 | 25472 / 19288 |
| qwen3-asr-1.7b | 7.60 | 6.35 | 3.73 | 2.90 | 3.72 | 25472 / 19288 |
| qwen3-asr-1.7b-ko-univa | 9.28 | 8.55 | 5.44 | 2.42 | 5.45 | 25472 / 19288 |
| qwen3-asr-1.7b-ko-univa-release | 8.89 | 8.01 | 5.36 | 2.32 | 5.39 | 25472 / 19288 |
| sensevoice-small-itn | 4.27 | 4.88 | 2.40 | 2.40 | 2.40 | 25472 / 19288 |
| sensevoice-small-noitn | 2.39 | 2.41 | 2.41 | 2.41 | 2.41 | 25472 / 19288 |
| whisper-large-v3 | 6.88 | 5.44 | 4.27 | 2.90 | 4.27 | 25472 / 19288 |

## fleurs: CER (%) at each normalization level

| model | raw | nospace | nospace+punct | kocer | nlptutti std (check) | ref chars raw / kocer |
|---|---|---|---|---|---|---|
| buzzasr-korean | 8.37 | 9.54 | 4.79 | 4.28 | 4.76 | 23888 / 17690 |
| qwen3-asr-1.7b | 6.08 | 6.53 | 4.56 | 4.25 | 4.54 | 23888 / 17690 |
| qwen3-asr-1.7b-ko-univa | 6.20 | 6.43 | 4.40 | 4.25 | 4.38 | 23888 / 17690 |
| qwen3-asr-1.7b-ko-univa-release | 6.25 | 6.61 | 4.39 | 4.19 | 4.37 | 23888 / 17690 |
| sensevoice-small-itn | 10.38 | 10.74 | 8.46 | 6.81 | 8.44 | 23888 / 17690 |
| sensevoice-small-noitn | 12.05 | 12.95 | 8.41 | 6.76 | 8.39 | 23888 / 17690 |
| whisper-large-v3 | 7.44 | 7.77 | 5.00 | 4.24 | 4.98 | 23888 / 17690 |

## commonvoice: CER (%) at each normalization level

| model | raw | nospace | nospace+punct | kocer | nlptutti std (check) | ref chars raw / kocer |
|---|---|---|---|---|---|---|
| buzzasr-korean | 7.36 | 8.23 | 3.98 | 3.88 | 3.98 | 15473 / 11475 |
| qwen3-asr-1.7b | 7.32 | 7.59 | 6.68 | 6.61 | 6.68 | 15473 / 11475 |
| qwen3-asr-1.7b-ko-univa | 7.04 | 7.28 | 6.30 | 6.05 | 6.30 | 15473 / 11475 |
| qwen3-asr-1.7b-ko-univa-release | 6.85 | 7.00 | 6.18 | 5.97 | 6.18 | 15473 / 11475 |
| sensevoice-small-itn | 10.37 | 10.53 | 9.80 | 9.68 | 9.80 | 15473 / 11475 |
| sensevoice-small-noitn | 12.87 | 13.66 | 9.83 | 9.72 | 9.83 | 15473 / 11475 |
| whisper-large-v3 | 8.52 | 9.06 | 5.85 | 5.80 | 5.85 | 15473 / 11475 |

## overall: CER (%) at each normalization level

| model | raw | nospace | nospace+punct | kocer | nlptutti std (check) | ref chars raw / kocer |
|---|---|---|---|---|---|---|
| buzzasr-korean | 7.83 | 7.81 | 5.02 | 3.71 | - | 64833 / 48453 |
| qwen3-asr-1.7b | 6.97 | 6.72 | 4.73 | 4.27 | - | 64833 / 48453 |
| qwen3-asr-1.7b-ko-univa | 7.61 | 7.45 | 5.26 | 3.94 | - | 64833 / 48453 |
| qwen3-asr-1.7b-ko-univa-release | 7.43 | 7.24 | 5.20 | 3.87 | - | 64833 / 48453 |
| sensevoice-small-itn | 7.98 | 8.43 | 6.36 | 5.73 | - | 64833 / 48453 |
| sensevoice-small-noitn | 8.45 | 9.05 | 6.36 | 5.73 | - | 64833 / 48453 |
| whisper-large-v3 | 7.48 | 7.18 | 4.91 | 4.08 | - | 64833 / 48453 |

## zeroth: where the raw errors go (counts; share of raw error count)

| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | remaining (kocer errors) | fake share (count) |
|---|---|---|---|---|---|---|
| buzzasr-korean | 1937 | 804 (42%) | 4 (0%) | 535 (28%) | 594 (31%) | 69% |
| qwen3-asr-1.7b | 1935 | 710 (37%) | 505 (26%) | 160 (8%) | 560 (29%) | 71% |
| qwen3-asr-1.7b-ko-univa | 2364 | 715 (30%) | 599 (25%) | 584 (25%) | 466 (20%) | 80% |
| qwen3-asr-1.7b-ko-univa-release | 2264 | 719 (32%) | 511 (23%) | 586 (26%) | 448 (20%) | 80% |
| sensevoice-small-itn | 1087 | 145 (13%) | 480 (44%) | 0 (0%) | 462 (43%) | 57% |
| sensevoice-small-noitn | 609 | 144 (24%) | 0 (0%) | 0 (0%) | 465 (76%) | 24% |
| whisper-large-v3 | 1753 | 704 (40%) | 226 (13%) | 263 (15%) | 560 (32%) | 68% |

## fleurs: where the raw errors go (counts; share of raw error count)

| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | remaining (kocer errors) | fake share (count) |
|---|---|---|---|---|---|---|
| buzzasr-korean | 2000 | 222 (11%) | 931 (47%) | 90 (4%) | 757 (38%) | 62% |
| qwen3-asr-1.7b | 1453 | 237 (16%) | 410 (28%) | 55 (4%) | 751 (52%) | 48% |
| qwen3-asr-1.7b-ko-univa | 1482 | 284 (19%) | 420 (28%) | 27 (2%) | 751 (51%) | 49% |
| qwen3-asr-1.7b-ko-univa-release | 1492 | 261 (17%) | 455 (30%) | 35 (2%) | 741 (50%) | 50% |
| sensevoice-small-itn | 2480 | 480 (19%) | 504 (20%) | 292 (12%) | 1204 (49%) | 51% |
| sensevoice-small-noitn | 2879 | 467 (16%) | 924 (32%) | 293 (10%) | 1195 (42%) | 58% |
| whisper-large-v3 | 1777 | 329 (19%) | 563 (32%) | 135 (8%) | 750 (42%) | 58% |

## commonvoice: where the raw errors go (counts; share of raw error count)

| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | remaining (kocer errors) | fake share (count) |
|---|---|---|---|---|---|---|
| buzzasr-korean | 1139 | 151 (13%) | 531 (47%) | 12 (1%) | 445 (39%) | 61% |
| qwen3-asr-1.7b | 1133 | 221 (20%) | 146 (13%) | 7 (1%) | 759 (67%) | 33% |
| qwen3-asr-1.7b-ko-univa | 1089 | 215 (20%) | 151 (14%) | 29 (3%) | 694 (64%) | 36% |
| qwen3-asr-1.7b-ko-univa-release | 1060 | 220 (21%) | 131 (12%) | 24 (2%) | 685 (65%) | 35% |
| sensevoice-small-itn | 1604 | 339 (21%) | 140 (9%) | 14 (1%) | 1111 (69%) | 31% |
| sensevoice-small-noitn | 1991 | 351 (18%) | 512 (26%) | 13 (1%) | 1115 (56%) | 44% |
| whisper-large-v3 | 1319 | 231 (18%) | 417 (32%) | 6 (0%) | 665 (50%) | 50% |

## overall: where the raw errors go (counts; share of raw error count)

| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | remaining (kocer errors) | fake share (count) |
|---|---|---|---|---|---|---|
| buzzasr-korean | 5076 | 1177 (23%) | 1466 (29%) | 637 (13%) | 1796 (35%) | 65% |
| qwen3-asr-1.7b | 4521 | 1168 (26%) | 1061 (23%) | 222 (5%) | 2070 (46%) | 54% |
| qwen3-asr-1.7b-ko-univa | 4935 | 1214 (25%) | 1170 (24%) | 640 (13%) | 1911 (39%) | 61% |
| qwen3-asr-1.7b-ko-univa-release | 4816 | 1200 (25%) | 1097 (23%) | 645 (13%) | 1874 (39%) | 61% |
| sensevoice-small-itn | 5171 | 964 (19%) | 1124 (22%) | 306 (6%) | 2777 (54%) | 46% |
| sensevoice-small-noitn | 5479 | 962 (18%) | 1436 (26%) | 306 (6%) | 2775 (51%) | 49% |
| whisper-large-v3 | 4849 | 1264 (26%) | 1206 (25%) | 404 (8%) | 1975 (41%) | 59% |

## Overall rank at each level (pooled Zeroth+FLEURS)

| model | raw | nospace | nopunct | kocer |
|---|---|---|---|---|
| buzzasr-korean | 7.83 (5) | 7.81 (5) | 5.02 (3) | 3.71 (1) |
| qwen3-asr-1.7b | 6.97 (1) | 6.72 (1) | 4.73 (1) | 4.27 (5) |
| qwen3-asr-1.7b-ko-univa | 7.61 (4) | 7.45 (4) | 5.26 (5) | 3.94 (3) |
| qwen3-asr-1.7b-ko-univa-release | 7.43 (2) | 7.24 (3) | 5.20 (4) | 3.87 (2) |
| sensevoice-small-itn | 7.98 (6) | 8.43 (6) | 6.36 (7) | 5.73 (7) |
| sensevoice-small-noitn | 8.45 (7) | 9.05 (7) | 6.36 (6) | 5.73 (6) |
| whisper-large-v3 | 7.48 (3) | 7.18 (2) | 4.91 (2) | 4.08 (4) |

## Pairwise paired bootstrap, level = raw (overall; 2000 resamples, seed 0). Cell = CER(row) - CER(col) in %p, 95% CI; * = CI excludes 0

| | buzzasr-korean | qwen3-asr-1.7b | qwen3-asr-1.7b | qwen3-asr-1.7b | sensevoice-sma | sensevoice-sma | whisper-large- |
|---|---|---|---|---|---|---|---|
| buzzasr-korean | . | +0.86 [+0.58,+1.14]* | +0.22 [-0.02,+0.46] | +0.40 [+0.17,+0.63]* | -0.15 [-0.59,+0.30] | -0.62 [-1.10,-0.14]* | +0.35 [+0.09,+0.63]* |
| qwen3-asr-1.7b | -0.86 [-1.14,-0.58]* | . | -0.64 [-0.87,-0.41]* | -0.46 [-0.70,-0.20]* | -1.00 [-1.45,-0.59]* | -1.48 [-1.96,-1.01]* | -0.51 [-0.77,-0.21]* |
| qwen3-asr-1.7b | -0.22 [-0.46,+0.02] | +0.64 [+0.41,+0.87]* | . | +0.18 [+0.04,+0.34]* | -0.36 [-0.85,+0.13] | -0.84 [-1.39,-0.32]* | +0.13 [-0.17,+0.45] |
| qwen3-asr-1.7b | -0.40 [-0.63,-0.17]* | +0.46 [+0.20,+0.70]* | -0.18 [-0.34,-0.04]* | . | -0.55 [-1.02,-0.08]* | -1.02 [-1.54,-0.51]* | -0.05 [-0.33,+0.25] |
| sensevoice-sma | +0.15 [-0.30,+0.59] | +1.00 [+0.59,+1.45]* | +0.36 [-0.13,+0.85] | +0.55 [+0.08,+1.02]* | . | -0.48 [-0.61,-0.35]* | +0.50 [+0.12,+0.88]* |
| sensevoice-sma | +0.62 [+0.14,+1.10]* | +1.48 [+1.01,+1.96]* | +0.84 [+0.32,+1.39]* | +1.02 [+0.51,+1.54]* | +0.48 [+0.35,+0.61]* | . | +0.97 [+0.56,+1.41]* |
| whisper-large- | -0.35 [-0.63,-0.09]* | +0.51 [+0.21,+0.77]* | -0.13 [-0.45,+0.17] | +0.05 [-0.25,+0.33] | -0.50 [-0.88,-0.12]* | -0.97 [-1.41,-0.56]* | . |

Rank distribution at level raw: P(rank 1), median rank, 95% rank interval
- buzzasr-korean: P(1st)=0.00, median=5, 95% [4, 6]
- qwen3-asr-1.7b: P(1st)=1.00, median=1, 95% [1, 1]
- qwen3-asr-1.7b-ko-univa: P(1st)=0.00, median=4, 95% [3, 5]
- qwen3-asr-1.7b-ko-univa-release: P(1st)=0.00, median=2, 95% [2, 3]
- sensevoice-small-itn: P(1st)=0.00, median=6, 95% [4, 6]
- sensevoice-small-noitn: P(1st)=0.00, median=7, 95% [7, 7]
- whisper-large-v3: P(1st)=0.00, median=3, 95% [2, 4]

## Pairwise paired bootstrap, level = nopunct (overall; 2000 resamples, seed 0). Cell = CER(row) - CER(col) in %p, 95% CI; * = CI excludes 0

| | buzzasr-korean | qwen3-asr-1.7b | qwen3-asr-1.7b | qwen3-asr-1.7b | sensevoice-sma | sensevoice-sma | whisper-large- |
|---|---|---|---|---|---|---|---|
| buzzasr-korean | . | +0.29 [-0.02,+0.62] | -0.24 [-0.48,+0.00] | -0.18 [-0.41,+0.06] | -1.34 [-1.78,-0.92]* | -1.34 [-1.77,-0.92]* | +0.11 [-0.15,+0.39] |
| qwen3-asr-1.7b | -0.29 [-0.62,+0.02] | . | -0.53 [-0.80,-0.28]* | -0.47 [-0.74,-0.19]* | -1.63 [-2.00,-1.28]* | -1.63 [-2.00,-1.28]* | -0.18 [-0.44,+0.09] |
| qwen3-asr-1.7b | +0.24 [-0.00,+0.48] | +0.53 [+0.28,+0.80]* | . | +0.07 [-0.07,+0.20] | -1.10 [-1.52,-0.67]* | -1.09 [-1.51,-0.67]* | +0.35 [+0.09,+0.64]* |
| qwen3-asr-1.7b | +0.18 [-0.06,+0.41] | +0.47 [+0.19,+0.74]* | -0.07 [-0.20,+0.07] | . | -1.16 [-1.57,-0.75]* | -1.16 [-1.56,-0.75]* | +0.29 [+0.02,+0.57]* |
| sensevoice-sma | +1.34 [+0.92,+1.78]* | +1.63 [+1.28,+2.00]* | +1.10 [+0.67,+1.52]* | +1.16 [+0.75,+1.57]* | . | +0.00 [-0.04,+0.05] | +1.45 [+1.09,+1.81]* |
| sensevoice-sma | +1.34 [+0.92,+1.77]* | +1.63 [+1.28,+2.00]* | +1.09 [+0.67,+1.51]* | +1.16 [+0.75,+1.56]* | -0.00 [-0.05,+0.04] | . | +1.45 [+1.10,+1.81]* |
| whisper-large- | -0.11 [-0.39,+0.15] | +0.18 [-0.09,+0.44] | -0.35 [-0.64,-0.09]* | -0.29 [-0.57,-0.02]* | -1.45 [-1.81,-1.09]* | -1.45 [-1.81,-1.10]* | . |

Rank distribution at level nopunct: P(rank 1), median rank, 95% rank interval
- buzzasr-korean: P(1st)=0.02, median=3, 95% [2, 4]
- qwen3-asr-1.7b: P(1st)=0.89, median=1, 95% [1, 2]
- qwen3-asr-1.7b-ko-univa: P(1st)=0.00, median=5, 95% [4, 5]
- qwen3-asr-1.7b-ko-univa-release: P(1st)=0.00, median=4, 95% [3, 5]
- sensevoice-small-itn: P(1st)=0.00, median=7, 95% [6, 7]
- sensevoice-small-noitn: P(1st)=0.00, median=6, 95% [6, 7]
- whisper-large-v3: P(1st)=0.09, median=2, 95% [1, 3]

## Pairwise paired bootstrap, level = kocer (overall; 2000 resamples, seed 0). Cell = CER(row) - CER(col) in %p, 95% CI; * = CI excludes 0

| | buzzasr-korean | qwen3-asr-1.7b | qwen3-asr-1.7b | qwen3-asr-1.7b | sensevoice-sma | sensevoice-sma | whisper-large- |
|---|---|---|---|---|---|---|---|
| buzzasr-korean | . | -0.57 [-0.78,-0.35]* | -0.24 [-0.44,-0.03]* | -0.16 [-0.36,+0.04] | -2.02 [-2.33,-1.74]* | -2.02 [-2.32,-1.74]* | -0.37 [-0.52,-0.22]* |
| qwen3-asr-1.7b | +0.57 [+0.35,+0.78]* | . | +0.33 [+0.18,+0.48]* | +0.40 [+0.24,+0.57]* | -1.46 [-1.74,-1.19]* | -1.46 [-1.74,-1.19]* | +0.20 [+0.00,+0.40]* |
| qwen3-asr-1.7b | +0.24 [+0.03,+0.44]* | -0.33 [-0.48,-0.18]* | . | +0.08 [-0.05,+0.20] | -1.79 [-2.06,-1.53]* | -1.78 [-2.05,-1.53]* | -0.13 [-0.32,+0.05] |
| qwen3-asr-1.7b | +0.16 [-0.04,+0.36] | -0.40 [-0.57,-0.24]* | -0.08 [-0.20,+0.05] | . | -1.86 [-2.13,-1.60]* | -1.86 [-2.13,-1.60]* | -0.21 [-0.39,-0.03]* |
| sensevoice-sma | +2.02 [+1.74,+2.33]* | +1.46 [+1.19,+1.74]* | +1.79 [+1.53,+2.06]* | +1.86 [+1.60,+2.13]* | . | +0.00 [-0.04,+0.04] | +1.66 [+1.40,+1.93]* |
| sensevoice-sma | +2.02 [+1.74,+2.32]* | +1.46 [+1.19,+1.74]* | +1.78 [+1.53,+2.05]* | +1.86 [+1.60,+2.13]* | -0.00 [-0.04,+0.04] | . | +1.65 [+1.39,+1.93]* |
| whisper-large- | +0.37 [+0.22,+0.52]* | -0.20 [-0.40,-0.00]* | +0.13 [-0.05,+0.32] | +0.21 [+0.03,+0.39]* | -1.66 [-1.93,-1.40]* | -1.65 [-1.93,-1.39]* | . |

Rank distribution at level kocer: P(rank 1), median rank, 95% rank interval
- buzzasr-korean: P(1st)=0.94, median=1, 95% [1, 2]
- qwen3-asr-1.7b: P(1st)=0.00, median=5, 95% [4, 5]
- qwen3-asr-1.7b-ko-univa: P(1st)=0.00, median=3, 95% [2, 4]
- qwen3-asr-1.7b-ko-univa-release: P(1st)=0.06, median=2, 95% [1, 3]
- sensevoice-small-itn: P(1st)=0.00, median=7, 95% [6, 7]
- sensevoice-small-noitn: P(1st)=0.00, median=6, 95% [6, 7]
- whisper-large-v3: P(1st)=0.00, median=4, 95% [3, 4]
