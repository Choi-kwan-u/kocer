
## zeroth: 152 utterances with numbers

| model | nospace+punct CER | kocer CER | drop | rank nopunct -> kocer |
|---|---|---|---|---|
| sensevoice-small-noitn | 2.44 | 2.44 | 0.00 | 1 -> 1 |
| sensevoice-small-itn | 2.47 | 2.47 | 0.00 | 2 -> 2 |
| qwen3-asr-1.7b-ko-univa-release | 11.09 | 2.78 | 8.30 | 7 -> 3 |
| qwen3-asr-1.7b-ko-univa | 11.06 | 2.78 | 8.28 | 5 -> 4 |
| whisper-large-v3 | 6.79 | 3.04 | 3.75 | 4 -> 5 |
| qwen3-asr-1.7b | 5.56 | 3.28 | 2.28 | 3 -> 6 |
| buzzasr-korean | 11.07 | 3.50 | 7.58 | 6 -> 7 |

version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct +5.49 [+4.35,+6.71]* | kocer -0.50 [-0.91,-0.09]*; release-base nopunct +5.52 [+4.36,+6.77]* | kocer -0.50 [-0.98,-0.04]*

## fleurs: 86 utterances with numbers

| model | nospace+punct CER | kocer CER | drop | rank nopunct -> kocer |
|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | 5.68 | 5.35 | 0.32 | 1 -> 1 |
| whisper-large-v3 | 8.18 | 5.35 | 2.83 | 5 -> 2 |
| qwen3-asr-1.7b-ko-univa | 5.73 | 5.43 | 0.30 | 2 -> 3 |
| buzzasr-korean | 6.82 | 5.58 | 1.24 | 3 -> 4 |
| qwen3-asr-1.7b | 6.92 | 5.75 | 1.17 | 4 -> 5 |
| sensevoice-small-noitn | 15.07 | 8.65 | 6.42 | 6 -> 6 |
| sensevoice-small-itn | 15.22 | 8.73 | 6.49 | 7 -> 7 |

version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -1.19 [-1.91,-0.49]* | kocer -0.32 [-0.77,+0.12]; release-base nopunct -1.24 [-2.06,-0.36]* | kocer -0.40 [-0.99,+0.25]

## kspon (spelling ref): 628 utterances with numbers

| model | nospace+punct CER | kocer CER | drop | rank nopunct -> kocer |
|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | 6.85 | 5.82 | 1.03 | 1 -> 1 |
| qwen3-asr-1.7b-ko-univa | 9.27 | 6.59 | 2.68 | 2 -> 2 |
| qwen3-asr-1.7b | 15.35 | 8.14 | 7.21 | 5 -> 3 |
| buzzasr-korean | 10.73 | 8.34 | 2.39 | 3 -> 4 |
| whisper-large-v3 | 14.88 | 13.08 | 1.81 | 4 -> 5 |
| sensevoice-small-noitn | 16.81 | 13.96 | 2.85 | 6 -> 6 |
| sensevoice-small-itn | 16.88 | 14.09 | 2.79 | 7 -> 7 |

version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -6.08 [-6.84,-5.34]* | kocer -1.55 [-2.04,-1.06]*; release-base nopunct -8.50 [-9.32,-7.70]* | kocer -2.32 [-2.79,-1.88]*

## kspon (pronunciation ref): 628 utterances with numbers

| model | nospace+punct CER | kocer CER | drop | rank nopunct -> kocer |
|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | 13.80 | 5.42 | 8.38 | 3 -> 1 |
| qwen3-asr-1.7b-ko-univa | 12.59 | 6.03 | 6.56 | 2 -> 2 |
| qwen3-asr-1.7b | 9.67 | 7.83 | 1.84 | 1 -> 3 |
| buzzasr-korean | 14.93 | 8.02 | 6.91 | 4 -> 4 |
| sensevoice-small-noitn | 19.06 | 13.59 | 5.47 | 5 -> 5 |
| sensevoice-small-itn | 19.28 | 13.70 | 5.58 | 6 -> 6 |
| whisper-large-v3 | 20.02 | 14.11 | 5.91 | 7 -> 7 |

version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct +2.92 [+2.21,+3.64]* | kocer -1.80 [-2.29,-1.31]*; release-base nopunct +4.13 [+3.40,+4.91]* | kocer -2.41 [-2.86,-1.96]*
