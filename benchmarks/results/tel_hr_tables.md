# tel_hr: 1936 utterances (AI-Hub 저음질 전화망 음성인식 데이터, validation). CER %, numbers only.

| model | spelling raw | spelling nospace+punct | spelling kocer | pronunciation raw | pronunciation nospace+punct | pronunciation kocer | kocer, raw transcript (aihub=True) |
|---|---|---|---|---|---|---|---|
| whisper-large-v3 | 5.92 | 5.44 | 4.97 | 11.03 | 10.25 | 5.04 | 4.95 |
| BuzzASR | 6.38 | 5.97 | 5.31 | 11.36 | 10.62 | 5.40 | 5.29 |
| TeamUNIVA ko | 6.73 | 6.26 | 5.69 | 11.48 | 10.78 | 5.76 | 5.68 |
| TeamUNIVA ko beta | 10.64 | 9.83 | 9.05 | 14.93 | 13.86 | 9.09 | 9.02 |
| Qwen3-ASR base | 12.96 | 12.01 | 10.69 | 16.18 | 14.92 | 10.71 | 10.66 |
| SenseVoice itn | 23.32 | 21.66 | 21.29 | 26.85 | 24.85 | 21.31 | 21.25 |
| SenseVoice noitn | 24.57 | 21.86 | 21.49 | 28.04 | 25.01 | 21.55 | 21.45 |

## Reference-choice sensitivity (pronunciation − spelling, pt)

| model | nospace+punct | kocer |
|---|---|---|
| whisper-large-v3 | +4.81 | +0.07 |
| BuzzASR | +4.65 | +0.09 |
| TeamUNIVA ko | +4.52 | +0.06 |
| TeamUNIVA ko beta | +4.03 | +0.04 |
| Qwen3-ASR base | +2.92 | +0.02 |
| SenseVoice itn | +3.18 | +0.02 |
| SenseVoice noitn | +3.15 | +0.06 |

## Ranks

- spelling nospace+punct: whisper-large-v3 < BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn
- pronunciation nospace+punct: whisper-large-v3 < BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn
- spelling kocer: whisper-large-v3 < BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn
- pronunciation kocer: whisper-large-v3 < BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn
- raw transcript kocer: whisper-large-v3 < BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn

## Where raw errors go (spelling reference, counts)

| model | raw errors | spacing | punctuation | numbers/letters | remaining |
|---|---|---|---|---|---|
| whisper-large-v3 | 4961 | 20% | 13% | 6% | 61% |
| BuzzASR | 5348 | 20% | 12% | 7% | 60% |
| TeamUNIVA ko | 5638 | 20% | 12% | 6% | 61% |
| TeamUNIVA ko beta | 8923 | 20% | 14% | 5% | 62% |
| Qwen3-ASR base | 10862 | 19% | 14% | 7% | 60% |
| SenseVoice itn | 19550 | 24% | 9% | 1% | 66% |
| SenseVoice noitn | 20598 | 23% | 13% | 1% | 63% |

## kocer.compare(): spelling reference, kocer

```
CER (1,936 pairs, 2,000 bootstrap resamples, 95% intervals, kocer 0.5.0)
  1. whisper-large-v3    4.97%   rank range [1, 1]   P(1st) 1.00
  2. BuzzASR             5.31%   rank range [2, 2]   P(1st) 0.00
  3. TeamUNIVA ko        5.69%   rank range [3, 3]   P(1st) 0.00
  4. TeamUNIVA ko beta   9.05%   rank range [4, 4]   P(1st) 0.00
  5. Qwen3-ASR base     10.69%   rank range [5, 5]   P(1st) 0.00
  6. SenseVoice itn     21.29%   rank range [6, 6]   P(1st) 0.00
  7. SenseVoice noitn   21.49%   rank range [7, 7]   P(1st) 0.00
Pairwise difference (row − col, %p), 95% interval, * = differs from 0
  whisper-large-v3  − BuzzASR            -0.34  [-0.47, -0.21] *
  whisper-large-v3  − TeamUNIVA ko       -0.72  [-1.00, -0.47] *
  whisper-large-v3  − TeamUNIVA ko beta  -4.08  [-5.11, -3.42] *
  whisper-large-v3  − Qwen3-ASR base     -5.71  [-6.11, -5.33] *
  whisper-large-v3  − SenseVoice itn     -16.32  [-17.01, -15.63] *
  whisper-large-v3  − SenseVoice noitn   -16.52  [-17.23, -15.82] *
  BuzzASR           − TeamUNIVA ko       -0.38  [-0.66, -0.12] *
  BuzzASR           − TeamUNIVA ko beta  -3.74  [-4.77, -3.08] *
  BuzzASR           − Qwen3-ASR base     -5.37  [-5.78, -4.99] *
  BuzzASR           − SenseVoice itn     -15.98  [-16.68, -15.28] *
  BuzzASR           − SenseVoice noitn   -16.18  [-16.88, -15.47] *
  TeamUNIVA ko      − TeamUNIVA ko beta  -3.36  [-4.38, -2.72] *
  TeamUNIVA ko      − Qwen3-ASR base     -4.99  [-5.36, -4.64] *
  TeamUNIVA ko      − SenseVoice itn     -15.59  [-16.27, -14.92] *
  TeamUNIVA ko      − SenseVoice noitn   -15.79  [-16.48, -15.12] *
  TeamUNIVA ko beta − Qwen3-ASR base     -1.63  [-2.30, -0.58] *
  TeamUNIVA ko beta − SenseVoice itn     -12.24  [-13.12, -11.06] *
  TeamUNIVA ko beta − SenseVoice noitn   -12.43  [-13.31, -11.27] *
  Qwen3-ASR base    − SenseVoice itn     -10.60  [-11.29, -9.96] *
  Qwen3-ASR base    − SenseVoice noitn   -10.80  [-11.48, -10.16] *
  SenseVoice itn    − SenseVoice noitn   -0.20  [-0.30, -0.10] *
```

## kocer.compare(): raw transcript, kocer aihub=True

```
CER (1,936 pairs, 2,000 bootstrap resamples, 95% intervals, kocer 0.5.0)
  1. whisper-large-v3    4.95%   rank range [1, 1]   P(1st) 1.00
  2. BuzzASR             5.29%   rank range [2, 2]   P(1st) 0.00
  3. TeamUNIVA ko        5.68%   rank range [3, 3]   P(1st) 0.00
  4. TeamUNIVA ko beta   9.02%   rank range [4, 4]   P(1st) 0.00
  5. Qwen3-ASR base     10.66%   rank range [5, 5]   P(1st) 0.00
  6. SenseVoice itn     21.25%   rank range [6, 6]   P(1st) 0.00
  7. SenseVoice noitn   21.45%   rank range [7, 7]   P(1st) 0.00
Pairwise difference (row − col, %p), 95% interval, * = differs from 0
  whisper-large-v3  − BuzzASR            -0.34  [-0.47, -0.21] *
  whisper-large-v3  − TeamUNIVA ko       -0.73  [-1.00, -0.47] *
  whisper-large-v3  − TeamUNIVA ko beta  -4.07  [-5.10, -3.41] *
  whisper-large-v3  − Qwen3-ASR base     -5.71  [-6.11, -5.32] *
  whisper-large-v3  − SenseVoice itn     -16.30  [-17.00, -15.62] *
  whisper-large-v3  − SenseVoice noitn   -16.50  [-17.21, -15.80] *
  BuzzASR           − TeamUNIVA ko       -0.39  [-0.66, -0.13] *
  BuzzASR           − TeamUNIVA ko beta  -3.73  [-4.76, -3.06] *
  BuzzASR           − Qwen3-ASR base     -5.37  [-5.77, -4.98] *
  BuzzASR           − SenseVoice itn     -15.96  [-16.66, -15.26] *
  BuzzASR           − SenseVoice noitn   -16.16  [-16.86, -15.46] *
  TeamUNIVA ko      − TeamUNIVA ko beta  -3.34  [-4.37, -2.70] *
  TeamUNIVA ko      − Qwen3-ASR base     -4.98  [-5.35, -4.63] *
  TeamUNIVA ko      − SenseVoice itn     -15.58  [-16.25, -14.91] *
  TeamUNIVA ko      − SenseVoice noitn   -15.77  [-16.47, -15.10] *
  TeamUNIVA ko beta − Qwen3-ASR base     -1.64  [-2.30, -0.59] *
  TeamUNIVA ko beta − SenseVoice itn     -12.23  [-13.11, -11.05] *
  TeamUNIVA ko beta − SenseVoice noitn   -12.43  [-13.31, -11.27] *
  Qwen3-ASR base    − SenseVoice itn     -10.59  [-11.27, -9.96] *
  Qwen3-ASR base    − SenseVoice noitn   -10.79  [-11.48, -10.15] *
  SenseVoice itn    − SenseVoice noitn   -0.20  [-0.30, -0.10] *
```

## Utterances with a digit in the spelling reference: 408

- spelling reference, nospace+punct: TeamUNIVA ko − Qwen3-ASR base = -6.58 pt [-7.46, -5.73] *
- spelling reference, kocer: TeamUNIVA ko − Qwen3-ASR base = -3.77 pt [-4.34, -3.23] *
- pronunciation reference, nospace+punct: TeamUNIVA ko − Qwen3-ASR base = -0.47 pt [-1.30, +0.43]
- pronunciation reference, kocer: TeamUNIVA ko − Qwen3-ASR base = -3.66 pt [-4.21, -3.12] *

## Runaway outputs (sentence kocer CER > 1, spelling reference)

- TeamUNIVA ko: 0
- TeamUNIVA ko beta: 2
- Qwen3-ASR base: 1
- BuzzASR: 0
- whisper-large-v3: 1
- SenseVoice itn: 1
- SenseVoice noitn: 1
