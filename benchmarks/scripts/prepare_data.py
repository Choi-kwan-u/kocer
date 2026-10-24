"""Download test splits and write data/{name}/test.jsonl + 16 kHz wav files.
Row: {"id", "ref", "audio_path", ...extra fields}. Audio decoded without `datasets` Audio feature
(datasets>=4 needs torchcodec) -> parquet bytes / tar members decoded with soundfile + librosa."""
import io, json, os, sys, tarfile, csv
import numpy as np, pandas as pd, soundfile as sf, librosa
from huggingface_hub import hf_hub_download

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

def to16k(y, sr):
    if y.ndim > 1: y = y.mean(axis=1)
    if sr != 16000: y = librosa.resample(y.astype(np.float32), orig_sr=sr, target_sr=16000)
    return y.astype(np.float32)

def write(name, rows):
    d = os.path.join(DATA, name); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "test.jsonl"), "w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[{name}] {len(rows)} rows -> {d}/test.jsonl")

def zeroth():
    p = hf_hub_download("kresnik/zeroth_korean", "data/test-00000-of-00001.parquet", repo_type="dataset")
    df = pd.read_parquet(p)
    wav = os.path.join(DATA, "zeroth", "wav"); os.makedirs(wav, exist_ok=True)
    rows = []
    for _, r in df.iterrows():
        a = r["audio"]; y, sr = sf.read(io.BytesIO(a["bytes"]))
        out = os.path.join(wav, f"{r['id']}.wav"); sf.write(out, to16k(y, sr), 16000)
        rows.append({"id": str(r["id"]), "ref": r["text"], "audio_path": out, "speaker_id": int(r["speaker_id"])})
    write("zeroth", rows)

def fleurs():
    tsv = hf_hub_download("google/fleurs", "data/ko_kr/test.tsv", repo_type="dataset")
    tgz = hf_hub_download("google/fleurs", "data/ko_kr/audio/test.tar.gz", repo_type="dataset")
    cols = ["id", "file_name", "raw_transcription", "transcription", "chars", "num_samples", "gender"]
    df = pd.read_csv(tsv, sep="\t", header=None, names=cols, quoting=csv.QUOTE_NONE, dtype=str)
    meta = {r.file_name: r for r in df.itertuples()}
    wav = os.path.join(DATA, "fleurs", "wav"); os.makedirs(wav, exist_ok=True)
    rows = []
    with tarfile.open(tgz) as tf:
        for m in tf:
            if not m.isfile(): continue
            fn = os.path.basename(m.name)
            if fn not in meta: continue
            y, sr = sf.read(io.BytesIO(tf.extractfile(m).read()))
            out = os.path.join(wav, fn); sf.write(out, to16k(y, sr), 16000)
            r = meta[fn]
            rows.append({"id": f"{r.id}_{fn[:-4]}", "ref": r.raw_transcription, "ref_normalized": r.transcription,
                         "audio_path": out, "gender": r.gender})
    rows.sort(key=lambda x: x["id"]); write("fleurs", rows)

def commonvoice():
    from datasets import load_dataset
    ds = load_dataset("mozilla-foundation/common_voice_17_0", "ko", split="test", trust_remote_code=True)
    wav = os.path.join(DATA, "commonvoice", "wav"); os.makedirs(wav, exist_ok=True)
    rows = []
    for i, r in enumerate(ds):
        a = r["audio"]; out = os.path.join(wav, f"cv_{i:05d}.wav")
        sf.write(out, to16k(np.asarray(a["array"]), a["sampling_rate"]), 16000)
        rows.append({"id": f"cv_{i:05d}", "ref": r["sentence"], "audio_path": out})
    write("commonvoice", rows)

if __name__ == "__main__":
    for n in sys.argv[1:] or ["zeroth", "fleurs"]:
        globals()[n]()
