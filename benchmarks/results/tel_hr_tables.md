# tel_hr: 1936 utterances (AI-Hub 저음질 전화망 음성인식 데이터, validation). CER %, numbers only.

| model | spelling raw | spelling nospace+punct | spelling kocer | pronunciation raw | pronunciation nospace+punct | pronunciation kocer | kocer, raw transcript (aihub=True) |
|---|---|---|---|---|---|---|---|
| whisper-large-v3 | 8.10 | 5.44 | 5.02 | 13.02 | 10.25 | 5.33 | 4.92 |
| BuzzASR | 8.17 | 5.97 | 5.61 | 12.97 | 10.62 | 5.93 | 5.50 |
| TeamUNIVA ko | 6.73 | 6.26 | 5.76 | 11.48 | 10.78 | 6.04 | 5.64 |
| TeamUNIVA ko beta | 10.64 | 9.83 | 9.17 | 14.93 | 13.86 | 9.31 | 8.97 |
| Qwen3-ASR base | 12.96 | 12.01 | 10.76 | 16.18 | 14.92 | 10.94 | 10.59 |
| SenseVoice itn | 23.32 | 21.66 | 21.30 | 26.85 | 24.85 | 21.38 | 21.08 |
| SenseVoice noitn | 24.57 | 21.86 | 21.55 | 28.04 | 25.01 | 21.58 | 21.32 |

## Reference-choice sensitivity (pronunciation − spelling, pt)

| model | nospace+punct | kocer |
|---|---|---|
| whisper-large-v3 | +4.81 | +0.31 |
| BuzzASR | +4.65 | +0.33 |
| TeamUNIVA ko | +4.52 | +0.28 |
| TeamUNIVA ko beta | +4.03 | +0.14 |
| Qwen3-ASR base | +2.92 | +0.18 |
| SenseVoice itn | +3.18 | +0.09 |
| SenseVoice noitn | +3.15 | +0.04 |

## Ranks

- spelling nospace+punct: whisper-large-v3 < BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn
- pronunciation nospace+punct: whisper-large-v3 < BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn
- spelling kocer: whisper-large-v3 < BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn
- pronunciation kocer: whisper-large-v3 < BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn
- raw transcript kocer: whisper-large-v3 < BuzzASR < TeamUNIVA ko < TeamUNIVA ko beta < Qwen3-ASR base < SenseVoice itn < SenseVoice noitn

## Where raw errors go (spelling reference, counts)

| model | raw errors | spacing | punctuation | numbers/letters | remaining |
|---|---|---|---|---|---|
| whisper-large-v3 | 6794 | 42% | 10% | 4% | 45% |
| BuzzASR | 6849 | 38% | 10% | 3% | 50% |
| TeamUNIVA ko | 5638 | 20% | 12% | 5% | 62% |
| TeamUNIVA ko beta | 8923 | 20% | 14% | 4% | 62% |
| Qwen3-ASR base | 10862 | 19% | 14% | 7% | 60% |
| SenseVoice itn | 19550 | 24% | 9% | 1% | 66% |
| SenseVoice noitn | 20598 | 23% | 13% | 1% | 64% |

## kocer.compare(): spelling reference, kocer

```
CER (1,936 pairs, 2,000 bootstrap resamples, 95% intervals, kocer 0.3.0)
  1. whisper-large-v3    5.02%   rank range [1, 1]   P(1st) 1.00
  2. BuzzASR             5.61%   rank range [2, 3]   P(1st) 0.00
  3. TeamUNIVA ko        5.76%   rank range [2, 3]   P(1st) 0.00
  4. TeamUNIVA ko beta   9.17%   rank range [4, 4]   P(1st) 0.00
  5. Qwen3-ASR base     10.76%   rank range [5, 5]   P(1st) 0.00
  6. SenseVoice itn     21.30%   rank range [6, 6]   P(1st) 0.00
  7. SenseVoice noitn   21.55%   rank range [7, 7]   P(1st) 0.00
Pairwise difference (row − col, %p), 95% interval, * = differs from 0
  whisper-large-v3  − BuzzASR            -0.58  [-0.74, -0.43] *
  whisper-large-v3  − TeamUNIVA ko       -0.74  [-1.02, -0.48] *
  whisper-large-v3  − TeamUNIVA ko beta  -4.15  [-5.19, -3.47] *
  whisper-large-v3  − Qwen3-ASR base     -5.73  [-6.13, -5.35] *
  whisper-large-v3  − SenseVoice itn     -16.27  [-16.98, -15.59] *
  whisper-large-v3  − SenseVoice noitn   -16.52  [-17.24, -15.83] *
  BuzzASR           − TeamUNIVA ko       -0.15  [-0.44, +0.12]
  BuzzASR           − TeamUNIVA ko beta  -3.57  [-4.60, -2.89] *
  BuzzASR           − Qwen3-ASR base     -5.15  [-5.57, -4.76] *
  BuzzASR           − SenseVoice itn     -15.69  [-16.35, -15.03] *
  BuzzASR           − SenseVoice noitn   -15.94  [-16.62, -15.27] *
  TeamUNIVA ko      − TeamUNIVA ko beta  -3.41  [-4.43, -2.76] *
  TeamUNIVA ko      − Qwen3-ASR base     -5.00  [-5.36, -4.65] *
  TeamUNIVA ko      − SenseVoice itn     -15.54  [-16.21, -14.87] *
  TeamUNIVA ko      − SenseVoice noitn   -15.79  [-16.48, -15.11] *
  TeamUNIVA ko beta − Qwen3-ASR base     -1.59  [-2.25, -0.52] *
  TeamUNIVA ko beta − SenseVoice itn     -12.13  [-13.01, -10.95] *
  TeamUNIVA ko beta − SenseVoice noitn   -12.38  [-13.26, -11.20] *
  Qwen3-ASR base    − SenseVoice itn     -10.54  [-11.22, -9.91] *
  Qwen3-ASR base    − SenseVoice noitn   -10.79  [-11.47, -10.15] *
  SenseVoice itn    − SenseVoice noitn   -0.25  [-0.36, -0.15] *
```

## kocer.compare(): raw transcript, kocer aihub=True

```
CER (1,936 pairs, 2,000 bootstrap resamples, 95% intervals, kocer 0.3.0)
  1. whisper-large-v3    4.92%   rank range [1, 1]   P(1st) 1.00
  2. BuzzASR             5.50%   rank range [2, 3]   P(1st) 0.00
  3. TeamUNIVA ko        5.64%   rank range [2, 3]   P(1st) 0.00
  4. TeamUNIVA ko beta   8.97%   rank range [4, 4]   P(1st) 0.00
  5. Qwen3-ASR base     10.59%   rank range [5, 5]   P(1st) 0.00
  6. SenseVoice itn     21.08%   rank range [6, 6]   P(1st) 0.00
  7. SenseVoice noitn   21.32%   rank range [7, 7]   P(1st) 0.00
Pairwise difference (row − col, %p), 95% interval, * = differs from 0
  whisper-large-v3  − BuzzASR            -0.58  [-0.73, -0.43] *
  whisper-large-v3  − TeamUNIVA ko       -0.72  [-0.99, -0.47] *
  whisper-large-v3  − TeamUNIVA ko beta  -4.05  [-5.08, -3.39] *
  whisper-large-v3  − Qwen3-ASR base     -5.67  [-6.07, -5.28] *
  whisper-large-v3  − SenseVoice itn     -16.16  [-16.87, -15.49] *
  whisper-large-v3  − SenseVoice noitn   -16.40  [-17.11, -15.72] *
  BuzzASR           − TeamUNIVA ko       -0.14  [-0.42, +0.13]
  BuzzASR           − TeamUNIVA ko beta  -3.47  [-4.48, -2.81] *
  BuzzASR           − Qwen3-ASR base     -5.08  [-5.50, -4.69] *
  BuzzASR           − SenseVoice itn     -15.58  [-16.24, -14.93] *
  BuzzASR           − SenseVoice noitn   -15.82  [-16.50, -15.15] *
  TeamUNIVA ko      − TeamUNIVA ko beta  -3.33  [-4.35, -2.69] *
  TeamUNIVA ko      − Qwen3-ASR base     -4.95  [-5.32, -4.60] *
  TeamUNIVA ko      − SenseVoice itn     -15.44  [-16.12, -14.77] *
  TeamUNIVA ko      − SenseVoice noitn   -15.68  [-16.38, -15.00] *
  TeamUNIVA ko beta − Qwen3-ASR base     -1.61  [-2.27, -0.57] *
  TeamUNIVA ko beta − SenseVoice itn     -12.11  [-12.99, -10.93] *
  TeamUNIVA ko beta − SenseVoice noitn   -12.35  [-13.22, -11.19] *
  Qwen3-ASR base    − SenseVoice itn     -10.50  [-11.17, -9.86] *
  Qwen3-ASR base    − SenseVoice noitn   -10.73  [-11.41, -10.09] *
  SenseVoice itn    − SenseVoice noitn   -0.24  [-0.34, -0.13] *
```

## Utterances with a digit in the spelling reference: 408

- spelling reference, nospace+punct: TeamUNIVA ko − Qwen3-ASR base = -6.58 pt [-7.46, -5.73] *
- spelling reference, kocer: TeamUNIVA ko − Qwen3-ASR base = -3.82 pt [-4.38, -3.28] *
- pronunciation reference, nospace+punct: TeamUNIVA ko − Qwen3-ASR base = -0.47 pt [-1.30, +0.43]
- pronunciation reference, kocer: TeamUNIVA ko − Qwen3-ASR base = -3.55 pt [-4.08, -3.01] *

## Runaway outputs (sentence kocer CER > 1, spelling reference)

- TeamUNIVA ko: 0
- TeamUNIVA ko beta: 2
- Qwen3-ASR base: 1
- BuzzASR: 0
- whisper-large-v3: 1
- SenseVoice itn: 0
- SenseVoice noitn: 0
