
## KsponSpeech (clean+other, spelling ref) (6000 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 10.06 | 9.62 | 19 | 10 | 8.98 |
| model-card settings | 10.49 | 10.05 | 17 | 8 | 9.95 |

card - greedy, kocer: +0.43 pt [-0.49, +1.02]
kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 6.31; 2. qwen3-asr-1.7b-ko-univa 7.06; 3. qwen3-asr-1.7b 8.62; 4. BuzzASR greedy 9.62; 5. BuzzASR card settings 10.05; 6. whisper-large-v3 11.53; 7. sensevoice-small-noitn 13.44; 8. sensevoice-small-itn 13.58
(whisper-large-v3 greedy runaway A/B: 25/14)

## Zeroth (457 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 5.85 | 3.10 | 0 | 0 | 3.10 |
| model-card settings | 6.17 | 3.43 | 0 | 0 | 3.43 |

card - greedy, kocer: +0.34 pt [+0.21, +0.46] *
kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 2.34; 2. sensevoice-small-itn 2.40; 3. sensevoice-small-noitn 2.41; 4. qwen3-asr-1.7b-ko-univa 2.44; 5. qwen3-asr-1.7b 2.90; 6. whisper-large-v3 2.90; 7. BuzzASR greedy 3.10; 8. BuzzASR card settings 3.43
(whisper-large-v3 greedy runaway A/B: 0/0)

## FLEURS (382 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 4.79 | 4.31 | 0 | 0 | 4.31 |
| model-card settings | 5.37 | 4.90 | 0 | 0 | 4.90 |

card - greedy, kocer: +0.59 pt [+0.39, +0.78] *
kocer ranking with both BuzzASR runs: 1. qwen3-asr-1.7b-ko-univa-release 4.19; 2. qwen3-asr-1.7b 4.25; 3. whisper-large-v3 4.25; 4. qwen3-asr-1.7b-ko-univa 4.25; 5. BuzzASR greedy 4.31; 6. BuzzASR card settings 4.90; 7. sensevoice-small-noitn 6.79; 8. sensevoice-small-itn 6.83
(whisper-large-v3 greedy runaway A/B: 0/0)

## Common Voice 27 (579 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 3.98 | 3.88 | 0 | 0 | 3.88 |
| model-card settings | 4.25 | 4.15 | 0 | 0 | 4.15 |

card - greedy, kocer: +0.27 pt [+0.13, +0.42] *
kocer ranking with both BuzzASR runs: 1. BuzzASR greedy 3.88; 2. BuzzASR card settings 4.15; 3. whisper-large-v3 5.80; 4. qwen3-asr-1.7b-ko-univa-release 6.00; 5. qwen3-asr-1.7b-ko-univa 6.08; 6. qwen3-asr-1.7b 6.61; 7. sensevoice-small-itn 9.68; 8. sensevoice-small-noitn 9.72
(whisper-large-v3 greedy runaway A/B: 0/0)

## AI-Hub telephone HR (spelling ref) (1936 utt.)

| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |
|---|---|---|---|---|---|
| greedy, no repetition penalty (published) | 5.97 | 5.36 | 0 | 0 | 5.36 |
| model-card settings | 6.87 | 6.26 | 0 | 0 | 6.26 |

card - greedy, kocer: +0.90 pt [+0.78, +1.02] *
kocer ranking with both BuzzASR runs: 1. whisper-large-v3 5.02; 2. BuzzASR greedy 5.36; 3. qwen3-asr-1.7b-ko-univa-release 5.75; 4. BuzzASR card settings 6.26; 5. qwen3-asr-1.7b-ko-univa 9.12; 6. qwen3-asr-1.7b 10.75; 7. sensevoice-small-itn 21.33; 8. sensevoice-small-noitn 21.53
(whisper-large-v3 greedy runaway A/B: 1/0)
