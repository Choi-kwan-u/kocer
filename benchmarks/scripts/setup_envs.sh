#!/bin/bash
set -x
BASE="${PYTHON:-python3}"   # 3.10 이상, CUDA 12.4 드라이버
cd "$(dirname "$0")/.."
TORCH="torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124"
COMMON="datasets soundfile librosa jiwer kocer nlptutti huggingface_hub[cli] pandas tqdm"

# 1) whisper / BuzzASR venv (+ scoring)
"$BASE" -m venv venv_whisper
venv_whisper/Scripts/python.exe -m pip install -U pip
venv_whisper/Scripts/python.exe -m pip install $TORCH
venv_whisper/Scripts/python.exe -m pip install transformers accelerate $COMMON
echo "=== venv_whisper DONE ==="

# 2) qwen-asr venv
"$BASE" -m venv venv_qwen
venv_qwen/Scripts/python.exe -m pip install -U pip
venv_qwen/Scripts/python.exe -m pip install $TORCH
venv_qwen/Scripts/python.exe -m pip install qwen-asr $COMMON
echo "=== venv_qwen DONE ==="

# 3) funasr venv
"$BASE" -m venv venv_sense
venv_sense/Scripts/python.exe -m pip install -U pip
venv_sense/Scripts/python.exe -m pip install $TORCH
venv_sense/Scripts/python.exe -m pip install funasr modelscope $COMMON
echo "=== venv_sense DONE ==="
