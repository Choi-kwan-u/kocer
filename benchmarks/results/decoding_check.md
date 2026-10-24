
## KsponSpeech (clean+other, spelling ref) (6000 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 10.06 | 9.71 | 19 | 10 | 9.07 |
| model-card settings | 10.49 | 10.14 | 17 | 8 | 10.04 |

card - greedy, kocer: +0.43 pt [-0.49, +1.02]
kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 6.32; 2. qwen3-asr-1.7b-ko-univa 7.08; 3. qwen3-asr-1.7b 8.63; 4. BuzzASR greedy 9.71; 5. BuzzASR card settings 10.14; 6. whisper-large-v3 11.55; 7. sensevoice-small-noitn 13.46; 8. sensevoice-small-itn 13.60
(whisper-large-v3 greedy runaway A/B: 25/14)

## Zeroth (457 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 5.85 | 3.16 | 0 | 0 | 3.16 |
| model-card settings | 6.17 | 3.50 | 0 | 0 | 3.50 |

card - greedy, kocer: +0.34 pt [+0.21, +0.46] *
kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 2.37; 2. sensevoice-small-itn 2.40; 3. sensevoice-small-noitn 2.41; 4. qwen3-asr-1.7b-ko-univa 2.46; 5. qwen3-asr-1.7b 2.91; 6. whisper-large-v3 2.93; 7. BuzzASR greedy 3.16; 8. BuzzASR card settings 3.50
(whisper-large-v3 greedy runaway A/B: 0/0)

## FLEURS (382 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 4.79 | 4.72 | 0 | 0 | 4.72 |
| model-card settings | 5.37 | 5.30 | 0 | 0 | 5.30 |

card - greedy, kocer: +0.58 pt [+0.39, +0.77] *
kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 4.25; 2. qwen3-asr-1.7b 4.31; 3. qwen3-asr-1.7b-ko-univa 4.31; 4. whisper-large-v3 4.37; 5. BuzzASR greedy 4.72; 6. BuzzASR card settings 5.30; 7. sensevoice-small-noitn 6.91; 8. sensevoice-small-itn 6.95
(whisper-large-v3 greedy runaway A/B: 0/0)

## Common Voice 27 (579 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 3.98 | 3.88 | 0 | 0 | 3.88 |
| model-card settings | 4.25 | 4.15 | 0 | 0 | 4.15 |

card - greedy, kocer: +0.27 pt [+0.13, +0.42] *
kocer ranking with both BuzzASR runs: 1. BuzzASR greedy 3.88; 2. BuzzASR card settings 4.15; 3. whisper-large-v3 5.80; 4. qwen3-asr-1.7b-ko-univa-release 6.00; 5. qwen3-asr-1.7b-ko-univa 6.08; 6. qwen3-asr-1.7b 6.61; 7. sensevoice-small-itn 9.68; 8. sensevoice-small-noitn 9.72
(whisper-large-v3 greedy runaway A/B: 0/0)
