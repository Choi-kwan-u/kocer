
## KsponSpeech (clean+other, spelling ref) (6000 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 10.06 | 9.61 | 19 | 10 | 8.97 |
| model-card settings | 10.49 | 10.04 | 17 | 8 | 9.94 |

card - greedy, kocer: +0.43 pt [-0.49, +1.02]
kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 6.30; 2. qwen3-asr-1.7b-ko-univa 7.05; 3. qwen3-asr-1.7b 8.62; 4. BuzzASR greedy 9.61; 5. BuzzASR card settings 10.04; 6. whisper-large-v3 11.53; 7. sensevoice-small-noitn 13.42; 8. sensevoice-small-itn 13.56
(whisper-large-v3 greedy runaway A/B: 25/14)

## Zeroth (457 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 5.85 | 3.08 | 0 | 0 | 3.08 |
| model-card settings | 6.17 | 3.43 | 0 | 0 | 3.43 |

card - greedy, kocer: +0.35 pt [+0.23, +0.48] *
kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 2.32; 2. sensevoice-small-itn 2.40; 3. sensevoice-small-noitn 2.41; 4. qwen3-asr-1.7b-ko-univa 2.42; 5. qwen3-asr-1.7b 2.90; 6. whisper-large-v3 2.90; 7. BuzzASR greedy 3.08; 8. BuzzASR card settings 3.43
(whisper-large-v3 greedy runaway A/B: 0/0)

## FLEURS (382 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 4.79 | 4.28 | 0 | 0 | 4.28 |
| model-card settings | 5.37 | 4.85 | 0 | 0 | 4.85 |

card - greedy, kocer: +0.57 pt [+0.34, +0.78] *
kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 4.19; 2. whisper-large-v3 4.24; 3. qwen3-asr-1.7b 4.25; 4. qwen3-asr-1.7b-ko-univa 4.25; 5. BuzzASR greedy 4.28; 6. BuzzASR card settings 4.85; 7. sensevoice-small-noitn 6.76; 8. sensevoice-small-itn 6.81
(whisper-large-v3 greedy runaway A/B: 0/0)

## Common Voice 27 (579 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 3.98 | 3.88 | 0 | 0 | 3.88 |
| model-card settings | 4.25 | 4.15 | 0 | 0 | 4.15 |

card - greedy, kocer: +0.27 pt [+0.13, +0.42] *
kocer ranking with both BuzzASR runs: 1. BuzzASR greedy 3.88; 2. BuzzASR card settings 4.15; 3. whisper-large-v3 5.80; 4. qwen3-asr-1.7b-ko-univa-release 5.97; 5. qwen3-asr-1.7b-ko-univa 6.05; 6. qwen3-asr-1.7b 6.61; 7. sensevoice-small-itn 9.68; 8. sensevoice-small-noitn 9.72
(whisper-large-v3 greedy runaway A/B: 0/0)

## AI-Hub telephone HR (spelling ref) (1936 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 5.97 | 5.31 | 0 | 0 | 5.31 |
| model-card settings | 6.87 | 6.21 | 0 | 0 | 6.21 |

card - greedy, kocer: +0.90 pt [+0.78, +1.02] *
kocer ranking with both BuzzASR runs: 1. whisper-large-v3 4.97; 2. BuzzASR greedy 5.31; 3. qwen3-asr-1.7b-ko-univa-release 5.69; 4. BuzzASR card settings 6.21; 5. qwen3-asr-1.7b-ko-univa 9.05; 6. qwen3-asr-1.7b 10.69; 7. sensevoice-small-itn 21.29; 8. sensevoice-small-noitn 21.49
(whisper-large-v3 greedy runaway A/B: 1/0)
