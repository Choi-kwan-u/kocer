#!/bin/bash
# Run all 7 settings on the AI-Hub telephone validation set (tel_hr). Resumable.
# Log: logs/infer_tel.log
cd "$(dirname "$0")/.."   # benchmark root (expects venv_whisper, venv_qwen, venv_sense here)
export PYTHONUTF8=1 HF_HUB_OFFLINE=1
W=venv_whisper/Scripts/python.exe; Q=venv_qwen/Scripts/python.exe; S=venv_sense/Scripts/python.exe
for ds in tel_hr; do
  $Q scripts/infer_qwen.py TeamUNIVA/qwen3_asr_1.7b_ko qwen3-asr-1.7b-ko-univa-release $ds 4
  $W scripts/infer_whisper.py BuzzASR/korean buzzasr-korean $ds 8
  $Q scripts/infer_qwen.py TeamUNIVA/qwen3_asr_1.7b_ko_beta qwen3-asr-1.7b-ko-univa $ds 4
  $W scripts/infer_whisper.py openai/whisper-large-v3 whisper-large-v3 $ds 8
  $Q scripts/infer_qwen.py Qwen/Qwen3-ASR-1.7B qwen3-asr-1.7b $ds 4
  $S scripts/infer_sense.py sensevoice-small-itn $ds 1 16
  $S scripts/infer_sense.py sensevoice-small-noitn $ds 0 16
done
echo "=== TEL ALL DONE ==="
