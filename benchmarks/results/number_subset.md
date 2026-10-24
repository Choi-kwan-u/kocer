
## zeroth: 152 utterances with numbers

| model | nospace+punct CER | kocer CER | drop | rank nopunct -> kocer |
|---|---|---|---|---|
| sensevoice-small-noitn | 2.44 | 2.44 | 0.00 | 1 -> 1 |
| sensevoice-small-itn | 2.47 | 2.47 | 0.00 | 2 -> 2 |
| qwen3-asr-1.7b-ko-univa | 11.06 | 2.85 | 8.20 | 5 -> 3 |
| qwen3-asr-1.7b-ko-univa-release | 11.09 | 2.87 | 8.22 | 7 -> 4 |
| whisper-large-v3 | 6.79 | 3.11 | 3.68 | 4 -> 5 |
| qwen3-asr-1.7b | 5.56 | 3.31 | 2.25 | 3 -> 6 |
| buzzasr-korean | 11.07 | 3.67 | 7.40 | 6 -> 7 |

version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct +5.49 [+4.35,+6.71]* | kocer -0.46 [-0.90,-0.03]*; release-base nopunct +5.52 [+4.36,+6.77]* | kocer -0.44 [-0.93,+0.04]

## fleurs: 86 utterances with numbers

| model | nospace+punct CER | kocer CER | drop | rank nopunct -> kocer |
|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | 5.68 | 5.57 | 0.10 | 1 -> 1 |
| qwen3-asr-1.7b-ko-univa | 5.73 | 5.65 | 0.08 | 2 -> 2 |
| whisper-large-v3 | 8.18 | 5.77 | 2.41 | 5 -> 3 |
| qwen3-asr-1.7b | 6.92 | 5.99 | 0.92 | 4 -> 4 |
| buzzasr-korean | 6.82 | 6.57 | 0.25 | 3 -> 5 |
| sensevoice-small-noitn | 15.07 | 8.88 | 6.19 | 6 -> 6 |
| sensevoice-small-itn | 15.22 | 8.98 | 6.24 | 7 -> 7 |

version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -1.19 [-1.91,-0.49]* | kocer -0.34 [-0.79,+0.09]; release-base nopunct -1.24 [-2.06,-0.36]* | kocer -0.42 [-1.01,+0.22]

## kspon (spelling ref): 628 utterances with numbers

| model | nospace+punct CER | kocer CER | drop | rank nopunct -> kocer |
|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | 6.85 | 5.89 | 0.96 | 1 -> 1 |
| qwen3-asr-1.7b-ko-univa | 9.27 | 6.68 | 2.59 | 2 -> 2 |
| qwen3-asr-1.7b | 15.35 | 8.23 | 7.12 | 5 -> 3 |
| buzzasr-korean | 10.73 | 8.54 | 2.20 | 3 -> 4 |
| whisper-large-v3 | 14.88 | 13.14 | 1.74 | 4 -> 5 |
| sensevoice-small-noitn | 16.81 | 14.12 | 2.69 | 6 -> 6 |
| sensevoice-small-itn | 16.88 | 14.25 | 2.63 | 7 -> 7 |

version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct -6.08 [-6.84,-5.34]* | kocer -1.55 [-2.06,-1.07]*; release-base nopunct -8.50 [-9.32,-7.70]* | kocer -2.34 [-2.80,-1.89]*

## kspon (pronunciation ref): 628 utterances with numbers

| model | nospace+punct CER | kocer CER | drop | rank nopunct -> kocer |
|---|---|---|---|---|
| qwen3-asr-1.7b-ko-univa-release | 13.80 | 5.51 | 8.28 | 3 -> 1 |
| qwen3-asr-1.7b-ko-univa | 12.59 | 6.13 | 6.45 | 2 -> 2 |
| qwen3-asr-1.7b | 9.67 | 7.87 | 1.80 | 1 -> 3 |
| buzzasr-korean | 14.93 | 8.28 | 6.65 | 4 -> 4 |
| sensevoice-small-noitn | 19.06 | 13.61 | 5.45 | 5 -> 5 |
| sensevoice-small-itn | 19.28 | 13.75 | 5.53 | 6 -> 6 |
| whisper-large-v3 | 20.02 | 14.26 | 5.76 | 7 -> 7 |

version check, fine-tune minus base (negative = fine-tune better): beta-base nopunct +2.92 [+2.21,+3.64]* | kocer -1.73 [-2.23,-1.23]*; release-base nopunct +4.13 [+3.40,+4.91]* | kocer -2.36 [-2.80,-1.91]*
