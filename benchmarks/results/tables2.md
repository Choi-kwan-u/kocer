
## zeroth: CER (%) at each normalization level

| model | raw | nospace | nospace+punct | kocer | nlptutti std (check) | ref chars raw / kocer |
|---|---|---|---|---|---|---|
| buzzasr-korean | 7.60 | 5.87 | 5.85 | 3.16 | 5.85 | 25472 / 19288 |
| qwen3-asr-1.7b | 7.60 | 6.35 | 3.73 | 2.91 | 3.72 | 25472 / 19288 |
| qwen3-asr-1.7b-ko-univa | 9.28 | 8.55 | 5.44 | 2.46 | 5.45 | 25472 / 19288 |
| sensevoice-small-itn | 4.27 | 4.88 | 2.40 | 2.40 | 2.40 | 25472 / 19288 |
| sensevoice-small-noitn | 2.39 | 2.41 | 2.41 | 2.41 | 2.41 | 25472 / 19288 |
| whisper-large-v3 | 8.60 | 5.44 | 4.27 | 2.93 | 4.27 | 25472 / 19288 |

## fleurs: CER (%) at each normalization level

| model | raw | nospace | nospace+punct | kocer | nlptutti std (check) | ref chars raw / kocer |
|---|---|---|---|---|---|---|
| buzzasr-korean | 8.38 | 9.54 | 4.79 | 4.72 | 4.76 | 23888 / 17707 |
| qwen3-asr-1.7b | 6.08 | 6.53 | 4.56 | 4.31 | 4.54 | 23888 / 17711 |
| qwen3-asr-1.7b-ko-univa | 6.20 | 6.43 | 4.40 | 4.31 | 4.38 | 23888 / 17710 |
| sensevoice-small-itn | 10.38 | 10.74 | 8.46 | 6.95 | 8.44 | 23888 / 17724 |
| sensevoice-small-noitn | 12.05 | 12.95 | 8.41 | 6.91 | 8.39 | 23888 / 17724 |
| whisper-large-v3 | 8.94 | 7.77 | 5.00 | 4.37 | 4.98 | 23888 / 17709 |

## overall: CER (%) at each normalization level

| model | raw | nospace | nospace+punct | kocer | nlptutti std (check) | ref chars raw / kocer |
|---|---|---|---|---|---|---|
| buzzasr-korean | 7.98 | 7.68 | 5.34 | 3.91 | - | 49360 / 36995 |
| qwen3-asr-1.7b | 6.86 | 6.44 | 4.13 | 3.58 | - | 49360 / 36999 |
| qwen3-asr-1.7b-ko-univa | 7.79 | 7.51 | 4.94 | 3.35 | - | 49360 / 36998 |
| sensevoice-small-itn | 7.23 | 7.76 | 5.30 | 4.57 | - | 49360 / 37012 |
| sensevoice-small-noitn | 7.07 | 7.59 | 5.28 | 4.57 | - | 49360 / 37012 |
| whisper-large-v3 | 8.77 | 6.59 | 4.62 | 3.62 | - | 49360 / 36997 |

## zeroth: where the raw errors go (counts; share of raw error count)

| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | remaining (kocer errors) | fake share (count) |
|---|---|---|---|---|---|---|
| buzzasr-korean | 1937 | 804 (42%) | 4 (0%) | 519 (27%) | 610 (31%) | 69% |
| qwen3-asr-1.7b | 1935 | 710 (37%) | 505 (26%) | 158 (8%) | 562 (29%) | 71% |
| qwen3-asr-1.7b-ko-univa | 2364 | 715 (30%) | 599 (25%) | 575 (24%) | 475 (20%) | 80% |
| sensevoice-small-itn | 1087 | 145 (13%) | 480 (44%) | 0 (0%) | 462 (43%) | 57% |
| sensevoice-small-noitn | 609 | 144 (24%) | 0 (0%) | 0 (0%) | 465 (76%) | 24% |
| whisper-large-v3 | 2191 | 1142 (52%) | 226 (10%) | 258 (12%) | 565 (26%) | 74% |

## fleurs: where the raw errors go (counts; share of raw error count)

| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | remaining (kocer errors) | fake share (count) |
|---|---|---|---|---|---|---|
| buzzasr-korean | 2001 | 223 (11%) | 931 (47%) | 11 (1%) | 836 (42%) | 58% |
| qwen3-asr-1.7b | 1453 | 237 (16%) | 410 (28%) | 43 (3%) | 763 (53%) | 47% |
| qwen3-asr-1.7b-ko-univa | 1482 | 284 (19%) | 420 (28%) | 15 (1%) | 763 (51%) | 49% |
| sensevoice-small-itn | 2480 | 480 (19%) | 504 (20%) | 265 (11%) | 1231 (50%) | 50% |
| sensevoice-small-noitn | 2879 | 467 (16%) | 924 (32%) | 263 (9%) | 1225 (43%) | 57% |
| whisper-large-v3 | 2136 | 688 (32%) | 563 (26%) | 111 (5%) | 774 (36%) | 64% |

## overall: where the raw errors go (counts; share of raw error count)

| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | remaining (kocer errors) | fake share (count) |
|---|---|---|---|---|---|---|
| buzzasr-korean | 3938 | 1027 (26%) | 935 (24%) | 530 (13%) | 1446 (37%) | 63% |
| qwen3-asr-1.7b | 3388 | 947 (28%) | 915 (27%) | 201 (6%) | 1325 (39%) | 61% |
| qwen3-asr-1.7b-ko-univa | 3846 | 999 (26%) | 1019 (26%) | 590 (15%) | 1238 (32%) | 68% |
| sensevoice-small-itn | 3567 | 625 (18%) | 984 (28%) | 265 (7%) | 1693 (47%) | 53% |
| sensevoice-small-noitn | 3488 | 611 (18%) | 924 (26%) | 263 (8%) | 1690 (48%) | 52% |
| whisper-large-v3 | 4327 | 1830 (42%) | 789 (18%) | 369 (9%) | 1339 (31%) | 69% |

## Overall rank at each level (pooled Zeroth+FLEURS)

| model | raw | nospace | nopunct | kocer |
|---|---|---|---|---|
| buzzasr-korean | 7.98 (5) | 7.68 (5) | 5.34 (6) | 3.91 (4) |
| qwen3-asr-1.7b | 6.86 (1) | 6.44 (1) | 4.13 (1) | 3.58 (2) |
| qwen3-asr-1.7b-ko-univa | 7.79 (4) | 7.51 (3) | 4.94 (3) | 3.35 (1) |
| sensevoice-small-itn | 7.23 (3) | 7.76 (6) | 5.30 (5) | 4.57 (6) |
| sensevoice-small-noitn | 7.07 (2) | 7.59 (4) | 5.28 (4) | 4.57 (5) |
| whisper-large-v3 | 8.77 (6) | 6.59 (2) | 4.62 (2) | 3.62 (3) |

## Pairwise paired bootstrap, level = raw (overall; 2000 resamples, seed 0). Cell = CER(row) - CER(col) in %p, 95% CI; * = CI excludes 0

| | buzzasr-korean | qwen3-asr-1.7b | qwen3-asr-1.7b | sensevoice-sma | sensevoice-sma | whisper-large- |
|---|---|---|---|---|---|---|
| buzzasr-korean | . | +1.11 [+0.79,+1.42]* | +0.19 [-0.07,+0.45] | +0.75 [+0.23,+1.28]* | +0.91 [+0.34,+1.50]* | -0.79 [-1.12,-0.46]* |
| qwen3-asr-1.7b | -1.11 [-1.42,-0.79]* | . | -0.93 [-1.20,-0.65]* | -0.36 [-0.89,+0.16] | -0.20 [-0.79,+0.39] | -1.90 [-2.23,-1.57]* |
| qwen3-asr-1.7b | -0.19 [-0.45,+0.07] | +0.93 [+0.65,+1.20]* | . | +0.57 [-0.06,+1.18] | +0.73 [+0.04,+1.41]* | -0.97 [-1.33,-0.61]* |
| sensevoice-sma | -0.75 [-1.28,-0.23]* | +0.36 [-0.16,+0.89] | -0.57 [-1.18,+0.06] | . | +0.16 [+0.02,+0.29]* | -1.54 [-2.02,-1.07]* |
| sensevoice-sma | -0.91 [-1.50,-0.34]* | +0.20 [-0.39,+0.79] | -0.73 [-1.41,-0.04]* | -0.16 [-0.29,-0.02]* | . | -1.70 [-2.25,-1.16]* |
| whisper-large- | +0.79 [+0.46,+1.12]* | +1.90 [+1.57,+2.23]* | +0.97 [+0.61,+1.33]* | +1.54 [+1.07,+2.02]* | +1.70 [+1.16,+2.25]* | . |

Rank distribution at level raw: P(rank 1), median rank, 95% rank interval
- buzzasr-korean: P(1st)=0.00, median=5, 95% [4, 5]
- qwen3-asr-1.7b: P(1st)=0.74, median=1, 95% [1, 3]
- qwen3-asr-1.7b-ko-univa: P(1st)=0.00, median=4, 95% [3, 5]
- sensevoice-small-itn: P(1st)=0.00, median=3, 95% [2, 4]
- sensevoice-small-noitn: P(1st)=0.26, median=2, 95% [1, 3]
- whisper-large-v3: P(1st)=0.00, median=6, 95% [6, 6]

## Pairwise paired bootstrap, level = nopunct (overall; 2000 resamples, seed 0). Cell = CER(row) - CER(col) in %p, 95% CI; * = CI excludes 0

| | buzzasr-korean | qwen3-asr-1.7b | qwen3-asr-1.7b | sensevoice-sma | sensevoice-sma | whisper-large- |
|---|---|---|---|---|---|---|
| buzzasr-korean | . | +1.22 [+0.87,+1.56]* | +0.40 [+0.17,+0.65]* | +0.05 [-0.44,+0.55] | +0.06 [-0.41,+0.56] | +0.72 [+0.40,+1.04]* |
| qwen3-asr-1.7b | -1.22 [-1.56,-0.87]* | . | -0.82 [-1.13,-0.51]* | -1.17 [-1.59,-0.73]* | -1.15 [-1.58,-0.73]* | -0.49 [-0.79,-0.20]* |
| qwen3-asr-1.7b | -0.40 [-0.65,-0.17]* | +0.82 [+0.51,+1.13]* | . | -0.35 [-0.87,+0.18] | -0.34 [-0.85,+0.19] | +0.32 [+0.01,+0.64]* |
| sensevoice-sma | -0.05 [-0.55,+0.44] | +1.17 [+0.73,+1.59]* | +0.35 [-0.18,+0.87] | . | +0.01 [-0.03,+0.05] | +0.68 [+0.23,+1.09]* |
| sensevoice-sma | -0.06 [-0.56,+0.41] | +1.15 [+0.73,+1.58]* | +0.34 [-0.19,+0.85] | -0.01 [-0.05,+0.03] | . | +0.66 [+0.23,+1.07]* |
| whisper-large- | -0.72 [-1.04,-0.40]* | +0.49 [+0.20,+0.79]* | -0.32 [-0.64,-0.01]* | -0.68 [-1.09,-0.23]* | -0.66 [-1.07,-0.23]* | . |

Rank distribution at level nopunct: P(rank 1), median rank, 95% rank interval
- buzzasr-korean: P(1st)=0.00, median=6, 95% [4, 6]
- qwen3-asr-1.7b: P(1st)=1.00, median=1, 95% [1, 1]
- qwen3-asr-1.7b-ko-univa: P(1st)=0.00, median=3, 95% [3, 5]
- sensevoice-small-itn: P(1st)=0.00, median=5, 95% [3, 6]
- sensevoice-small-noitn: P(1st)=0.00, median=5, 95% [3, 6]
- whisper-large-v3: P(1st)=0.00, median=2, 95% [2, 2]

## Pairwise paired bootstrap, level = kocer (overall; 2000 resamples, seed 0). Cell = CER(row) - CER(col) in %p, 95% CI; * = CI excludes 0

| | buzzasr-korean | qwen3-asr-1.7b | qwen3-asr-1.7b | sensevoice-sma | sensevoice-sma | whisper-large- |
|---|---|---|---|---|---|---|
| buzzasr-korean | . | +0.33 [+0.10,+0.56]* | +0.56 [+0.35,+0.78]* | -0.67 [-0.94,-0.36]* | -0.66 [-0.93,-0.35]* | +0.29 [+0.13,+0.46]* |
| qwen3-asr-1.7b | -0.33 [-0.56,-0.10]* | . | +0.24 [+0.08,+0.39]* | -0.99 [-1.28,-0.70]* | -0.98 [-1.28,-0.69]* | -0.04 [-0.23,+0.15] |
| qwen3-asr-1.7b | -0.56 [-0.78,-0.35]* | -0.24 [-0.39,-0.08]* | . | -1.23 [-1.50,-0.94]* | -1.22 [-1.49,-0.93]* | -0.27 [-0.45,-0.11]* |
| sensevoice-sma | +0.67 [+0.36,+0.94]* | +0.99 [+0.70,+1.28]* | +1.23 [+0.94,+1.50]* | . | +0.01 [-0.04,+0.05] | +0.95 [+0.67,+1.23]* |
| sensevoice-sma | +0.66 [+0.35,+0.93]* | +0.98 [+0.69,+1.28]* | +1.22 [+0.93,+1.49]* | -0.01 [-0.05,+0.04] | . | +0.95 [+0.67,+1.22]* |
| whisper-large- | -0.29 [-0.46,-0.13]* | +0.04 [-0.15,+0.23] | +0.27 [+0.11,+0.45]* | -0.95 [-1.23,-0.67]* | -0.95 [-1.22,-0.67]* | . |

Rank distribution at level kocer: P(rank 1), median rank, 95% rank interval
- buzzasr-korean: P(1st)=0.00, median=4, 95% [4, 4]
- qwen3-asr-1.7b: P(1st)=0.00, median=2, 95% [2, 3]
- qwen3-asr-1.7b-ko-univa: P(1st)=1.00, median=1, 95% [1, 1]
- sensevoice-small-itn: P(1st)=0.00, median=6, 95% [5, 6]
- sensevoice-small-noitn: P(1st)=0.00, median=5, 95% [5, 6]
- whisper-large-v3: P(1st)=0.00, median=3, 95% [2, 3]
