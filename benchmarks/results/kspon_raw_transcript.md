# KsponSpeech, kocer 0.4.0: spelling / pronunciation / raw transcript (aihub=True). 6000 utterances, numbers only.

| Model | kocer, spelling ref | kocer, pronunciation ref | kocer, raw transcript (`aihub=True`) | utterances where raw > min(spelling, pron) errors |
|---|---|---|---|---|
| TeamUNIVA/qwen3_asr_1.7b_ko | 6.31 | 6.12 | 5.79 | 0 |
| TeamUNIVA/qwen3_asr_1.7b_ko_beta | 7.06 | 6.71 | 6.45 | 0 |
| Qwen/Qwen3-ASR-1.7B | 8.62 | 8.60 | 8.15 | 0 |
| BuzzASR/korean | 9.62 | 9.51 | 9.10 | 0 |
| openai/whisper-large-v3 | 11.53 | 11.59 | 11.01 | 0 |
| SenseVoiceSmall (itn off) | 13.44 | 13.28 | 12.92 | 0 |
