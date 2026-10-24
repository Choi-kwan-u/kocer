
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

## commonvoice: CER (%) at each normalization level

| model | raw | nospace | nospace+punct | kocer | nlptutti std (check) | ref chars raw / kocer |
|---|---|---|---|---|---|---|
| buzzasr-korean | 7.36 | 8.23 | 3.98 | 3.88 | 3.98 | 15473 / 11475 |
| qwen3-asr-1.7b | 7.32 | 7.59 | 6.68 | 6.61 | 6.68 | 15473 / 11475 |
| qwen3-asr-1.7b-ko-univa | 7.04 | 7.28 | 6.30 | 6.08 | 6.30 | 15473 / 11475 |
| sensevoice-small-itn | 10.37 | 10.53 | 9.80 | 9.68 | 9.80 | 15473 / 11475 |
| sensevoice-small-noitn | 12.87 | 13.66 | 9.83 | 9.72 | 9.83 | 15473 / 11475 |
| whisper-large-v3 | 12.17 | 9.06 | 5.85 | 5.80 | 5.85 | 15473 / 11475 |

## overall: CER (%) at each normalization level

| model | raw | nospace | nospace+punct | kocer | nlptutti std (check) | ref chars raw / kocer |
|---|---|---|---|---|---|---|
| buzzasr-korean | 7.83 | 7.81 | 5.02 | 3.90 | - | 64833 / 48470 |
| qwen3-asr-1.7b | 6.97 | 6.72 | 4.73 | 4.30 | - | 64833 / 48474 |
| qwen3-asr-1.7b-ko-univa | 7.61 | 7.45 | 5.26 | 3.99 | - | 64833 / 48473 |
| sensevoice-small-itn | 7.98 | 8.43 | 6.36 | 5.78 | - | 64833 / 48487 |
| sensevoice-small-noitn | 8.45 | 9.05 | 6.36 | 5.79 | - | 64833 / 48487 |
| whisper-large-v3 | 9.58 | 7.18 | 4.91 | 4.13 | - | 64833 / 48472 |

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

## commonvoice: where the raw errors go (counts; share of raw error count)

| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | remaining (kocer errors) | fake share (count) |
|---|---|---|---|---|---|---|
| buzzasr-korean | 1139 | 151 (13%) | 531 (47%) | 12 (1%) | 445 (39%) | 61% |
| qwen3-asr-1.7b | 1133 | 221 (20%) | 146 (13%) | 7 (1%) | 759 (67%) | 33% |
| qwen3-asr-1.7b-ko-univa | 1089 | 215 (20%) | 151 (14%) | 25 (2%) | 698 (64%) | 36% |
| sensevoice-small-itn | 1604 | 339 (21%) | 140 (9%) | 14 (1%) | 1111 (69%) | 31% |
| sensevoice-small-noitn | 1991 | 351 (18%) | 512 (26%) | 13 (1%) | 1115 (56%) | 44% |
| whisper-large-v3 | 1883 | 795 (42%) | 417 (22%) | 6 (0%) | 665 (35%) | 65% |

## overall: where the raw errors go (counts; share of raw error count)

| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | remaining (kocer errors) | fake share (count) |
|---|---|---|---|---|---|---|
| buzzasr-korean | 5077 | 1178 (23%) | 1466 (29%) | 542 (11%) | 1891 (37%) | 63% |
| qwen3-asr-1.7b | 4521 | 1168 (26%) | 1061 (23%) | 208 (5%) | 2084 (46%) | 54% |
| qwen3-asr-1.7b-ko-univa | 4935 | 1214 (25%) | 1170 (24%) | 615 (12%) | 1936 (39%) | 61% |
| sensevoice-small-itn | 5171 | 964 (19%) | 1124 (22%) | 279 (5%) | 2804 (54%) | 46% |
| sensevoice-small-noitn | 5479 | 962 (18%) | 1436 (26%) | 276 (5%) | 2805 (51%) | 49% |
| whisper-large-v3 | 6210 | 2625 (42%) | 1206 (19%) | 375 (6%) | 2004 (32%) | 68% |

## Overall rank at each level (pooled Zeroth+FLEURS)

| model | raw | nospace | nopunct | kocer |
|---|---|---|---|---|
| buzzasr-korean | 7.83 (3) | 7.81 (4) | 5.02 (3) | 3.90 (1) |
| qwen3-asr-1.7b | 6.97 (1) | 6.72 (1) | 4.73 (1) | 4.30 (4) |
| qwen3-asr-1.7b-ko-univa | 7.61 (2) | 7.45 (3) | 5.26 (4) | 3.99 (2) |
| sensevoice-small-itn | 7.98 (4) | 8.43 (5) | 6.36 (6) | 5.78 (5) |
| sensevoice-small-noitn | 8.45 (5) | 9.05 (6) | 6.36 (5) | 5.79 (6) |
| whisper-large-v3 | 9.58 (6) | 7.18 (2) | 4.91 (2) | 4.13 (3) |

## Pairwise paired bootstrap, level = raw (overall; 2000 resamples, seed 0). Cell = CER(row) - CER(col) in %p, 95% CI; * = CI excludes 0

| | buzzasr-korean | qwen3-asr-1.7b | qwen3-asr-1.7b | sensevoice-sma | sensevoice-sma | whisper-large- |
|---|---|---|---|---|---|---|
| buzzasr-korean | . | +0.86 [+0.58,+1.14]* | +0.22 [-0.02,+0.46] | -0.14 [-0.58,+0.30] | -0.62 [-1.10,-0.14]* | -1.75 [-2.03,-1.45]* |
| qwen3-asr-1.7b | -0.86 [-1.14,-0.58]* | . | -0.64 [-0.87,-0.41]* | -1.00 [-1.45,-0.59]* | -1.48 [-1.96,-1.01]* | -2.61 [-2.89,-2.31]* |
| qwen3-asr-1.7b | -0.22 [-0.46,+0.02] | +0.64 [+0.41,+0.87]* | . | -0.36 [-0.85,+0.13] | -0.84 [-1.39,-0.32]* | -1.97 [-2.28,-1.65]* |
| sensevoice-sma | +0.14 [-0.30,+0.58] | +1.00 [+0.59,+1.45]* | +0.36 [-0.13,+0.85] | . | -0.48 [-0.61,-0.35]* | -1.60 [-1.99,-1.21]* |
| sensevoice-sma | +0.62 [+0.14,+1.10]* | +1.48 [+1.01,+1.96]* | +0.84 [+0.32,+1.39]* | +0.48 [+0.35,+0.61]* | . | -1.13 [-1.55,-0.70]* |
| whisper-large- | +1.75 [+1.45,+2.03]* | +2.61 [+2.31,+2.89]* | +1.97 [+1.65,+2.28]* | +1.60 [+1.21,+1.99]* | +1.13 [+0.70,+1.55]* | . |

Rank distribution at level raw: P(rank 1), median rank, 95% rank interval
- buzzasr-korean: P(1st)=0.00, median=3, 95% [2, 4]
- qwen3-asr-1.7b: P(1st)=1.00, median=1, 95% [1, 1]
- qwen3-asr-1.7b-ko-univa: P(1st)=0.00, median=2, 95% [2, 3]
- sensevoice-small-itn: P(1st)=0.00, median=4, 95% [2, 4]
- sensevoice-small-noitn: P(1st)=0.00, median=5, 95% [5, 5]
- whisper-large-v3: P(1st)=0.00, median=6, 95% [6, 6]

## Pairwise paired bootstrap, level = nopunct (overall; 2000 resamples, seed 0). Cell = CER(row) - CER(col) in %p, 95% CI; * = CI excludes 0

| | buzzasr-korean | qwen3-asr-1.7b | qwen3-asr-1.7b | sensevoice-sma | sensevoice-sma | whisper-large- |
|---|---|---|---|---|---|---|
| buzzasr-korean | . | +0.29 [-0.02,+0.62] | -0.24 [-0.48,+0.00] | -1.34 [-1.78,-0.92]* | -1.34 [-1.77,-0.92]* | +0.11 [-0.15,+0.39] |
| qwen3-asr-1.7b | -0.29 [-0.62,+0.02] | . | -0.53 [-0.80,-0.28]* | -1.63 [-2.00,-1.28]* | -1.63 [-2.00,-1.28]* | -0.18 [-0.44,+0.09] |
| qwen3-asr-1.7b | +0.24 [-0.00,+0.48] | +0.53 [+0.28,+0.80]* | . | -1.10 [-1.52,-0.67]* | -1.09 [-1.51,-0.67]* | +0.35 [+0.09,+0.64]* |
| sensevoice-sma | +1.34 [+0.92,+1.78]* | +1.63 [+1.28,+2.00]* | +1.10 [+0.67,+1.52]* | . | +0.00 [-0.04,+0.05] | +1.45 [+1.09,+1.81]* |
| sensevoice-sma | +1.34 [+0.92,+1.77]* | +1.63 [+1.28,+2.00]* | +1.09 [+0.67,+1.51]* | -0.00 [-0.05,+0.04] | . | +1.45 [+1.10,+1.81]* |
| whisper-large- | -0.11 [-0.39,+0.15] | +0.18 [-0.09,+0.44] | -0.35 [-0.64,-0.09]* | -1.45 [-1.81,-1.09]* | -1.45 [-1.81,-1.10]* | . |

Rank distribution at level nopunct: P(rank 1), median rank, 95% rank interval
- buzzasr-korean: P(1st)=0.02, median=3, 95% [2, 4]
- qwen3-asr-1.7b: P(1st)=0.89, median=1, 95% [1, 2]
- qwen3-asr-1.7b-ko-univa: P(1st)=0.00, median=4, 95% [3, 4]
- sensevoice-small-itn: P(1st)=0.00, median=6, 95% [5, 6]
- sensevoice-small-noitn: P(1st)=0.00, median=5, 95% [5, 6]
- whisper-large-v3: P(1st)=0.09, median=2, 95% [1, 3]

## Pairwise paired bootstrap, level = kocer (overall; 2000 resamples, seed 0). Cell = CER(row) - CER(col) in %p, 95% CI; * = CI excludes 0

| | buzzasr-korean | qwen3-asr-1.7b | qwen3-asr-1.7b | sensevoice-sma | sensevoice-sma | whisper-large- |
|---|---|---|---|---|---|---|
| buzzasr-korean | . | -0.40 [-0.64,-0.16]* | -0.09 [-0.32,+0.13] | -1.88 [-2.20,-1.60]* | -1.88 [-2.20,-1.60]* | -0.23 [-0.40,-0.06]* |
| qwen3-asr-1.7b | +0.40 [+0.16,+0.64]* | . | +0.31 [+0.15,+0.46]* | -1.48 [-1.76,-1.22]* | -1.49 [-1.77,-1.23]* | +0.16 [-0.03,+0.37] |
| qwen3-asr-1.7b | +0.09 [-0.13,+0.32] | -0.31 [-0.46,-0.15]* | . | -1.79 [-2.06,-1.54]* | -1.79 [-2.07,-1.54]* | -0.14 [-0.33,+0.04] |
| sensevoice-sma | +1.88 [+1.60,+2.20]* | +1.48 [+1.22,+1.76]* | +1.79 [+1.54,+2.06]* | . | -0.00 [-0.05,+0.04] | +1.65 [+1.39,+1.92]* |
| sensevoice-sma | +1.88 [+1.60,+2.20]* | +1.49 [+1.23,+1.77]* | +1.79 [+1.54,+2.07]* | +0.00 [-0.04,+0.05] | . | +1.65 [+1.40,+1.92]* |
| whisper-large- | +0.23 [+0.06,+0.40]* | -0.16 [-0.37,+0.03] | +0.14 [-0.04,+0.33] | -1.65 [-1.92,-1.39]* | -1.65 [-1.92,-1.40]* | . |

Rank distribution at level kocer: P(rank 1), median rank, 95% rank interval
- buzzasr-korean: P(1st)=0.80, median=1, 95% [1, 2]
- qwen3-asr-1.7b: P(1st)=0.00, median=4, 95% [3, 4]
- qwen3-asr-1.7b-ko-univa: P(1st)=0.20, median=2, 95% [1, 3]
- sensevoice-small-itn: P(1st)=0.00, median=5, 95% [5, 6]
- sensevoice-small-noitn: P(1st)=0.00, median=6, 95% [5, 6]
- whisper-large-v3: P(1st)=0.00, median=3, 95% [2, 4]
